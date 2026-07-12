"""
Custom voice agent with proper WebRTC endpoint setup for voicebot.html
"""

import json
import os
from pathlib import Path
import asyncio

from dotenv import load_dotenv
from loguru import logger
from aiohttp import web

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
from pipecat.services.google.llm import GoogleLLMService
from pipecat.services.sarvam.stt import SarvamSTTService
from pipecat.services.sarvam.tts import SarvamTTSService
from pipecat.transports.base_transport import TransportParams
from pipecat.transports.network.webrtc_transport import WebRTCTransport

from language_router import LanguageRouterProcessor
from prompts import build_system_prompt

load_dotenv(override=True)

LEAD_FILE = Path(__file__).parent / "current_lead.json"

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


async def run_bot(transport):
    lead = load_current_lead()
    logger.info(f"Starting outbound call to lead: {lead.get('name')} ({lead.get('lead_id')})")

    stt = SarvamSTTService(
        api_key=os.getenv("SARVAM_API_KEY"),
        settings=SarvamSTTService.Settings(
            model="saaras:v3",
        ),
        keepalive_timeout=15.0,
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

    context = LLMContext(
        [{"role": "system", "content": build_system_prompt(lead)}]
    )
    context_aggregator = LLMContextAggregatorPair(
        context,
        user_params=LLMUserAggregatorParams(
            vad_analyzer=SileroVADAnalyzer(params=VADParams(stop_secs=0.2)),
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
        logger.info("Client connected - bot initiating conversation")
        await task.queue_frames([LLMRunFrame()])

    @transport.event_handler("on_client_disconnected")
    async def on_client_disconnected(transport, client):
        logger.info("Client disconnected")
        await task.cancel()

    runner = PipelineRunner()
    await runner.run(task)


async def handle_websocket(request):
    """Handle WebSocket connections for WebRTC signaling"""
    ws = web.WebSocketResponse()
    await ws.prepare(request)

    logger.info("WebSocket connection established")

    # Create WebRTC transport
    transport = WebRTCTransport(
        params=TransportParams(
            audio_in_enabled=True,
            audio_out_enabled=True,
        )
    )

    # Start the bot in a background task
    bot_task = asyncio.create_task(run_bot(transport))

    try:
        async for msg in ws:
            if msg.type == web.WSMsgType.TEXT:
                data = json.loads(msg.data)
                logger.info(f"Received WebSocket message: {data.get('type')}")

                # Handle WebRTC signaling messages
                if data.get('type') == 'offer':
                    # Send answer back to client
                    answer = await transport.handle_offer(data)
                    await ws.send_json(answer)

                elif data.get('type') == 'ice-candidate':
                    await transport.handle_ice_candidate(data.get('candidate'))

            elif msg.type == web.WSMsgType.ERROR:
                logger.error(f'WebSocket error: {ws.exception()}')

    except Exception as e:
        logger.error(f"WebSocket error: {e}")

    finally:
        logger.info("WebSocket connection closed")
        bot_task.cancel()

    return ws


async def handle_cors(request, handler):
    """Add CORS headers to all responses"""
    if request.method == "OPTIONS":
        response = web.Response()
    else:
        response = await handler(request)

    response.headers['Access-Control-Allow-Origin'] = '*'
    response.headers['Access-Control-Allow-Methods'] = 'GET, POST, OPTIONS'
    response.headers['Access-Control-Allow-Headers'] = 'Content-Type'

    return response


async def init_app():
    """Initialize the web application"""
    app = web.Application(middlewares=[handle_cors])

    # Add WebSocket endpoint
    app.router.add_get('/ws', handle_websocket)

    # Add health check endpoint
    async def health(request):
        return web.json_response({"status": "healthy", "service": "voice-bot"})

    app.router.add_get('/health', health)

    return app


if __name__ == "__main__":
    logger.info("Starting voice bot server on http://localhost:7860")

    app = init_app()
    web.run_app(
        asyncio.run(app),
        host='0.0.0.0',
        port=7860
    )
