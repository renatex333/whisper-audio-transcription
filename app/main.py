from contextlib import asynccontextmanager

from fastapi import FastAPI, UploadFile, File, HTTPException, status
from fastapi.responses import HTMLResponse

import os
from uuid import uuid4
import magic
import whisper
from loguru import logger
import boto3
import os
from dotenv import load_dotenv

KB = 1024
MB = KB * KB

SUPPORTED_FILE_TYPES = { # File type to extension mapping
    "audio/wav": ".wav",
    "audio/x-wav": ".wav",
    "audio/wave": ".wav",
    "audio/x-pn-wav": ".wav",
    "audio/mp3": ".mp3",
    "audio/mpeg": ".mp3",
    "audio/ogg": ".ogg",
    "audio/x-ogg": ".ogg",
    "audio/x-flac": ".flac",
    "audio/x-aiff": ".aiff",
    "audio/x-aifc": ".aifc",
    "audio/x-m4a": ".m4a",
    "audio/x-matroska": ".mka",
    "audio/x-musepack": ".mpc",
    "audio/x-ms-wma": ".wma",
    "audio/x-ms-wax": ".wax",
    "audio/x-vorbis": ".ogg",
    "audio/x-vorbis+ogg": ".ogg",
    "audio/x-speex": ".spx",
    "audio/3gpp": ".3gp",
    "audio/3gpp2": ".3g2",
    "audio/aac": ".aac",
    "audio/x-aac": ".aac",
    "audio/ac3": ".ac3",
    "audio/x-caf": ".caf",
    "audio/eac3": ".eac3",
    "audio/x-it": ".it",
    "audio/x-m4b": ".m4b",
    "audio/x-matroska": ".mka",
    "audio/x-mod": ".mod",
    "audio/x-mp3": ".mp3",
    "audio/x-mpeg": ".mp3",
    "audio/x-mpegurl": ".m3u",
    "audio/x-ms-asf": ".asf",
    "audio/x-ms-asx": ".asx",
}

load_dotenv(override=True)

AWS_BUCKET = os.getenv("AWS_BUCKET")

s3 = boto3.resource("s3")
bucket = s3.Bucket(AWS_BUCKET)

def s3_upload(contents: bytes, key: str):
    # Upload to S3
    logger.info(f"Uploading {key} to S3")
    bucket.put_object(Key=key, Body=contents)

def transcript(model, path: str):

    result = model.transcribe(path)

    return {"transcription": result['text']}


ml_models = {}


@asynccontextmanager
async def lifespan(app: FastAPI):
    model = whisper.load_model("large") # "tiny", "base", "small", "medium" or "large"
    # Load the ML model
    ml_models["Model"] = model
    yield
    # Clean up the ML models and release the resources
    ml_models.clear()


app = FastAPI(lifespan=lifespan)


@app.post("/transcript/")
async def predict(audio: UploadFile = File(...)):
    if not audio:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="No audio file provided")
    else:
        contents = audio.file.read()
        # Transcribe
        file_path = f"files/{audio.filename}"
        with open(file_path, "wb") as write_file:
            write_file.write(contents)
        result = transcript(ml_models["Model"], file_path)
        try:
            os.remove(file_path)
        except:
            pass
        # Send to S3
        file_size = len(contents)
        print(file_size)

        if not 0 < file_size <= MB:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File needs to be 0 - 1 MB")
        
        file_type = magic.from_buffer(buffer=contents, mime=True)
        print(file_type)

        if file_type not in SUPPORTED_FILE_TYPES:
            raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="File type not supported")
        
        s3_upload(contents=contents, key=f"{uuid4()}.{SUPPORTED_FILE_TYPES[file_type]}")
        
        return result

@app.get("/")
async def main():
    content = """
                <body>
                    <form action="/transcript/" enctype="multipart/form-data" method="post">
                        <input name="audio" type="file" accept="audio/*">
                            <input type="submit">
                    </form>
                </body>
              """
    return HTMLResponse(content=content)