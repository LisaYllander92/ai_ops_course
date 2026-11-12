from pydantic_ai import Agent
from pydantic_ai import RunContext
from model import nvidia_model
from dependencies import ClientDeps
from datetime import datetime
from pathlib import Path
from prompts import get_prompt

# Skapar språkmodellen som alla agenter delar
model = nvidia_model("nvidia/nemotron-3.5-super-vl-120b-a12b")

# Specialistagent för studieråd
study_agent = Agent(
    model=model,
    deps_type=ClientDeps,
    instructions=(
        get_prompt("study_agent_instructions")
    ),
)

# Specialistagent för karriärråd
career_agent = Agent(
    model=model,
    deps_type=ClientDeps,
    instructions=(
        get_prompt("career_agent_instructions")
    ),
)

# Huvudagent som koordinerar och delegerar till specialisterna
coach_agent = Agent(
    model=model,
    deps_type=ClientDeps,
    instructions=(
        get_prompt("coach_agent_instructions")
    ),
)


# Dynamiska instruktioner: lägger till klientens namn i varje agents prompt
@study_agent.instructions
def study_name(ctx: RunContext[ClientDeps]) -> str:
    return f"Student's name is {ctx.deps.name}. Adress them by name"

@career_agent.instructions
def career_name(ctx: RunContext[ClientDeps]) -> str:
    return f"Person you are coaching is {ctx.deps.name}. Adress them by name"

@coach_agent.instructions
def coach_name(ctx: RunContext[ClientDeps]) -> str:
    return f"Client you are advicing is {ctx.deps.name}. Adress them by name"


# Delegation Tools

# Låter coach-agenten fråga studieagenten (delar deps och usage-räkning)
@coach_agent.tool
async def ask_study_agent(ctx: RunContext[ClientDeps], question: str) -> str:
    """ask study specialist for advice on learning and studying"""
    result = await study_agent.run(question, deps = ctx.deps, usage=ctx.usage)
    return result.output


# Låter coach-agenten fråga karriäragenten
@coach_agent.tool
async def ask_career_agent(ctx: RunContext[ClientDeps], question: str) -> str:
    """ask career specialist for advice on what to choose for a career"""
    result = await career_agent.run(question, deps = ctx.deps, usage=ctx.usage)
    return result.output

# Sparar en rapport som markdown-fil i mappen "exports"
@coach_agent.tool
def export_report(ctx: RunContext[ClientDeps], text: str):
    """export the text to specified path"""
    # Tidsstämpel gör filnamnet unikt
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    # Skapar mappen om den inte redan finns
    export_dir = Path("exports")
    export_dir.mkdir(exist_ok=True)
    # Filnamn: klientens namn + tidsstämpel
    path = export_dir / f"{ctx.deps.name.casefold()}_{timestamp}.md"
    path.write_text(text, encoding="utf-8")