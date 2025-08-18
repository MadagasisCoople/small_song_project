# ConsoleSub.py

import asyncio
import os
import sys
import time
from inspect import iscoroutinefunction
from typing import AsyncGenerator, Awaitable, Callable, Dict, List, Optional, TypeVar, Union, cast

from autogen_core import CancellationToken
from autogen_core.models import RequestUsage
from autogen_agentchat.agents import UserProxyAgent
from autogen_agentchat.base import Response, TaskResult
from autogen_agentchat.messages import (
    BaseAgentEvent,
    BaseChatMessage,
    ModelClientStreamingChunkEvent,
    MultiModalMessage,
    UserInputRequestedEvent,
    ToolCallExecutionEvent,
    ToolCallSummaryMessage,
    ToolCallRequestEvent,
)

from service.voice_service import VoiceService

voiceService = VoiceService()

T = TypeVar("T", bound=TaskResult | Response)

def _is_running_in_iterm() -> bool:
    return os.getenv("TERM_PROGRAM") == "iTerm.app"

def _is_output_a_tty() -> bool:
    return sys.stdout.isatty()

def aprint(output: str, end: str = "\n", flush: bool = False) -> Awaitable[None]:
    return asyncio.to_thread(print, output, end=end, flush=flush)


class UserInputManager:
    def __init__(self, callback: Callable):
        self.input_events: Dict[str, asyncio.Event] = {}
        self.callback = callback

    def get_wrapped_callback(self) -> Callable:
        async def wrapper(prompt: str, cancellation_token: Optional[CancellationToken]) -> str:
            request_id = UserProxyAgent.InputRequestContext.request_id()
            if request_id not in self.input_events:
                self.input_events[request_id] = asyncio.Event()
            await self.input_events[request_id].wait()
            del self.input_events[request_id]

            if iscoroutinefunction(self.callback):
                return await self.callback(prompt, cancellation_token)
            else:
                loop = asyncio.get_event_loop()
                return await loop.run_in_executor(None, self.callback, prompt)

        return wrapper

    def notify_event_received(self, request_id: str) -> None:
        self.input_events.setdefault(request_id, asyncio.Event()).set()


class ConsoleSub:
    @staticmethod
    async def run(
        stream: AsyncGenerator[BaseAgentEvent | BaseChatMessage | T, None],
        *,
        no_inline_images: bool = False,
        output_stats: bool = False,
        user_input_manager: UserInputManager | None = None,
    ) -> T:
        render_image_iterm = _is_running_in_iterm() and _is_output_a_tty() and not no_inline_images
        start_time = time.time()
        total_usage = RequestUsage(prompt_tokens=0, completion_tokens=0)
        last_processed: Optional[T] = None
        streaming_chunks: List[str] = []

        async for message in stream:

            if isinstance(message, TaskResult):
                duration = time.time() - start_time
                if output_stats:
                    await aprint(
                        f"{'-' * 10} Summary {'-' * 10}\n"
                        f"Number of messages: {len(message.messages)}\n"
                        f"Finish reason: {message.stop_reason}\n"
                        f"Total prompt tokens: {total_usage.prompt_tokens}\n"
                        f"Total completion tokens: {total_usage.completion_tokens}\n"
                        f"Duration: {duration:.2f} seconds\n"
                    )
                last_processed = message  # type: ignore

            elif isinstance(message, Response):
                duration = time.time() - start_time
                final_content = (
                    message.chat_message.to_text(iterm=render_image_iterm)
                    if isinstance(message.chat_message, MultiModalMessage)
                    else message.chat_message.to_text()
                )

                output = f"{'-' * 10} {message.chat_message.source} {'-' * 10}\n{final_content}\n"
                if message.chat_message.models_usage:
                    if output_stats:
                        output += f"[Prompt tokens: {message.chat_message.models_usage.prompt_tokens}, Completion tokens: {message.chat_message.models_usage.completion_tokens}]\n"
                    total_usage.completion_tokens += message.chat_message.models_usage.completion_tokens
                    total_usage.prompt_tokens += message.chat_message.models_usage.prompt_tokens
                await aprint(output, end="", flush=True)

                if output_stats:
                    num_inner_messages = len(message.inner_messages) if message.inner_messages else 0
                    await aprint(
                        f"{'-' * 10} Summary {'-' * 10}\n"
                        f"Number of inner messages: {num_inner_messages}\n"
                        f"Total prompt tokens: {total_usage.prompt_tokens}\n"
                        f"Total completion tokens: {total_usage.completion_tokens}\n"
                        f"Duration: {duration:.2f} seconds\n"
                    )
                last_processed = message  # type: ignore

            elif isinstance(message, UserInputRequestedEvent):
                if user_input_manager is not None:
                    user_input_manager.notify_event_received(message.request_id)

            else:
                message = cast(BaseAgentEvent | BaseChatMessage, message)  # type: ignore
                source = getattr(message, "source", None)
                # SKIP TOOL and USER MESSAGES
                if source in ("user",):  #"song_recommender"
                   continue

                # if isinstance(message, (ToolCallRequestEvent,ToolCallExecutionEvent, ToolCallSummaryMessage)):
                #     continue

                if not streaming_chunks:
                    await aprint(
                        f"{'-' * 10} {message.source} ({message.__class__.__name__}) {'-' * 10}"
                    )
                if isinstance(message, ModelClientStreamingChunkEvent):
                    await aprint(message.to_text(), end="", flush=True)
                    streaming_chunks.append(message.content)
                
                else:
                    if streaming_chunks:
                        streaming_chunks.clear()
                        await aprint("", end="\n", flush=True)
                    elif isinstance(message, MultiModalMessage):
                        await aprint(message.to_text(iterm=render_image_iterm), end="\n", flush=True)
                    else:
                        if(source == "Ms_Robin"):
                            print(len(message.to_text().split()))
                            if(len(message.to_text().split()) <28):
                               cleaned = message.to_text().replace("[", "").replace("]", "")
                               one_line = " ".join(cleaned.split())
                               # await voiceService.speak_up(one_line)
                            await aprint(message.to_text(), end="\n", flush=True)
                        else:
                            await aprint(message.to_text(), end="\n", flush=True)

                    if message.models_usage and output_stats:
                        await aprint(
                            f"[Prompt tokens: {message.models_usage.prompt_tokens}, Completion tokens: {message.models_usage.completion_tokens}]"
                        )
                    if message.models_usage:
                        total_usage.completion_tokens += message.models_usage.completion_tokens
                        total_usage.prompt_tokens += message.models_usage.prompt_tokens

        if last_processed is None:
            raise ValueError("No TaskResult or Response was processed.")
        
        return last_processed
