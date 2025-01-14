# RAG Chatbot
## Overview
This is a basic chatbot that is designed to let you speak to a provided set of documents of a similar topic or theme, in our case some PDFs and HTML pages. 

## Prerequisites
You will need the following prerequisites to run this project:
- Python 3.10 or higher installed on your machine
- For this project I used Google's Gemini as the llm of choice (using the `gemini-1.5-flash` model)
  - To run this project, you will need to obtain your own API key from Google's AI Platform and set it as an environment variable called `GOOGLE_API_KEY` - which can be downloaded [here](https://aistudio.google.com/app/apikey)
- You will also need to setup a local database of your choice, one that is supported by SQLAlchemy. I used `postgresql` for this project. You can set your database URL as an environment variable called `DATABASE_URL`.Please make sure its following the format `postgresql+psycopg://user:password@host:port/dbname[?key=value&key=value...]` eg. postgresql+psycopg://localhost/ragchat

## How to run the project
- If you want to not make any changes and just run the chatbot, you can first install the requirements by running:
  ```pip install -r requirements.txt``` (you may have to use `pip3` instead of `pip` depending on your setup).
    - I recommend using a virtual environment to install the requirements. (see [here](https://docs.python.org/3/library/venv.html) for more information on how to set up a virtual environment).
- Duplicate the `.env.example` file and rename it to `.env` and fill in the required environment variables.
- You can then run the `create_vector_store` script to generate the embeddings for the documents in the `data_sources` folder by running:
  ```python -m create_vector_store``` in the root of the project.
    - This will create a new table in your database called `info` and populate it with the embeddings for the documents in the `data_sources` folder.
- Then you can run the chatbot by running (in the root directory of the repo):
  ```streamlit run app.py```
- This will open a new tab in your browser with the chatbot. You can start chatting with it by typing in the text box at the bottom of the screen.
  - (if you can't see it in the browser, you can try going to the following link: http://localhost:8501)

## How to add more data sources
- The simplest way to add more data sources is to add more documents to the `data_sources` folder, clear your database and run the `create_vector_store` script again.
    ```python -m create_vector_store``` in the root of the project.


Formatted using [ruff](https://docs.astral.sh/ruff/)


# Approach
- The approach I took was to use the Gemini model to generate embeddings for the documents in the data_sources folder. 
- The magic lies in the chunking of the data source where instead of just splitting up the documents by number of characters, we use *Semantic Chunking* to split the documents into chunks that are semantically meaningful. This allows the model to generate embeddings that are more representative of the document as a whole, whilst ensuring that similar pieces of text are close together in the embedding space.
  - We also use the breakpoint_threshold_type of "gradient" given alot of the data source is actually relating to the same topic, this allows us to effectively differentiate between the different pieces of knowledge.
- I then used these embeddings to find the most similar documents to the user's query (in our case up to the 5 closest texts). We do this via a tool call that runs a cosine similarity between the user's query and the embeddings of the text chunks, returning the chunks to the LLM. 

## The prompt
The prompt I used was:
```
You are a chatbot dedicated to providing information about anything that the user asks.
To answer the user's questions, you MUST use the tools provided to you.

If you aren't able to answer the user's question using the provided tool, you should let the user know that you don't have the information.

```

We can obviously tailor the prompt to be more specific to your given topic, but I think this is a good starting point for general use cases and minimal hallucinations.

## The model
I used `gemini-1.5-flash` as the model for this project. You can change to any other model that you have access to by changing the `MODEL_NAME` in the environment variables.