from fastapi import FastAPI
from dotenv import load_dotenv
from setup_db import query_duckdb
from data_models import Movie, Prompt
from agent import movie_agent

load_dotenv()

app = FastAPI()


# Endpoint
@app.get("/movies")
async def read_movies(genre: str | None = None):
    if genre:
        sql = "SELECT * FROM movies WHERE genre = ?;"
        params = [genre]
    else:
        sql = "FROM movies;"
        params = None

    movies = query_duckdb(sql, parameters=params)
    return movies.to_dict(orient="records")


@app.post("/movie")
async def create_movie(query: Prompt):
    result = await movie_agent.run(query.prompt, output_type=Movie)
    movie = result.output
    # protect against SQL injection
    query_duckdb(
        "INSERT INTO movies VALUES (?,?,?,?,?)",
        parameters=[movie.title, movie.year, movie.genre, movie.rating, movie.summary],
    )
    return movie
