"""
Outbound sales voice agent.

Run locally:
    python bot.py

Then open http://localhost:7860/client in your browser, allow mic access,
and click Connect. The bot speaks first, exactly like it would on a real
outbound call — because as far as it's concerned, you just picked up.

To simulate a CRM lead coming in and personalizing the call, run
trigger_call.py BEFORE connecting (see that file / the README).
"""

import json
import os
from pathlib import Path

from dotenv import load_dotenv
from loguru import logger

from pipecat.audio.vad.silero import SileroVADAnalyzer
from pipecat.audio.vad.vad_analyzer import VADParams
from pipecat.frames.frames import LLMRunFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.runner import PipelineRunner
from pipecat.pipeline.task import PipelineParams, PipelineTask
from pipecat.processors.aggregators.llm_context import LLMContext
from pipecat.processors.aggregators.llm_response_universal import (
    LLMContextAggregatorPair,
    LLMUserAggregatorParams,
)
from pipecat.runner.types import RunnerArguments
from pipecat.runner.utils import create_transport
from pipecat.services.google.llm import GoogleLLMService
# from pipecat.services.sarvam import SarvamTTSService, SarvamHttpSTTService
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService
from pipecat.transcriptions.language import Language
from pipecat.transports.base_transport import BaseTransport, TransportParams

from language_router import LanguageRouterProcessor

from prompts import build_system_prompt

load_dotenv(override=True)

LEAD_FILE = Path(__file__).parent / "current_lead.json"

# Used only if no CRM trigger has run yet, so `python bot.py` always works out of the box.
DEFAULT_LEAD = {
    "lead_id": "DEMO",
    "name": "Arun",
    "phone": "+91XXXXXXXXXX",
    "source": "Housing.com",
    "enquired_project": "My Home Apas",
    "notes": "Demo lead used when no CRM trigger has run yet.",
}


def load_current_lead() -> dict:
    if LEAD_FILE.exists():
        try:
            return json.loads(LEAD_FILE.read_text())
        except Exception as e:
            logger.warning(f"Could not read {LEAD_FILE}, falling back to demo lead: {e}")
    return DEFAULT_LEAD


# Transport factory map required by create_transport(). We only wire up "webrtc"
# for local testing. See README for how to add "twilio"/"exotel" etc. later.
transport_params = {
    "webrtc": lambda: TransportParams(
        audio_in_enabled=True,
        audio_out_enabled=True,
    ),
}


async def run_bot(transport: BaseTransport):
    lead = load_current_lead()
    logger.info(f"Starting outbound call to lead: {lead.get('name')} ({lead.get('lead_id')})")

    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY"),
        settings=SarvamSTTService.Settings(
            model="saaras:v3",     # multilingual, built for Indian code-switching
        ),
        keepalive_timeout=15.0,    # keep STT websocket connection warm to prevent connection cold starts
    )

    llm = GoogleLLMService(
        api_key=os.getenv("GOOGLE_API_KEY"),
        settings=GoogleLLMService.Settings(
            model="gemini-2.5-flash",
            temperature=0.4,
            max_tokens=200,
        ),
    )

    tts = SarvamTTSService(
        api_key=os.getenv("SARVAM_API_KEY"),
        settings=SarvamTTSService.Settings(
            voice="shreya",
            model="bulbul:v3",
            pace=1.05,
        ),
    )

    # context = LLMContext()
    context = LLMContext(
        [{"role": "system", "content": build_system_prompt(lead)}]
    )
    context_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),  # reduced from 0.6 to detect end of speech 200ms faster
        ),
    )

    language_router = LanguageRouterProcessor()

    pipeline = Pipeline(
        [
            transport.input(),
            stt,
            context_aggregator.user(),
            llm,
            language_router,
            tts,
            transport.output(),
            context_aggregator.assistant(),
        ]
    )

    task = PipelineTask(
        pipeline,
        params=PipelineParams(
            allow_interruptions=True,
            enable_metrics=True,
        ),
    )

    @transport.event_handler("on_client_connected")
    async def on_client_connected(transport, client):
        logger.info("Prospect 'answered' — bot is initiating the conversation")
        # This is what makes it an OUTBOUND call: the bot speaks first,
        # instead of waiting for the person to say something.
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Call ended")
        await task.cancel()

    runner = PipelineRunner()
    await runner.run(task)


async def bot(runner_args: RunnerArguments):
    """Entry point called by the Pipecat dev runner for every new connection."""
    transport = await create_transport(runner_args, transport_params)
    await run_bot(transport)


if __name__ == "__main__":
    from pipecat.runner.run import main

    main()
