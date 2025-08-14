from agents import Agent, Runner, trace, function_tool
from connection import config  # Using your Gemini connection file
import asyncio
from dotenv import load_dotenv

# Load .env variables
load_dotenv()

# ----------- Tools -----------
@function_tool
def current_location():
    return "Karachi, Pakistan"

# ----------- Analyst Agents -----------
lyric_poetry = Agent(
    name="Lyric Poetry Agent",
    instructions="""
    You are a lyric poetry analyst.
    Lyric poetry expresses personal emotions and feelings.
    When a user submits such a poem, summarize the emotions and feelings.
    """
)

narrative_poetry = Agent(
    name="Narrative Poetry Agent",
    instructions="""
    You are a narrative poetry analyst.
    Narrative poetry tells a story with characters and events.
    When a user submits such a poem, summarize the story and its message.
    """
)

dramatic_poetry = Agent(
    name="Dramatic Poetry Agent",
    instructions="""
    You are a dramatic poetry analyst.
    Dramatic poetry is like a speech or monologue meant to be performed.
    When a user submits such a poem, summarize the character’s speech and drama.
    """
)

# ----------- Parent Agent -----------
poet_agent = Agent(
    name="Parent Poetry Agent",
    instructions="""
        You are a parent poetry agent.
        Your job is to:
        - If the poem is emotional or expressive → handoff to Lyric Poetry Agent.
        - If the poem tells a story with events → handoff to Narrative Poetry Agent.
        - If the poem is theatrical or like a monologue → handoff to Dramatic Poetry Agent.
        - If the poem also asks about location, call the current_location tool yourself.
    """,
    handoffs=[lyric_poetry, narrative_poetry, dramatic_poetry],
    tools=[current_location]
)

# ----------- Main function -----------
async def main():
    with trace("Poetry Agent - Gemini Test"):
        poem_input = """
        The weeping skies, a mirrored grief,
        Reflecting pain beyond belief.
        Each silver tear, a memory's sting,
        As sorrows rise on fragile wing.
        Where am I?
        """
        result = await Runner.run(
            poet_agent,
            poem_input,
            run_config=config
        )

        print("\n=== Final Output ===")
        print(result.final_output)
        print("\nLast Agent ==> ", result.last_agent.name)

if __name__ == "__main__":
    asyncio.run(main())
