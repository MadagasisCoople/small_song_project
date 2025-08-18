from io import BytesIO
from fastapi.responses import StreamingResponse
from typing import Union,Optional
import base64

class HandlingReturn:

    async def text_and_audio(self, audio: Union[StreamingResponse,BytesIO], text: str, context:Optional[str] = None,/):
        """
        Returns a StreamingResponse object with the given audio bytes and a header with the given text
        encoded with base64. The header name is determined by the context parameter, defaulting to "header".

        Args:
            audio (Union[StreamingResponse,BytesIO]): The audio bytes to return
            text (str): The text to encode and return in the header
            context (Optional[str], optional): The name of the header to use. Defaults to None.

        Returns:
            StreamingResponse: The response object with the audio and header
        """
        encodedText = encoded = base64.b64encode(text.encode('utf-8')).decode('ascii')
        header = context or "header"
        if isinstance(audio, StreamingResponse):
            audio.headers[header] = encodedText
            return audio

        elif isinstance(audio, BytesIO):
            # Convert UploadFile to StreamingResponse
            audio.seek(0)           
            response = StreamingResponse(
                audio,
                media_type="audio/wav"
                )
            response.headers[header] = encodedText
            return response
