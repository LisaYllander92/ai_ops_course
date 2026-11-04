from pydantic import BaseModel, Field
from typing import Literal

# How we want the agent to answer = output format
class Movie(BaseModel):
    title: str = Field(description="Title of the movie")
    year: int = Field(description="Year when this movie came out")
    # use Literal to allow only theese options
    genre: Literal["action", "comedy", "romance", "cartoon", "adventure", "thiller"] = Field(description="main genre, choose the one that is most charateristic for the movie")
    rating: int = Field(gt=0, lt=6) # or Field(instructions="give a rating between 1-5... ")
    summary: str = Field(description="short exiting summary of the movie, max 3 sentences")


class Prompt(BaseModel):
    prompt: str