from langchain.chains import RetrievalQA
from langchain.callbacks.manager import CallbackManager
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain_chroma import Chroma
from langchain_ollama import OllamaEmbeddings, OllamaLLM
from langchain.prompts import PromptTemplate
from langchain.memory import ConversationBufferMemory
import streamlit as st
import time
import os

vectorstore = Chroma(
    persist_directory="vector_store_dir",
    embedding_function=OllamaEmbeddings(model="llama3.2"),
)
callbacks = [StreamingStdOutCallbackHandler()]

OLLAMA_URL = os.environ.get("OLLAMA_URL", "http://localhost:11434")

llm = OllamaLLM(
    base_url=OLLAMA_URL,
    model="llama3.2",
    verbose=True,
    callback_manager=CallbackManager([StreamingStdOutCallbackHandler()]),
)

retriever = vectorstore.as_retriever(k=10)

template = """
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, don't try to make up an answer and just try to be helpful using the context provided.

    Context: {context}
    History: {history}
    Question: {question}
    Helpful Answer:
"""

memory = ConversationBufferMemory(
    memory_key="history", return_messages=True, input_key="question"
)

prompt = PromptTemplate(
    input_variables=["context", "history", "question"],
    template=template,
)

qa_chain = RetrievalQA.from_chain_type(
    llm=llm,
    chain_type="stuff",
    retriever=retriever,
    verbose=True,
    chain_type_kwargs={
        "verbose": True,
        "prompt": prompt,
        "memory": memory,
    },
)

# Initialize the chat history
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

st.title("CIC Chatbot")
st.text("This is a simple chatbot that uses the provided CIC data to answer questions.")

for message in st.session_state.chat_history:
    with st.chat_message(message["role"]):
        st.markdown(message["message"])

if user_input := st.chat_input("You:", key="user_input"):
    user_message = {"role": "user", "message": user_input}
    st.session_state.chat_history.append(user_message)
    with st.chat_message("user"):
        st.markdown(user_input)
    with st.chat_message("assistant"):
        with st.spinner("Assistant is typing..."):
            response = qa_chain(user_input)
        message_placeholder = st.empty()
        full_response = ""
        for chunk in response["result"].split():
            full_response += chunk + " "
            time.sleep(0.05)
            # Add a blinking cursor to simulate typing
            message_placeholder.markdown(full_response + "▌")
        message_placeholder.markdown(full_response)

    chatbot_message = {"role": "assistant", "message": response["result"]}
    st.session_state.chat_history.append(chatbot_message)
