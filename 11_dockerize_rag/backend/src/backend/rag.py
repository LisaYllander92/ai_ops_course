from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from pydantic_ai.settings import ModelSettings
from dotenv import load_dotenv
import os
from backend.data_models import RagResponse
from backend.constants import VECTOR_DATABASE_PATH
from backend.model import nvidia_model
import lancedb

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

rag_agent = Agent(
    model=nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b"),
    retries=1,
    model_settings=ModelSettings(timeout=30, thinking="minimal"),
    system_prompt=(
        "You are an expert in rabbit races and knows how to distinguish between the rabbits",
        "Always answer based on the retrieved knowledge, but you can mix in your expertise to make the answer more coherent",
        "Don't hallucinate, rather say you can't answer it if the user prompts outside of the retrieved knowledge",
        "Make sure to keep the answer clear and concise, getting to the point directly, max 6 sentences",
        "Also describe which file you have used as source",
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int = 3) -> str:
    """
    Uses vector search to find closest k matching documents to the query
    """
    results = vector_db["articles"].search(query=query).limit(k).to_list()
    top_results = results[0]

    return f"""
    Filename: {top_results["filename"]},
    Filepath: {top_results["filepath"]},
    Content: {top_results["content"]}
    """
