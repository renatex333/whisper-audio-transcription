# whatsapp-audio-transcription

Projeto de bot de WhatsApp que recebe áudios de usuários e devolve a transcrição desses áudios de forma corrigida e compreensível.

Conta com o modelo de reconhecimento de voz e transcrição da gigante da Inteligência Artificial OpenAI, o Whisper (Open Source).

## Ambiente de Desenvolvimento do Software

Crie um ambiente virtual:

  python -m venv env
  
Instale as dependências necessárias:

    pip install -r requirements.txt
  
Faça update do Whisper:

    pip install --upgrade --no-deps --force-reinstall git+https://github.com/openai/whisper.git

É necessário também instalar a ferramenta `ffmpeg`.

No Windows, precisamos do [Chocolatey](https://chocolatey.org/). Execute no Windows PowerShell em modo de Administrador:

    choco install ffmpeg

No Linux Ubuntu:

    sudo apt update && sudo apt install ffmpeg

Para salvar as dependências utilizadas, sempre que realizar alguma modificação, use o comando:

    pip freeze > requirements.txt

## Referências

[Repositório do Whisper Open Source](https://github.com/openai/whisper)

  
