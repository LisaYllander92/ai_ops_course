import logfire
from logfire import VariablesOptions
from dotenv import load_dotenv
import os

# Läser in miljövariabler från .env-filen
load_dotenv()

# Konfigurerar Logfire med API-nyckel och stöd för variabler (promptar)
logfire.configure(api_key=os.environ["LOGFIRE_API"], variables=VariablesOptions())


# Hämtar en prompt från Logfire med given namn och version (label)
def get_prompt(
    name: str = "coach_agent_instructions",
    default: str = "jokey assistant",
    label: str = "latest",
):  
    # Definierar variabeln i Logfire; default används om den saknas
    prompt = logfire.var(name=f"prompt__{name}", type=str, default=default)
    # Tvingar fram en ny hämtning så att vi får senaste versionen
    prompt.refresh_sync(force=True)
    # Hämtar värdet för vald label (t.ex. "latest" eller "production")
    resolved = prompt.get(label=label)
    #print(resolved.label)
    return resolved.value

# Test: skriver ut produktionsversionen av prompten när filen körs direkt
if __name__ == "__main__":
    prompt = get_prompt(label="production")
    print(prompt)