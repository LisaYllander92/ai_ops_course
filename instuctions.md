# Setup: NVIDIA + Pydantic AI

## 1. Initiera projektet

```bash
uv init --no-package --python 3.13
```

## 2. Skapa konto och API-nyckel hos NVIDIA

1. Skapa ett konto på NVIDIA (build.nvidia.com).
2. Skapa en API-nyckel. Du kan döpa om nyckeln när du skapar den, vilket är bra om du har flera nycklar.
3. Kopiera nyckeln till en `.env`-fil i projektets rotmapp:

```env
NVIDIA_API=nvapi-xxxxxxxxxxxxxxxx
```

> Lägg till `.env` i `.gitignore` så att nyckeln inte hamnar på GitHub.

## 3. Installera dependencies

```bash
uv add pandas pydantic-ai ipykernel
```

## 4. Testa i notebook (`.ipynb`)

### Cell 1: Importer och modellkonfiguration

```python
import os

from dotenv import load_dotenv
from pydantic_ai import Agent
from pydantic_ai.models.openai import OpenAIChatModel  # NVIDIA finns inte som egen modell i pydantic_ai
from pydantic_ai.providers.openai import OpenAIProvider  # NVIDIA har ett OpenAI-kompatibelt API

# Läs in miljövariabler från .env (t.ex. NVIDIA_API) så att nyckeln inte hårdkodas i koden
load_dotenv()

# Skapa en modell som pratar med NVIDIA:s OpenAI-kompatibla endpoint
model = OpenAIChatModel(
    # Hämta modellnamnet från NVIDIA: Models -> välj modell -> kopiera namnet
    model_name="nvidia/nemotron-3.5-lightning-30b-a3b",
    provider=OpenAIProvider(
        base_url="https://integrate.api.nvidia.com/v1",  # NVIDIA:s API-adress
        api_key=os.environ["NVIDIA_API"],  # API-nyckeln från .env (kraschar tydligt om den saknas)
    ),
)

model  # Visar modellobjektet i notebooken för att bekräfta att allt är korrekt konfigurerat
```

### Cell 2: Skapa agent och kör ett test

```python
# Skapa en agent som använder NVIDIA-modellen
agent = Agent(model)

# Kör agenten asynkront (notebooks stödjer top-level await)
result = await agent.run("Give me a funny python joke", timeout=60)

# Visar hela resultatobjektet (inkl. output, usage m.m.)
result
```

### Cell 3 (valfri): Visa bara svaret

```python
# Skriver ut enbart modellens textsvar, utan extra metadata
print(result.output)
```

# LLM intro

Nu när modellen är konfigurerad (se `nvidia-pydantic-ai-setup.md`) kan vi ge agenten en personlighet med en **system prompt**.

## Agent med system prompt

```python
# Skapa en agent med NVIDIA-modellen från tidigare setup
# system_prompt styr hur modellen beter sig i alla svar (roll, ton, format)
agent = Agent(
    model=model,
    system_prompt=(
        "You are funny joking bot, "       # Rollen: en rolig bot
        "answer shortly in a nerdy style, " # Stilen: kort och nördig
        "also add emojis"                   # Formatet: lägg till emojis
    ),
)

# Användarens fråga (user prompt), det vi faktiskt vill ha svar på
prompt = "Explain what PydanticAI is and the difference between it and Pydantic"

# Kör agenten asynkront (notebooks stödjer top-level await)
result = await agent.run(prompt)

# Skriver ut enbart modellens textsvar, utan extra metadata
print(result.output)
```

## Vad händer här?

- **System prompt**: instruktioner som gäller under hela konversationen och styr modellens beteende.
- **User prompt**: själva frågan som skickas in vid varje `agent.run()`.
- **`result.output`**: modellens svar som text.

