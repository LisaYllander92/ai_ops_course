from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider
from dotenv import load_dotenv
import os
from backend.data_models import RagResponse
from backend.constants import VECTOR_DATABASE_PATH
import lancedb

load_dotenv()

vector_db = lancedb.connect(uri=VECTOR_DATABASE_PATH)

model=OpenAIChatModel(
    "nvidia/nemotron-3.5-super-vl-120b-a12b",
    provider=OpenAIProvider(
        base_url="https://integrate.api.nvidia.com/v1", api_key=os.environ["NVIDIA_API"],
    ),
)

rag_agent = Agent(model=model, retries=2, system_prompt=(
        "You are an expert in rabbit races and knows how to distinguish between the rabbits",
        "Always answer based on the retrieved knowledge, but you can mix in your expertise to make the answer more coherent",
        "Don't hallucinate, rather say you can't answer it if the user prompts outside of the retrieved knowledge",
        "Make sure to keep the answer clear and concise, getting to the point directly, max 6 sentences",
        "Also describe which file you have used as source",
    ),
    output_type=RagResponse,
)


@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int=3) -> str:
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