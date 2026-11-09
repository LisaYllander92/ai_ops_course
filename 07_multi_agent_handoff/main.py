from agents import coach_agent, ClientDeps
import asyncio


async def main(prompt: str, **kwargs):
    result = await coach_agent.run(prompt, **kwargs)
    print(result.output)


if __name__ == "__main__":
    client = ClientDeps(
        name="Bobby",
        goal="looking for study opportunities and work opportunities within dta engineering",
        experience_lvl="intermediate",
        weekly_hours=16,
        current_role="IT-supporter",
    )
    asyncio.run(
        main(
            "I'm learning python and want to become a data engineer. What should I do?",
        deps=client,
        ),
    )
