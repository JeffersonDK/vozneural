# Autor: Jefferson O. Santos

import asyncio
import edge_tts
import os
from pathlib import Path

async def list_voices():
    voices = await edge_tts.list_voices()
    return voices

async def generate_speech(text, voice, output_file, rate, pitch):
    communicate = edge_tts.Communicate(text, voice, rate=rate, pitch=pitch)
    await communicate.save(output_file)
    return output_file

def get_languages_and_voices(voices):
    languages = sorted(set(voice['Locale'] for voice in voices))
    language_voice_map = {lang: [v for v in voices if v['Locale'] == lang] for lang in languages}
    return languages, language_voice_map

async def text_to_speech(text):
    # Configurações fixas
    output_file = "output.mp3"
    selected_voice = 'pt-BR-AntonioNeural'
    rate = -8
    pitch = 10
    rate_str = f"{rate:+d}%"
    pitch_str = f"{pitch:+d}Hz"

    # Carregar vozes disponíveis
    voices = await list_voices()
    languages, language_voice_map = get_languages_and_voices(voices)

    # Verificar se pt-BR e pt-BR-AntonioNeural estão disponíveis
    if 'pt-BR' not in languages:
        raise ValueError("Idioma pt-BR não disponível. Verifique a biblioteca edge-tts.")
    if not any(voice['ShortName'] == 'pt-BR-AntonioNeural' for voice in language_voice_map['pt-BR']):
        raise ValueError("Voz pt-BR-AntonioNeural não disponível. Verifique a biblioteca edge-tts.")

    if not text:
        raise ValueError("Nenhum texto fornecido para conversão.")

    # Gerar o áudio
    try:
        audio_file = await generate_speech(text, selected_voice, output_file, rate_str, pitch_str)
        if not os.path.exists(audio_file):
            raise FileNotFoundError("Erro: Arquivo de áudio não encontrado.")
        return audio_file
    except Exception as e:
        raise Exception(f"Erro ao gerar o áudio: {str(e)}")

def play_audio(audio_file):
    # Função para tocar o áudio diretamente (depende do sistema operacional)
    try:
        if os.name == 'nt':  # Windows
            os.startfile(audio_file)
        elif os.name == 'posix':  # macOS/Linux
            os.system(f"open {audio_file}" if os.uname().sysname == 'Darwin' else f"xdg-open {audio_file}")
    except Exception as e:
        raise Exception(f"Erro ao reproduzir o áudio: {str(e)}")

async def convert_and_play(text):
    audio_file = await text_to_speech(text)
    play_audio(audio_file)

if __name__ == "__main__":
    import nest_asyncio
    nest_asyncio.apply()
    # Exemplo de uso
    text = "Este é um exemplo de texto para conversão em fala."
    asyncio.run(convert_and_play(text))