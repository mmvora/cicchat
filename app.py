import streamlit as st
import google.generativeai as genai

from config import get_gemini_model
from crud.tools import find_related_info
from google.generativeai.types import content_types
from collections.abc import Iterable


def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )


prompt = """
You are a chatbot dedicated to providing information on anything that the user asks.
To answer the user's questions, you MUST use the tools provided to you.

If you aren't able to answer the user's question using the provided tool, you should let the user know that you don't have the information.

"""

tool_config = tool_config_from_mode("any", fns=["find_related_info"])

model = genai.GenerativeModel(
    model_name=get_gemini_model(), tools=[find_related_info], system_instruction=prompt
)
chat = model.start_chat(enable_automatic_function_calling=True)

st.title("RAG Chatbot")
st.text("This is a simple chatbot that uses the provided data to answer questions.")


user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = chat.send_message(user_quest, tool_config=tool_config)
    print(result.parts)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)
