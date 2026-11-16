# Fullstack RAG: PydanticAI + FastAPI + LanceDB + Streamlit

Sammanfattning av lektionen "Fullstack RAG Application part 1 - Building" (Kokchun Coding Tutorials), kompletterat med erfarenheter från mitt eget projekt (kaninraser).

> Källa: videons beskrivning och kapitel. Detaljer är kompletterade från eget bygge.

## Vad är RAG och varför?

**Retrieval-Augmented Generation**: i stället för att LLM:en svarar från minnet hämtar vi först relevanta dokument ur en databas och låter modellen svara utifrån dem.
Fördelar: färre hallucinationer, svar baserade på egen data, källhänvisning.

## Arkitektur

```
Streamlit (frontend) -> FastAPI (API) -> PydanticAI-agent -> LanceDB (vektorsök)
                                              |
                                          LLM (Gemini/NVIDIA)
```

| Del | Uppgift |
|---|---|
| **LanceDB** | Vektordatabas, lagrar texter + embeddings |
| **PydanticAI** | Agent med verktyg (`retrieve_top_documents`) och typad output |
| **FastAPI** | Exponerar agenten som endpoint `POST /rag/query` |
| **Streamlit** | Enkelt UI för frågor och svar |

## Steg för steg

### 1. Miljö (`uv`)
```bash
uv add lancedb pydantic-ai fastapi uvicorn streamlit python-dotenv requests
```
- API-nycklar i `.env`, laddas med `load_dotenv()`.
- Mappar: `backend/` (logik), `frontend/` (Streamlit), `data/` (texter), `assets/` (bilder).

### 2. Konvertera PDF till text
Kunskapsbasen görs om från PDF till `.txt` i `data/`. Text är lättare att embedda och söka i.

### 3. Datamodeller (`backend/data_models.py`)
- `Article(LanceModel)`: `doc_id`, `filepath`, `filename`, `content` (källfält för embedding) och `embedding` (vektor).
- `Prompt`: användarens fråga.
- `RagResponse`: `filename`, `filepath`, `answer` (agentens strukturerade svar).

```python
embedding_model = get_registry().get("gemini-text").create(name="gemini-embedding-001")
EMBEDDING_DIM = 768  # måste matcha vad funktionen faktiskt returnerar

class Article(LanceModel):
    content: str = embedding_model.SourceField()
    embedding: Vector(EMBEDDING_DIM) = embedding_model.VectorField()
```

### 4. Ingestion (`ingestion.py`)
1. Anslut: `lancedb.connect(uri=VECTOR_DATABASE_PATH)`.
2. Skapa tabell: `create_table("articles", schema=Article)`.
3. Loopa över `data/*.txt`, ta bort gammal rad med samma `doc_id`, lägg till ny.
4. LanceDB skapar embeddings automatiskt via schemats `SourceField`.
5. `time.sleep(...)` mellan anrop för att inte nå API:ets rate limit.

Körs en gång (eller när datan ändras): `uv run ingestion.py`.

### 5. RAG-agent (`backend/rag.py`)
- Agent med `system_prompt` (roll, "svara bara utifrån hämtad kunskap", kort svar, ange källfil).
- `output_type=RagResponse` ger strukturerat svar.
- Verktyg som agenten själv väljer att anropa:

```python
@rag_agent.tool_plain
def retrieve_top_documents(query: str, k: int = 3) -> str:
    """Vector search for closest matching documents"""
    results = vector_db["articles"].search(query=query).limit(k).to_list()
    ...
```

### 6. API (`api.py`)
```python
@app.post("/rag/query")
async def query_documentation(query: Prompt):
    result = await rag_agent.run(query.prompt)
    return result.output
```
Start: `uv run uvicorn api:app --reload`, testa på `/docs`.

### 7. Frontend (`frontend/app.py`)
Textfält + knapp, `requests.post` mot API:t, visa fråga, svar, källa och bild från `assets/<filename>.png`.
Start: `uv run streamlit run frontend/app.py`.

## Fallgropar jag stötte på

| Problem | Orsak / lösning |
|---|---|
| `KeyError` på embedding-namn | Egen embedding-klass måste vara registrerad (dekoratorn körd) innan `get(...)` |
| `expected 4096 but got 768` | Tabellens schema gammalt eller `EMBEDDING_DIM` fel. Droppa tabellen, sätt rätt dimension |
| `Provided schema does not match existing table` | `exist_ok=True` skriver inte över. Använd `drop_table` en gång |
| `Unknown model: google-gla:` | Använd `google:<modell>` i nya pydantic-ai |
| 404 modell borta / 503 hög belastning | Byt modellnamn / försök igen senare |
| `'<=' not supported between str and int` | Verktygsparameter utan typ (`k=3`). Skriv `k: int = 3` |
| `KeyError: 'answer'` | Stavfel i `RagResponse` (`answe`). Skriv ut `response.text` för att felsöka |
| Bild kraschar | Filen saknas eller `filename` innehåller flera namn. Kolla `Path.exists()` |

## Bonus: Dockerize (nästa lektion)

- `backend.dockerfile` och `frontend.dockerfile` (python-slim + `uv`), kör `uv sync --no-dev --no-install-project`.
- `docker-compose.yml`: två tjänster, `env_file: ../.env` för backend, `environment: API_URL=http://backend:8000` för frontend.
- Frontend läser URL från miljö: `BASE_URL = os.getenv("API_URL", "http://127.0.0.1:8000")`.
- Containrar når varandra via tjänstenamn, inte `127.0.0.1`.
- Uvicorn/Streamlit måste lyssna på `0.0.0.0`.
- `.env` ska aldrig in i git eller imagen (`.gitignore` + `.dockerignore`).
- Bygg och kör: `docker compose up -d --build`, felsök med `docker compose logs <tjänst>`.

## Nästa steg i kursen
Deploya FastAPI-appen med Azure Functions.