from langchain_google_genai import GoogleGenerativeAIEmbeddings
from sqlalchemy import create_engine
from sqlalchemy.orm import Session
from config import load_db_url
from crud.model import Info

engine = create_engine(load_db_url())


def find_related_info(query: str) -> dict:
    """
    Find related information based on the query provided.
    Args:
        query (str): The query to find related information for.
    Returns:
        dict: A dictionary containing the related information.
    Example:
    Input: What are the different safety training options available?
    Output:
    {
        "related_info": ["info1", "info2", "info3"]
    }
    """
    print("Finding related info for query: ", query)
    query_embedding = GoogleGenerativeAIEmbeddings(
        model="models/text-embedding-004"
    ).embed_query(query)
    with Session(engine) as session:
        k = 5
        similarity_threshold = 0.7
        query = (
            session.query(
                Info, Info.embedding.cosine_distance(query_embedding).label("distance")
            )
            .filter(
                Info.embedding.cosine_distance(query_embedding) < similarity_threshold
            )
            .order_by("distance")
            .limit(k)
            .all()
        )

        return {
            "related_info": [info[0].text for info in query],
        }


if __name__ == "__main__":
    info = find_related_info(
        "What are the different safety training options available?"
    )
    print(info)
