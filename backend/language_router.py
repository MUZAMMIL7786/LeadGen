"""
Sits between `llm` and `tts` in the pipeline. Gemini is instructed (see
prompts.py) to prefix every reply with a tag like [[LANG:te]] before the
actual reply text. This processor:
  1. Buffers just the first few characters of each assistant turn
  2. Parses the tag and strips it out (the tag itself is never spoken)
  3. Pushes a TTSUpdateSettingsFrame so Sarvam switches voice + language
     BEFORE the rest of the sentence streams through
  4. Passes everything else straight through untouched

Because it only buffers ~10-15 characters (not the whole reply), it adds
no meaningful latency to the streaming TTS behavior you already have.
"""

import re

from pipecat.frames.frames import (
    Frame,
    LLMFullResponseStartFrame,
    LLMTextFrame,
    TTSUpdateSettingsFrame,
)
from pipecat.processors.frame_processor import FrameDirection, FrameProcessor
from pipecat.transcriptions.language import Language

TAG_RE = re.compile(r"\[\[LANG:(\w+)\]\]")

# language code -> (Sarvam Language enum, speaker voice)
LANG_VOICE_MAP = {
    "en": (Language.EN_IN, "shreya"),
    "hi": (Language.EN_IN, "shreya"),  # Route Hinglish (Latin script) to EN_IN for natural pronunciation
    "te": (Language.TE_IN, "kavya"),
}
DEFAULT_LANG = "en"

# Safety cap: if no closing "]]" shows up within this many buffered
# characters, assume the model forgot the tag and just flush as-is.
MAX_BUFFER = 24


class LanguageRouterProcessor(FrameProcessor):
    def __init__(self):
        super().__init__()
        self._buffer = ""
        self._tag_resolved = False

    async def process_frame(self, frame: Frame, direction: FrameDirection):
        await super().process_frame(frame, direction)

        if isinstance(frame, LLMFullResponseStartFrame):
            self._buffer = ""
            self._tag_resolved = False
            await self.push_frame(frame, direction)
            return

        if isinstance(frame, LLMTextFrame) and not self._tag_resolved:
            self._buffer += frame.text
            
            # Strip leading whitespace/newlines to find the tag robustly
            stripped_buffer = self._buffer.lstrip()
            match = TAG_RE.match(stripped_buffer)

            if match:
                lang_code = match.group(1).lower()
                language, voice = LANG_VOICE_MAP.get(
                    lang_code, LANG_VOICE_MAP[DEFAULT_LANG]
                )
                await self.push_frame(
                    TTSUpdateSettingsFrame(settings={"language": language, "voice": voice}),
                    direction,
                )
                self._tag_resolved = True
                
                # Extract everything after the matched tag
                tag_start = self._buffer.find(match.group(0))
                remainder = self._buffer[tag_start + len(match.group(0)):]
                if remainder:
                    # Strip any single leading space after the tag if present
                    if remainder.startswith(" "):
                        remainder = remainder[1:]
                    await self.push_frame(LLMTextFrame(text=remainder), direction)
                return

            if len(self._buffer) >= MAX_BUFFER:
                # No tag found — flush the buffered text as-is, keep
                # whatever language was already set, stop buffering.
                self._tag_resolved = True
                await self.push_frame(LLMTextFrame(text=self._buffer), direction)
            return  # still buffering, don't forward yet

        await self.push_frame(frame, direction)