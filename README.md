# whatsapp-audio-transcription

Projeto de bot de WhatsApp que recebe áudios de usuários e devolve a transcrição desses áudios de forma corrigida e compreensível.

Conta com o modelo de reconhecimento de voz e transcrição da gigante da Inteligência Artificial OpenAI, o Whisper (Open Source).

[Código do Whisper](https://github.com/openai/whisper)

## Ambiente de Desenvolvimento do Software

Crie um ambiente virtual:

  python -m venv env
  
Instale as dependências necessárias:

  pip install -r requirements.txt
  
Faça update do Whisper:

  pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git
  
