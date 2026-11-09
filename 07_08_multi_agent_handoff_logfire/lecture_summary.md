# Multi-Agent Architecture & Observability (Pydantic AI + Logfire)

**Källor:** 
- Part 1: [PydanticAI MultiAgent Handoff](https://youtu.be/U-PB-dvvEp4) – Kokchun Coding Tutorials
- Part 2: [Pydantic Logfire + PydanticAI](https://www.youtube.com/watch?v=hG-jJy2o5Ok) – Kokchun Coding Tutorials

---

## 1. Översikt & Arkitektur

Ett modulärt multi-agent-system byggt med **Pydantic AI** och övervakat via **Pydantic Logfire**. 

* **Orkestrering:** En huvudagent (`coach_agent`) tar emot förfrågningar och delegerar deluppgifter via verktyg (tools) till specialister.
* **Specialister:** Exempelvis `study_agent` (studieplanering) och `career_agent` (karriärsrådgivning).
* **Exporter:** Ett verktyg (`export_report`) sparar det kombinerade svaret till en tidsstämplad Markdown-fil.
* **Observability & Prompt Management:** Logfire spårar agenternas anrop (traces/spans), token-förbrukning samt hanterar versionshanterade systemprompter.

```
Användare ──► coach_agent ──┬──► study_agent (Tool)
                           ├──► career_agent (Tool)
                           └──► export_report (Tool)
                                     │
                             [ Logfire Observability ]
```

---

## 2. Installations- och Miljöuppsättning

### Beroenden via `uv`
Skapa projekt och installera nödvändiga paket:

```bash
uv init --no-package -p 3.13
uv add pydantic-ai logfire logfire-system-metrics logfire-variables python-dotenv
```

### Autentisering & Konfigurering av Logfire
1. **Autentisera CLI:**
   ```bash
   uv run logfire auth
   ```
   *(Välj EU/US-region och slutför i webbläsaren)*

2. **Miljövariabler (`.env`):**
   ```env
   LOGFIRE_API_KEY=dina_logfire_read_write_keys
   ```

---

## 3. Kodstruktur & Implementering

### A. Aktivera Logfire i koden (`main.py`)
Lägg till instrumentering innan agenterna körs:

```python
import logfire

# Konfigurera och aktivera spårning
logfire.configure()
logfire.instrument_system_metrics()
logfire.instrument_pydantic_ai()  # Fångar alla Pydantic AI-agenter och verktygsanrop
```

### B. Klientberoenden (Dependency Injection)
Skicka med delat tillstånd till agenterna så att svaren anpassas:

```python
from dataclasses import dataclass

@dataclass
class ClientDeps:
    name: str
    goal: str
    experience_level: str
    hours_per_week: int
    current_role: str
```

### C. Verktyg för Delegering (Multi-Agent Handoff)
För att en agent ska kunna anropa en annan paketeras underagenten i en funktion som registreras som ett `tool` på huvudagenten:

```python
from pydantic_ai import RunContext

@coach_agent.tool
async def ask_study_agent(ctx: RunContext[ClientDeps], question: str) -> str:
    """Delegerar studiefrågor till studieexperten."""
    result = await study_agent.run(question, deps=ctx.deps)
    return result.data
```

### D. Export-verktyg med säker filkodning
För att undvika `UnicodeEncodeError` på Windows (t.ex. vid tecken som `→` eller `—`), ange alltid `utf-8` explicit:

```python
from pathlib import Path

@coach_agent.tool
def export_report(ctx: RunContext[ClientDeps], text: str) -> str:
    """Sparar det slutgiltiga svaret till en Markdown-fil."""
    path = Path(f"report_{ctx.deps.name}.md")
    path.write_text(text, encoding="utf-8")  # <--- Viktigt för Windows!
    return f"Rapport sparad till {path}"
```

---

## 4. Prompt Management med Logfire (`prompts.py`)

Logfire gör det möjligt att flytta systemprompter utanför källkoden till Logfires webbgränssnitt för versionering och taggning (t.ex. `dev` vs `production`).

```python
import os
import logfire
from dotenv import load_dotenv

load_dotenv()

logfire.configure(api_key=os.environ.get("LOGFIRE_API_KEY"))

def get_prompt(name: str, default: str = "Fallback prompt", label: str = "production") -> str:
    """Hämtar en versionshanterad prompt från Logfire."""
    prompt_var = logfire.var(
        name=name,
        type=str,
        default=default
    )
    prompt_var.refresh_sync(force=True)
    resolved = prompt_var.get(label=label)
    return resolved.value
```

**Användning i agentfilen:**
```python
coach_instructions = get_prompt("coach_agent_instructions", label="production")
coach_agent = Agent('openai:nvidia/nemotron-...', system_prompt=coach_instructions)
```

---

## 5. Övervakning & Felsökning i Logfire Dashboard

När applikationen körs (`uv run main.py`) skickas data live till Logfire:

1. **Traces & Spans:** Visualiserar exakt vilket verktyg som anropades, agentens egna resonemang och exakt tidsåtgång.
2. **Tokens & Kostnad:** Visar antal tokens som förbrukats per agent/modell-anrop.
3. **Playground:** Gör det möjligt att analysera och testa ändringar i systemprompter eller verktygsdefinitioner direkt i UI.
4. **SQL-Workbench:** Tillåter sökning och filtrering i körningsloggar, exempelvis:
   ```sql
   SELECT duration, span_name 
   FROM records 
   WHERE regexp_like(span_name, 'career_agent');
   ```

---

## 6. Att tänka på / Best Practices

* **Kodning på Windows:** Sätt `encoding="utf-8"` vid alla filskrivningar eller sätt miljövariabeln `PYTHONUTF8=1`.
* **När ska man använda Multi-Agent?**
  * **Fördelar:** *Separation of concerns* – renare prompter och specialiserade ansvarsområden.
  * **Nackdelar:** Ökad latens, högre token-kostnader och mer komplex felhantering.
  * **Råd:** Börja med en singelagent med tydliga verktyg och introducera multi-agent först när komplexiteten kräver det.