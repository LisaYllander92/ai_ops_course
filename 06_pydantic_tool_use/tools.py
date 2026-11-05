import httpx                           # HTTP-klient för att anropa väder-API:erna
from pydantic_ai import RunContext     # Ger verktyget tillgång till kontext (deps) från agenten
from deps import WeatherDeps           # Din egen klass med data som skickas in till agenten (t.ex. city)

def get_weather(ctx: RunContext[WeatherDeps], lat:float, lon:float) -> str:
    """get current weather for longitude and latitude"""
    # Docstringen skickas till modellen så den vet vad verktyget gör.
    # lat och lon fyller modellen själv i när den anropar verktyget.

    # Hämtar aktuell temperatur från Open-Meteo för en given plats
    response = httpx.get("https://api.open-meteo.com/v1/forecast",
    params={"latitude": lat, "longitude": lon, "current": "temperature_2m"},  # "current" anger vilken data vi vill ha
    timeout=30,  # Väntar max 30 sekunder på svar
    )
    response.raise_for_status()  # Kastar ett fel om API:et svarar med t.ex. 400 eller 500

    current = response.json().get("current")             # Plockar ut blocket med aktuell väderdata
    temparature = current.get("temparature_2m")          # Plockar ut temperaturen (se felet nedan)

    # ctx.deps är den WeatherDeps som skickades in när agenten kördes,
    # här används den för att visa vilken stad det gäller
    return f"Current temperature in {ctx.deps.city} is {temparature}°C"


def geocode(city: str) -> dict:
    # Omvandlar ett stadsnamn till koordinater (latitud/longitud)
    response = httpx.get(
        "https://geocoding-api.open-meteo.com/v1/search",
        params={"name": city, "count": 1},  # Söker efter staden och tar bara bästa träffen
    )    
    response.raise_for_status()                           # Kastar fel vid misslyckat anrop
    place = response.json().get("results")[0]             # Första (bästa) träffen i resultatlistan
    return {"latitude": place.get("latitude"), "longitude": place.get("longitude")}  # Returnerar bara koordinaterna
    

#get_weather(WeatherDeps(city="London"), 20,30)   # Manuellt test av väderfunktionen
#geocode("gothenburg")                            # Manuellt test av geokodningen