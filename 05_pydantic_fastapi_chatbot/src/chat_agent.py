from pydantic_ai import Agent               # Agent: Pydantic AI:s klass för att skapa en AI-agent kopplad till en LLM
from constants import MODEL                 # Vilken modell som används (t.ex. "openai:gpt-4o"), definierad i constants.py
from dotenv import load_dotenv              # Läser in miljövariabler från en .env-fil (t.ex. API-nycklar)
from data_models import ChatRequest, ChatResponse  # Datamodellerna för inkommande och utgående data

load_dotenv()  # Laddar .env så att API-nyckeln finns tillgänglig när agenten anropar modellen


# Skapar agenten som hanterar samtalet med LLM:en
chat_agent = Agent(
    MODEL,  # Modellen som ska användas
    # System prompt: instruktioner som styr botens personlighet och beteende
    # i hela samtalet (här: skämtsam programmerarnörd med emojis)
    system_prompt="Be a joking programming nerd, always answer with a programming joke. "
    "Also add in some emojis to make it funnier.",
)


async def chat(request: ChatRequest):
    # async eftersom anropet till LLM:en tar tid, och då kan servern
    # hantera andra förfrågningar medan den väntar på svar

    # Skickar användarens fråga till modellen tillsammans med tidigare
    # meddelanden, så att agenten har kontext från samtalet hittills
    result = await chat_agent.run(
        request.question, message_history=request.message_history
    )

    # Returnerar botens svar (result.output) samt hela den uppdaterade historiken
    # (result.all_messages()) som klienten sparar och skickar med nästa gång
    return ChatResponse(response=result.output, message_history=result.all_messages())