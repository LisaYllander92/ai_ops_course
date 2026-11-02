# PydanticAI + FastAPI + DuckDB: sammanfattning

Mål: en AI-agent som genererar filminfo från en prompt, sparar den i DuckDB och exponerar det hela som ett REST API.

```
Prompt → FastAPI → PydanticAI-agent (NVIDIA-modell) → Movie-objekt → DuckDB → JSON
```

Alla kommandon körs från mappen `04_pydantic_fastapi/src`.

---

## Filer och vad de gör

### `.env` (i kursens rot)

Håller API-nyckeln till modellen. Ska inte committas (lägg i `.gitignore`).

```
NVIDIA_API=din-nyckel
```

### `utils.py`

Hjälpfunktionen `query_duckdb(query, parameters=...)` som:

- öppnar `data/movies.duckdb`
- kör en SQL-fråga
- returnerar resultatet som DataFrame

`DATA_PATH` pekar på mappen `data/`, som måste finnas innan databasen skapas.

### `setup_db.py`

Engångsskript som skapar tabellen `movies`:

```sql
CREATE TABLE IF NOT EXISTS movies (
    title VARCHAR,
    year INTEGER,
    genre VARCHAR,
    rating INTEGER
);
```

Kolumnerna ska matcha fälten i `Movie`, i samma ordning.

### `data_models.py`

Pydantic-modeller för in- och utdata:

```python
from pydantic import BaseModel, Field

class Movie(BaseModel):
    title: str
    year: int
    genre: str
    rating: int = Field(gt=0, lt=6)   # betyg 1-5

class Prompt(BaseModel):
    prompt: str
```

- `Prompt`: vad användaren skickar in.
- `Movie`: strukturen som LLM:en tvingas svara med. Validering (t.ex. betyg 1-5) sker automatiskt.

### `model.py`

Gör modellen till en återanvändbar funktion (NVIDIA har ett OpenAI-kompatibelt API):

```python
import os
from dotenv import load_dotenv
from pydantic_ai.models.openai import OpenAIChatModel
from pydantic_ai.providers.openai import OpenAIProvider

load_dotenv()

def nvidia_model(model_name: str) -> OpenAIChatModel:
    return OpenAIChatModel(
        model_name=model_name,
        provider=OpenAIProvider(
            base_url="https://integrate.api.nvidia.com/v1",
            api_key=os.environ["NVIDIA_API"],
        ),
    )
```

### `movies_api.py`

FastAPI-appen med agenten och två endpoints:

```python
from fastapi import FastAPI
from pydantic_ai import Agent
from utils import query_duckdb
from data_models import Movie, Prompt
from model import nvidia_model

app = FastAPI()

agent = Agent(model=nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b"))


@app.get("/movies")
async def read_movies():
    movies = query_duckdb("FROM movies;")
    return movies.to_dict(orient="records")


@app.post("/movie")
async def create_movie(query: Prompt):
    result = await agent.run(query.prompt, output_type=Movie)
    movie = result.output

    query_duckdb(
        "INSERT INTO movies VALUES (?,?,?,?)",
        parameters=[movie.title, movie.year, movie.genre, movie.rating],
    )
    return movie
```

- `GET /movies`: hämtar alla filmer från databasen.
- `POST /movie`: skickar prompten till agenten, får tillbaka ett validerat `Movie`, sparar i databasen och returnerar det.
- `?`-parametrarna i `INSERT` skyddar mot SQL injection.

---

## Kommandon

| Kommando | Vad det gör |
|---|---|
| `mkdir -p data` | Skapar mappen där databasfilen ligger |
| `uv run setup_db.py` | Skapar databasen och tabellen `movies` (körs en gång) |
| `uv run uvicorn movies_api:app --reload` | Startar API-servern, laddar om vid filändringar |
| `uv run python -c "import duckdb; print(duckdb.connect('data/movies.duckdb').sql('FROM movies').df())"` | Visar innehållet i tabellen |
| `uv run duckdb -ui data/movies.duckdb` | Öppnar databasen i DuckDB:s webb-UI (kräver att CLI-versionen är minst lika ny som Python-paketet) |

**Testa API:t:** öppna http://127.0.0.1:8000/docs, välj `POST /movie` och skicka till exempel:

```json
{ "prompt": "Generate a sci-fi movie about AI and space exploration" }
```

Kontrollera sedan resultatet med `GET /movies`.

---

## Arbetsordning

1. Lägg API-nyckeln i `.env`.
2. Skapa `data/`-mappen och skriv `utils.py`.
3. Skriv och kör `setup_db.py` för att skapa tabellen.
4. Skriv `data_models.py` (`Movie`, `Prompt`).
5. Skriv `model.py` (`nvidia_model`).
6. Skriv `movies_api.py` (agent + endpoints).
7. Starta servern med uvicorn och testa i `/docs`.