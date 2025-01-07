from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.memory import ConversationBufferMemory
import streamlit as st
import time
import os
import google.generativeai as genai

from config import get_gemini_model
from crud.tool import find_related_info
from google.generativeai.types import content_types
from collections.abc import Iterable


def tool_config_from_mode(mode: str, fns: Iterable[str] = ()):
    """Create a tool config with the specified function calling mode."""
    return content_types.to_tool_config(
        {"function_calling_config": {"mode": mode, "allowed_function_names": fns}}
    )


prompt = """
You are a chatbot dedicated to providing information about safety, training and anything else that the user asks.
To answer the user's questions, you MUST use the tools provided to you.

If you aren't able to answer the user's question using the provided tool, you should let the user know that you don't have the information.

"""

tool_config = tool_config_from_mode("any", fns=["find_related_info"])

model = genai.GenerativeModel(
    model_name=get_gemini_model(), tools=[find_related_info], system_instruction=prompt
)
chat = model.start_chat(enable_automatic_function_calling=True)

st.title("CIC Chatbot")
st.text("This is a simple chatbot that uses the provided CIC data to answer questions.")


user_quest = st.text_input("Ask a question:")
btn = st.button("Ask")

if btn and user_quest:
    result = chat.send_message(user_quest, tool_config=tool_config)
    print(result.parts)
    st.subheader("Response : ")
    for word in result:
        st.text(word.text)


# template = """
#     Use the following pieces of context to answer the question at the end.
#     If you don't know the answer, don't try to make up an answer and just try to be helpful using the context provided.

#     Context: {context}
#     History: {history}
#     Question: {question}
#     Helpful Answer:
# """

# memory = ConversationBufferMemory(
#     memory_key="history", return_messages=True, input_key="question"
# )

# prompt = PromptTemplate(
#     input_variables=["context", "history", "question"],
#     template=template,
# )

# qa_chain = RetrievalQA.from_chain_type(
#     llm=llm,
#     chain_type="stuff",
#     retriever=retriever,
#     verbose=True,
#     chain_type_kwargs={
#         "verbose": True,
#         "prompt": prompt,
#         "memory": memory,
#     },
# )

# # Initialize the chat history
# if "chat_history" not in st.session_state:
#     st.session_state.chat_history = []


# for message in st.session_state.chat_history:
#     with st.chat_message(message["role"]):
#         st.markdown(message["message"])

# if user_input := st.chat_input("You:", key="user_input"):
#     user_message = {"role": "user", "message": user_input}
#     st.session_state.chat_history.append(user_message)
#     with st.chat_message("user"):
#         st.markdown(user_input)
#     with st.chat_message("assistant"):
#         with st.spinner("Assistant is typing..."):
#             response = qa_chain(user_input)
#         message_placeholder = st.empty()
#         full_response = ""
#         for chunk in response["result"].split():
#             full_response += chunk + " "
#             time.sleep(0.05)
#             # Add a blinking cursor to simulate typing
#             message_placeholder.markdown(full_response + "▌")
#         message_placeholder.markdown(full_response)

#     chatbot_message = {"role": "assistant", "message": response["result"]}
#     st.session_state.chat_history.append(chatbot_message)
