import asyncio
import os
import logging
from dotenv import load_dotenv

from livekit.agents import JobContext, WorkerOptions, cli, Agent, AgentSession, llm
from livekit.plugins import openai, deepgram, elevenlabs, silero
from airtable_logger import AirtableLogger

# Load environment variables
load_dotenv()

# Setup logging
logger = logging.getLogger("voice-agent")
logger.setLevel(logging.INFO)

# Initialize Airtable Logger
airtable = AirtableLogger()

# Define the System Prompt for Lily
LILY_PROMPT = """
You are Lily, a friendly and professional customer support assistant for 'Flora', a premium flower shop.
Your goal is to assist customers with their queries about flower arrangements, delivery services, and store information.

Key Information:
- Shop Name: Flora
- Business Hours: Monday to Saturday, 9:00 AM to 6:00 PM. Closed on Sundays.
- Delivery: Same-day delivery is available for orders placed before 2:00 PM.
- Products: We specialize in Roses, Lilies, Tulips, and Exotic Orchids.
- Tone: Polite, warm, and natural. Keep responses concise for voice interaction.
- Restrictions: If you don't know the answer, politely ask the customer to leave their number so a human can call them back.

Always be helpful and greet the customer warmly.
"""

async def entrypoint(ctx: JobContext):
    logger.info(f"Connecting to room: {ctx.room.name}")

    try:
        # Setup the Agent with its own configuration
        lily_agent = Agent(
            instructions=LILY_PROMPT,
            stt=deepgram.STT(),
            llm=openai.LLM(model="gpt-4o"),
            tts=elevenlabs.TTS(voice_id=os.getenv("ELEVENLABS_VOICE_ID", "21m00Tcm4lpxqxtOC5vp")),
            vad=silero.VAD.load(),
        )

        # Setup the AgentSession
        session = AgentSession(
            stt=lily_agent.stt,
            vad=lily_agent.vad,
            llm=lily_agent.llm,
            tts=lily_agent.tts,
        )

        # Track transcript for logging
        full_transcript = []

        @session.on("conversation_item_added")
        def on_conversation_item(event):
            item = event.item
            if hasattr(item, "role"):
                role = "Lily" if item.role == "assistant" else "User"
                # Use text_content helper if available, otherwise fallback to content
                content = getattr(item, "text_content", "")
                if not content and hasattr(item, "content"):
                    content = str(item.content)
                
                if content:
                    logger.info(f"Transcript: {role}: {content}")
                    full_transcript.append(f"{role}: {content}")

        # Start the session
        await session.start(lily_agent, room=ctx.room)
        logger.info("Agent session started.")

        # Wait for disconnect
        await ctx.wait_for_disconnect()
        
        logger.info("Room disconnected. Saving transcript...")

        # Log the call to Airtable
        duration = 0 
        caller_id = "Unknown"
        
        for participant in ctx.room.participants.values():
            if participant.kind == "sip":
                caller_id = participant.identity
                break

        combined_transcript = "\n".join(full_transcript)
        if combined_transcript:
            airtable.log_call(caller_id, duration, combined_transcript)
            logger.info(f"Call logged to Airtable for {caller_id}")
        else:
            logger.info("No transcript gathered, skipping Airtable log.")

    except Exception as e:
        logger.error(f"Error in entrypoint: {e}", exc_info=True)

if __name__ == "__main__":
    cli.run_app(WorkerOptions(entrypoint_fnc=entrypoint))
