from fastapi import FastAPI
from pydantic_ai import Agent
from dotenv import load_dotenv
from utils import query_duckdb
from data_models import Movie, Prompt
from agent import movie_agent

load_dotenv()

app = FastAPI()

# Endpoint
@app.get("/movies")
async def read_movies():
    movies = query_duckdb("FROM movies;")
    return movies.to_dict(orient="records")


@app.post("/movie")
async def create_movie(query: Prompt):
    result = await movie_agent.run(query.prompt, output_type=Movie)
    movie = result.output

    # protect against SQL injection
    query_duckdb(
        "INSERT INTO movies VALUES (?,?,?,?)",
        parameters=[movie.title, movie.year, movie.genre, movie.rating],
    )

    return movie