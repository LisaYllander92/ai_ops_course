## Förra veckan - structured output
- testa bygga en ai-agent med två olika nvidia modeller
- testa prompta på olika sätt 
- hämta text/data från STI och strukturera den m.h.a agenten
- spara ner resultat i .csv

![Workflow build nvidia agent](images/agent_build_workflow.png)


## Arketektur 
![Architecture](images/back_to_frontend.png)


# Lektion 04/05 - Pydantic FastAPI Chatbot

*Kopiera fil till annan mapp:* 
```bash
cd <work_folder>
cp ../<folder_name>/<file_name>
```

### Skapa agenten med vald modell och testa agenten direkt i teminalen 
1. Skapa agenten och lägg till instructions
2. testa agenten direkt i terminalen
*i scriptet*
```python
movie = movie_agent.run_sync("meddelande till agenten")
```
*i terminalen*
```bash
uv run agent.py
```

- skapa BaseModel för putput formart och vad du vill ha med


- för att testa endpointen @app.get("/...")
```bash
uv runn uvicorn api:app --reload
```


# 05 chatbot

I lektion 04 gjorde vi så att vi kunde skcika in en fråga till ai-agenten - be om en film och få tillbaka ett svar - men den kom inte ihåg någonting och kunde inte svara. det ska vi göra nu.

1. Skapa agenten med en modell
- System_prompt = satt för eveigt
- instructions = kan ändras med tiden

2. Skapa minne för chatboten
- använd message_history = result.all_messages()
```python
result = await chat_agent.run("....", message_history = result.all_messages())
```

Skapa cha_agent med minne: (se *05 chat_agent.py*)
```python
async def chat(request: ChatRequest):
    result = await chat_agent.run(
        request.question, message_history=request.message_history
    )

    return ChatResponse(response=result.output, message_history=result.all_messages())
```

kommer från:
````python
class ChatRequest(BaseModel):
    question: str = Field(
        description="users message or question to JokeBot",
    )

    message_history: list[ModelMessage] = []

    model_config = {
        "json_schema_extra": {"example": {"question": "Tell me a joke about Python"}}
    }

class ChatResponse(BaseModel):
    response: str = Field(
        description="The JokeBot's response including a programming joke and emojis"
    )

    message_history: list[ModelMessage]
```

````python
from pydantic import BaseModel, Field 
from pydantic_ai import ModelMessage

class ChatRequest(BaseModel):
    question: str = Field(
        description="users message or question to JokeBot",  # Visas i den automatiska API-dokumentationen (/docs)
    )


    message_history: list[ModelMessage] = []

    model_config = {
        # Exempel som visas i den automatiskt genererade dokumentationen (Swagger/OpenAPI) - **här kam man lägga till fler frågor till användaren**
        "json_schema_extra": {"example": {"question": "Tell me a joke about Python"}}
    }


class ChatResponse(BaseModel):
    response: str = Field(
        description="The JokeBot's response including a programming joke and emojis"  # Botens textsvar
    )

    message_history: list[ModelMessage]

```