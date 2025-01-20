import os
from dotenv import dotenv_values

dotenv_config = dotenv_values(".env")


def load_db_url() -> str:
    db_url = os.getenv("DATABASE_URL", dotenv_config.get("DATABASE_URL"))
    if db_url is None:
        raise Exception("DATABASE_URL environment variable not set")
    os.environ["DATABASE_URL"] = db_url
    return db_url


def load_google_api_key() -> dict:
    api_key = os.getenv("GOOGLE_API_KEY", dotenv_config.get("GOOGLE_API_KEY"))
    if api_key is None:
        raise Exception("GOOGLE_API_KEY environment variable not set")
    return {"api_key": api_key}


def get_gemini_model() -> str:
    environment_model = os.getenv("MODEL", dotenv_config.get("MODEL"))
    if environment_model is None:
        raise Exception("MODEL environment variable not set")
    return environment_model


def get_datasource_dir() -> str:
    datasource_dir = os.getenv("DATASOURCE_DIR", dotenv_config.get("DATASOURCE_DIR"))
    if datasource_dir is None:
        raise Exception("DATASOURCE_DIR environment variable not set")
    return datasource_dir
