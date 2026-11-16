# Dockerize Full-Stack RAG-app + Logfire-övervakning

Sammanfattning av lektionen "Dockerize a Full-Stack RAG App (PydanticAI + FastAPI + Streamlit) with Logfire Monitoring" (Kokchun Coding Tutorials). Bygger vidare på föregående lektion (RAG-appen).

> Källa: videons beskrivning och kapitel, kompletterat med mitt eget bygge. Logfire-delen är skriven från allmän kunskap om biblioteket och bör jämföras med videon.

## Mål

Ta den färdiga RAG-appen och:
1. dela upp den i två paket (backend/frontend) med **uv workspaces**,
2. lägga till **Logfire** för att spåra anrop, spans och kostnad,
3. köra båda delarna i **Docker-containrar** med **docker compose**.

I videon byts även LLM till NVIDIA Build och embeddings till Cohere (multilingual). Det är bara modellval, själva strukturen är densamma.

## Steg för steg

### 1. uv workspaces
Ett rotprojekt med två medlemmar, så att varje del har egna beroenden och kan paketeras i egen container.

```
project/
  pyproject.toml        # [tool.uv.workspace] members = ["backend", "frontend"]
  backend/              # eget pyproject.toml (fastapi, pydantic-ai, lancedb ...)
  frontend/             # eget pyproject.toml (streamlit, requests)
  data/  assets/  dockerfiles/  docker-compose.yml
```

Varför: containrarna blir mindre och byggs snabbare när frontend inte drar med backendens tunga beroenden.

### 2. Flytta in kod och data
Kopiera backend-koden, `data/` och ingestion. Konvertera PDF till text och kör ingestion till LanceDB igen (`uv run ingestion.py`). Verifiera att `/rag/query` svarar på `/docs` innan något annat läggs till.

### 3. Logfire (övervakning)
Logfire visar varje request, varje LLM-anrop, verktygsanrop och kostnad i en live-dashboard.

```python
import logfire
logfire.configure()
logfire.instrument_pydantic_ai()   # spårar agent, verktyg och modellanrop
logfire.instrument_fastapi(app)    # spårar HTTP-anrop till API:t
```

- Kräver ett Logfire-konto och en token i `.env` (`LOGFIRE_TOKEN`).
- Varför: man ser vad agenten faktiskt gjorde (vilket verktyg, vilken fråga, hur lång tid, vad det kostade) vilket är svårt att se i vanliga loggar.

### 4. Koppla frontend till API
Läs bas-URL från en miljövariabel så att samma kod fungerar lokalt och i Docker:

```python
BASE_URL = os.getenv("API_URL", default="http://127.0.0.1:8000")
requests.post(f"{BASE_URL}/rag/query", json={"prompt": text_input})
```

Fixa även sökvägen till `assets/` (`Path(__file__).parents[1] / "assets"`) så att bilderna hittas.

### 5. Dockerfiler (`dockerfiles/backend.dockerfile`, `frontend.dockerfile`)
Mönster för båda:

```dockerfile
FROM python:3.13-slim
WORKDIR /app/
COPY backend backend            # frontend: COPY frontend frontend
RUN pip install --no-cache-dir uv
WORKDIR /app/backend/src/backend
RUN uv sync --no-dev --no-install-project
CMD ["uv", "run", "--no-sync", "uvicorn", "api:app", "--host", "0.0.0.0", "--port", "8000"]
```

Frontend-CMD:
```dockerfile
CMD ["uv", "run", "--no-sync", "streamlit", "run", "app.py", "--server.address=0.0.0.0", "--server.port=8501"]
```

Varför:
- `python:3.13-slim` ger en liten image.
- `--no-dev` hoppar över utvecklingsberoenden.
- `--no-install-project` installerar bara beroenden, så README m.m. behövs inte.
- `--no-sync` gör att `uv run` inte försöker bygga om projektet vid start.
- `0.0.0.0` krävs, annars når man inte tjänsten utanför containern.

### 6. docker compose
```yaml
services:
  backend:
    build: { context: ., dockerfile: dockerfiles/backend.dockerfile }
    ports: ["8000:8000"]
    env_file: [../.env]            # API-nycklar (justera sökväg efter var .env ligger)
    image: backend:v1

  frontend:
    build: { context: ., dockerfile: dockerfiles/frontend.dockerfile }
    ports: ["8501:8501"]
    environment:
      - API_URL=http://backend:8000   # tjänstenamnet, inte 127.0.0.1
    depends_on: [backend]
    image: frontend:v1
```

Varför:
- Containrar når varandra via **tjänstenamn** (`backend`), `127.0.0.1` pekar på containern själv.
- `env_file` läser en fil med nycklar, `environment` sätter enskilda variabler.

### 7. `.dockerignore`
Håll imagen liten och säker: ignorera `.venv`, `__pycache__`, `.git`, `.env`.
Se upp så att du inte ignorerar filer som bygget behöver (t.ex. `README.md` om projektet byggs).

### 8. Bygg och kör
```bash
docker compose up -d --build
docker compose logs backend
docker compose logs frontend
```
Frontend: `http://localhost:8501`, API-docs: `http://localhost:8000/docs`.
Stäng ner: `docker compose down`.

## Fallgropar jag stötte på

| Problem | Lösning |
|---|---|
| `env file .env not found` | `env_file` är relativ till compose-filen. Använd `../.env` om den ligger en nivå upp |
| `envionment` (stavfel) | Rätt nyckel är `environment` |
| `pull access denied for frontend/backend` | Ofarlig varning, compose bygger imagen lokalt |
| `failed to open /app/frontend/README.md` | README i `.dockerignore` men projektet byggs. Använd `--no-install-project` eller ta bort raden |
| Streamlit nås inte | Stavfel `--server.adress`, ska vara `--server.address=0.0.0.0` |
| Frontend får connection refused | `API_URL` saknas, `127.0.0.1` används i stället för `http://backend:8000` |
| Bilder saknas i containern | Kopiera in `assets/` och kontrollera att sökvägen stämmer med mappstrukturen i imagen |
| `.env` med nycklar | Aldrig in i git eller imagen (`.gitignore` + `.dockerignore`) |

## Checklista inför nytt projekt
- [ ] Workspace med separata backend/frontend-paket
- [ ] `.env` utanför git, `.env.example` med nyckelnamn
- [ ] `API_URL` via miljövariabel
- [ ] `0.0.0.0` på alla servrar i containrar
- [ ] Logfire-token satt och instrumentering på plats
- [ ] Testat med `docker compose up -d --build` från ren miljö