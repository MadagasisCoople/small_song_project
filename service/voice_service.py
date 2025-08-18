from hashlib import sha256
from io import BytesIO
from dotenv import load_dotenv
import wave
import os
from fastapi.responses import StreamingResponse
from pipecat.services.elevenlabs.tts import ElevenLabsTTSService
from pipecat.frames.frames import Frame, TTSSpeakFrame, EndFrame, BotSpeakingFrame, AudioRawFrame
from pipecat.pipeline.pipeline import Pipeline
from pipecat.pipeline.task import PipelineTask, PipelineParams
from pipecat.pipeline.runner import PipelineRunner as PipecatPipelineRunner
from pipecat.observers.base_observer import BaseObserver, FramePushed
from uuid import uuid4
from pipecat.services.deepgram.stt import DeepgramSTTService
from deepgram import LiveOptions
import platform
from pipecat.pipeline.runner import PipelineRunner as BasePipelineRunner

class PipelineRunner(BasePipelineRunner):
    def _setup_sigint(self):
        if platform.system() != "Windows":
            super()._setup_sigint()


class VoiceService():

    # Setting up def
    # This function wraps PCM data into a WAV format
    def wrapPCMToWav(self, pcm_data: bytes, sample_rate=24000, num_channels=1, sample_width=2) -> bytes:
        buffer = BytesIO()
        with wave.open(buffer, 'wb') as wav_file:
            wav_file.setnchannels(num_channels)
            wav_file.setsampwidth(sample_width)  # 2 bytes = 16-bit
            wav_file.setframerate(sample_rate)
            wav_file.writeframes(pcm_data)
        buffer.seek(0)
        return buffer.read()

    async def extractWavData(self, wavData: bytes):
        with wave.open(BytesIO(wavData), 'rb') as wf:
            sampleRate = wf.getframerate()
            numChannels = wf.getnchannels()
        return sampleRate, numChannels
    # This function uses ElevenLabs TTS service to convert text to speech

    async def speak_up(self, text: str):

        load_dotenv()
        tts = None
        apiKey: str | None = os.getenv("ELEVENLABS_API_KEY")
        if apiKey is None:
            raise ValueError(
                "ELEVENLABS_API_KEY environment variable is not set")

        print(f"API Key starts with: {apiKey[:4]}...{apiKey[-4:]}")
        print("Attempting to create TTS service...")

        # Create TTS service and establish connection
        tts = ElevenLabsTTSService(
            api_key=apiKey,
            voice_id="wnRasc8KqpciFFcZl9OS",
            model="eleven_multilingual_v2"
        )

        print("TTS service created, attempting connection...")

        # Create and run pipeline
        observer = MyFrameObserver()
        task = PipelineTask(
            Pipeline([tts]),
            observers=[observer],
            params=PipelineParams(allow_interruptions=True),
            idle_timeout_secs= 20 ,  # 15 sec timeout
            # Only monitor bot speaking
            idle_timeout_frames=(BotSpeakingFrame,),
            cancel_on_idle_timeout=True,
        )  # Auto-cancel

        # Queue frames and run
        await task.queue_frames([TTSSpeakFrame(text), EndFrame()])
        print("Frames queued, starting runner...")

        runner = PipelineRunner()
        print("Before runner.run")
        await runner.run(task)

        print("After runner.run")

        if hasattr(tts, '_disconnect_websocket'):
            await tts._disconnect_websocket()

        output = observer.get_audio_bytes()
        outputWave = self.wrapPCMToWav(output)

        # return StreamingResponse(BytesIO(outputWave), media_type = "audio/wav")
        return StreamingResponse(
            BytesIO(outputWave),
            media_type="audio/wav"
        )

    async def speak_down(self, outLanguage: str, audio: bytes):
        load_dotenv()
        stt = None
        apiKey: str | None = os.getenv("DEEPGRAM_API_KEY")
        if apiKey is None:
            raise ValueError(
                "DEEPGRAM_API_KEY environment variable is not set")

        print(f"API Key starts with: {apiKey[:4]}...{apiKey[-4:]}")
        print("Attempting to create STT service...")

        print(outLanguage)
        # Create STT service and establish connection
        stt = DeepgramSTTService(
            api_key=apiKey,
            live_options=LiveOptions(
                model="nova-2",
                language=outLanguage,
            )
        )

        print("STT service created, attempting connection...")

        # Create and run pipeline
        observer = MyTextObserver()

        task = PipelineTask(
            Pipeline([stt]),
            observers=[observer],
            params=PipelineParams(allow_interruptions=True),
            cancel_on_idle_timeout=True,
        )

        # Prepare data for AudioRawFrame
        with wave.open(BytesIO(audio), 'rb') as wf:
            rawPcm = wf.readframes(wf.getnframes())
        sampleRate, numChannels = await self.extractWavData(audio)

        audioFrame = AudioRawFrame(
            rawPcm,
            sample_rate=sampleRate,
            num_channels=numChannels,
        )

        setattr(audioFrame, "encoding", "linear16")
        setattr(audioFrame, "id", str(uuid4()))

        await task.queue_frames([
            audioFrame,  # type: ignore
            EndFrame()
        ])

        runner = PipelineRunner()
        try:
            await runner.run(task)
        except Exception as e:
            print(f"Deepgram failed: {e}")
            return {"message": "Deepgram failed"}

        return {"message": observer.get_text()}


class MyFrameObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self._name = "MyFrameObserver"
        self.audio_chunks = []
        self.seenHashes = set()

    async def on_push_frame(self, data: FramePushed):
        frame = data.frame
        print(f"[Frame] {frame}")

        if isinstance(frame, AudioRawFrame):
            audio_hash = sha256(frame.audio).hexdigest()
            if audio_hash not in self.seenHashes:
                self.seenHashes.add(audio_hash)
                self.audio_chunks.append(frame.audio)
            else:
                print("Duplicate audio skipped")
        elif isinstance(frame, BotSpeakingFrame):
            print("🗣️ Bot is speaking")

    def get_audio_bytes(self) -> bytes:
        print(f"Number of chunks: {len(self.audio_chunks)}")
        return b"".join(self.audio_chunks)


class MyTextObserver(BaseObserver):
    def __init__(self):
        super().__init__()
        self._name = "MyTextObserver"
        self.final_text = None

    async def on_push_frame(self, data: FramePushed):

        frame = data.frame
        if hasattr(data.frame, "text") and data.frame.text:  # type: ignore
            # Only keep final
            if (getattr(data.frame, "is_final", True)):
                print(f"📝 Transcribed Text: {data.frame.text}")  # type: ignore
                self.final_text = data.frame.text  # type: ignore

    def get_text(self) -> str:
        return self.final_text.strip() if self.final_text else "[no speech detected]"
