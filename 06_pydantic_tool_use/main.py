from agents import weather_agent    # Den färdiga agenten (definierad i agents.py) med väderverktygen kopplade
import asyncio                      # Pythons bibliotek för asynkron kod, behövs för att köra async-funktioner
from tools import WeatherDeps       # Deps-klassen med stadsnamn (importeras här via tools.py)

async def main(prompt, **kwargs):
    # **kwargs tar emot extra argument (här: deps) och skickar vidare till agenten,
    # så samma funktion kan återanvändas med olika inställningar

    # Kör agenten med frågan. await eftersom LLM-anropet och verktygsanropen tar tid
    result = await weather_agent.run(prompt, **kwargs)
    print(result.output)  # Skriver ut agentens slutliga svar i terminalen

if __name__ == "__main__":
    # Körs bara när filen startas direkt (t.ex. med: uv run main.py)

    # asyncio.run startar en händelseloop och kör main till den är klar.
    # deps skickar in staden till verktygen via RunContext (ctx.deps.city)
    asyncio.run(main("What is the weather in Skövde?", deps = WeatherDeps(city="Skövde")))
    asyncio.run(main("What is the weather in London?", deps = WeatherDeps(city="London")))
#    asyncio.run(main("Give me a fun joke about London?", deps = WeatherDeps(city="London")))  # Avstängt testanrop, utan väder