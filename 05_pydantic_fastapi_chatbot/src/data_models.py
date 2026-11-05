from pydantic import BaseModel, Field # BaseModel: grunden för datamodeller med validering. Field: lägger till metadata, t.ex. beskrivning
from pydantic_ai import ModelMessage # Pydantic AI:s typ för ett enskilt meddelande i en konversation med en AI-modell


class ChatRequest(BaseModel):
    # Beskriver datan som klienten (t.ex. Streamlit-appen) skickar TILL API:et.
    # FastAPI använder klassen för att validera inkommande JSON automatiskt.

    question: str = Field(
        description="users message or question to JokeBot",  # Visas i den automatiska API-dokumentationen (/docs)
    )

    # Tidigare meddelanden i samtalet. ModelMessage är Pydantic AI:s format för
    # både förfrågningar (användarens text, system prompt) och svar (modellens text, verktygsanrop).
    # Genom att skicka med historiken "minns" agenten vad som sagts tidigare,
    # eftersom själva API:et inte sparar något mellan anrop.
    # Tom lista som standard = ett nytt samtal.
    message_history: list[ModelMessage] = []

    model_config = {
        # Exempel som visas i den automatiskt genererade dokumentationen (Swagger/OpenAPI)
        "json_schema_extra": {"example": {"question": "Tell me a joke about Python"}}
    }


class ChatResponse(BaseModel):
    # Beskriver datan som API:et skickar TILLBAKA till klienten

    response: str = Field(
        description="The JokeBot's response including a programming joke and emojis"  # Botens textsvar
    )

    # Den uppdaterade historiken, inklusive det senaste frågan och svaret.
    # Klienten sparar den och skickar tillbaka den vid nästa fråga,
    # så att samtalet kan fortsätta med full kontext.
    message_history: list[ModelMessage]
