from fastapi import FastAPI                         # FastAPI: ramverk för att bygga webb-API:er i Python
from chat_agent import chat                         # Funktionen som skickar frågan till AI-agenten
from data_models import ChatResponse, ChatRequest   # Datamodeller för inkommande och utgående data

app = FastAPI()  # Skapar själva API-applikationen (startas t.ex. med: uvicorn main:app --reload)

# get endpoint to pick out chat history





# Registrerar en POST-endpoint på adressen /chat (samma adress som Streamlit anropar).
# response_model gör att FastAPI validerar svaret och dokumenterar det i /docs.
@app.post("/chat", response_model=ChatResponse)
async def joke_chat(request: ChatRequest):
    # FastAPI läser automatiskt in JSON-bodyn och validerar den
    # mot ChatRequest (question + message_history) innan funktionen körs

    # Anropar chat-funktionen, som kör agenten mot LLM:en.
    # await eftersom LLM-anropet tar tid och körs asynkront
    chat_response = await chat(request)

    # Returnerar ChatResponse, som FastAPI omvandlar till JSON och skickar till klienten
    return chat_response