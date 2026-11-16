from pydantic import BaseModel, Field
from lancedb.embeddings import get_registry
from lancedb.pydantic import LanceModel, Vector
from dotenv import load_dotenv

load_dotenv()

embedding_model = get_registry().get("cohere").create(name="embed-multilingual-v3.0")


class Article(LanceModel):
    doc_id: str 
    filepath: str
    filename: str = Field(description="the stem of the file i.e. without the suffix")
    content: str = embedding_model.SourceField()
    embedding: Vector(embedding_model.ndims()) = embedding_model.VectorField()


class Prompt(BaseModel):
    prompt: str = Field(description="prompt from user, if empty consider it as missing")

class RagResponse(BaseModel):
    filename: str = Field(description="filename of retrived file without siffix")
    filepath: str = Field(description="absolute path to the retrived file")
    answer: str = Field(description="answer based on the retrived file")