# Audio Transcription with Whisper

A simple FastAPI application designed for uploading audio messages, saving them to an AWS S3 bucket for storage, and returning corrected and comprehensible transcriptions.

It utilizes OpenAI's Whisper, a state-of-the-art speech recognition and transcription model (Open Source).

## Software Development Environment

Create a virtual environment:

    python -m venv env

Activate the virtual environment:

    . env/bin/activate  # For Unix-based systems
    . env\Scripts\activate  # For Windows

Install the necessary dependencies:

    pip install -r requirements.txt --no-cache-dir

Update Whisper:

    pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

You also need to install the `ffmpeg` tool.

On Windows, we need [Chocolatey](https://chocolatey.org/). Run the following command in Windows PowerShell as Administrator:

    choco install ffmpeg

On Ubuntu Linux:

    sudo apt update && sudo apt install ffmpeg

To save the dependencies used, whenever you make a modification, use the command:

    pip freeze > requirements.txt

To run the API:

    uvicorn app.main:app --reload

It will be exposed on port 8000.

## References

[Whisper Open Source Repository](https://github.com/openai/whisper)

[FastAPI Tutorial](https://fastapi.tiangolo.com/tutorial/)

[File Upload Tutorial](https://fastapi.tiangolo.com/tutorial/request-files/?h=file)
