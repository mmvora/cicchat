# CIC ChatBot MVP
## Overview
This is a basic chatbot that is designed to let you speak to a provided set of documents, in our case some CIC information. 

## Prerequisites
You will need the following prerequisites to run this project:
- Python 3.10 or higher installed on your machine
- For this project I used Llama as the model (run locally). I recommend installing it and running it via Ollama. 
You can find the instructions [here](https://ollama.com/) and use the `llama3.2` model.
  - Once installed (assuming you are using a mac), you can run the following command to start the model:
  ```ollama run llama3.2```
  - Please verify that the model is running on port 11434 (you can check this by going to http://localhost:11434 and you should see the message "Ollama is running").
    If it is running on a different port, you will need to create a .env file (you can just duplicate the `.env.example` file and rename it to `.env`) in the root of the project and add/modify line:
    ```OLLAMA_URL=http://localhost:<port>```

## How to run the project
- If you want to not make any changes and just run the chatbot, you can first install the requirements by running:
  ```pip install -r requirements.txt``` (you may have to use `pip3` instead of `pip` depending on your setup).
    - I recommend using a virtual environment to install the requirements. (see [here](https://docs.python.org/3/library/venv.html) for more information on how to set up a virtual environment).
- Then you can run the chatbot by running (in the root directory of the repo):
  ```streamlit run app.py```
- This will open a new tab in your browser with the chatbot. You can start chatting with it by typing in the text box at the bottom of the screen.
  - (if you can't see it in the browser, you can try going to the following link: http://localhost:8501)

## How to add more data sources
- The simplest way to add more data sources is to add more documents to the `data_sources` folder, then delete the exisiting `vector_store_dir` folder and run the following command:
    ```python -m create_vector_store``` in the root of the project.


Formatted using [ruff](https://docs.astral.sh/ruff/)


# Approach
The approach I took was to use the Llama model to generate embeddings for the documents in the data_sources folder. I then used these embeddings to find the most similar document to the user's query. It was a very simple approach but it worked well for the MVP, if I was to do it again I would probably use a more advanced model and use an SQL database to store the embeddings - this would allow for:
1. A larger dataset
2. We can add tool calls to A/B test various similarity metrics and querying strategies to fetch the most relevant documents
3. We can add a feedback loop to improve the model over time

## The prompt
The prompt I used was:
```
    Use the following pieces of context to answer the question at the end.
    If you don't know the answer, don't try to make up an answer and just try to be helpful using the context provided.

    Context: {context}
    History: {history}
    Question: {question}
    Helpful Answer:
```

We can obviously tailor the prompt to be more specific to the CIC documents, but I think this is a good starting point for general use cases and minimises hallucinations.

## The model
I used llama3.2 as the model for this project. It was free, small (7B parameters) and easy to run locally. There are obviously more advanced models that could be used.