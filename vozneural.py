# Autor: Jefferson O. Santos

import streamlit as st
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

def main():
    st.set_page_config(page_title="Voz-Neural", page_icon="🎙️")
    st.title("Voz-Neural: Conversor de Texto para Fala")
    st.write("Digite um texto, selecione o idioma, a voz, ajuste a velocidade e entonação para gerar e ouvir o áudio.")

    # Carregar vozes disponíveis
    voices = asyncio.run(list_voices())
    languages, language_voice_map = get_languages_and_voices(voices)

    # Interface do Streamlit
    text = st.text_area("Texto para converter em fala", placeholder="Digite seu texto aqui...")
    
    # Seleção do idioma
    selected_language = st.selectbox("Selecione o idioma", languages, index=languages.index('pt-BR') if 'pt-BR' in languages else 0)
    
    # Seleção da voz com base no idioma escolhido
    voice_options = [f"{voice['ShortName']} ({voice['Gender']})" for voice in language_voice_map[selected_language]]
    voice_short_names = [voice['ShortName'] for voice in language_voice_map[selected_language]]
    default_voice_index = voice_short_names.index('pt-BR-AntonioNeural') if 'pt-BR-AntonioNeural' in voice_short_names else 0
    selected_voice_display = st.selectbox("Selecione a voz", voice_options, index=default_voice_index)
    selected_voice = voice_short_names[voice_options.index(selected_voice_display)]

    rate = st.slider("Velocidade da fala (%)", -50, 50, 0, help="Ajuste a velocidade: positivo para mais rápido, negativo para mais lento.")
    pitch = st.slider("Entonação da fala (Hz)", -50, 50, 0, help="Ajuste o tom: positivo para mais agudo, negativo para mais grave.")
    
    # Botão para gerar e tocar áudio
    output_file = "output.mp3"
    if st.button("Gerar e Tocar Áudio"):
        if not text:
            st.error("Por favor, insira um texto para converter.")
        else:
            with st.spinner("Gerando áudio..."):
                rate_str = f"{rate:+d}%"
                pitch_str = f"{pitch:+d}Hz"
                try:
                    # Gerar o áudio
                    audio_file = asyncio.run(generate_speech(text, selected_voice, output_file, rate_str, pitch_str))
                    st.success(f"Áudio gerado com sucesso: {audio_file}")
                    
                    # Tocar o áudio usando st.audio
                    if os.path.exists(audio_file):
                        audio_value = open(audio_file, "rb")
                        st.audio(audio_value, format="audio/mp3")
                        audio_value.close()
                    else:
                        st.error("Erro: Arquivo de áudio não encontrado.")
                except Exception as e:
                    st.error(f"Erro ao gerar ou reproduzir o áudio: {str(e)}")

    # Adicionar nome do autor no rodapé
    st.markdown(
        """
        <style>
        .footer {
            position: fixed;
            bottom: 10px;
            width: 100%;
            text-align: center;
            color: #555;
            font-size: 14px;
        }
        </style>
        <div class="footer">
            Desenvolvido por Jefferson O. Santos
        </div>
        """,
        unsafe_allow_html=True
    )

if __name__ == "__main__":
    # Configuração para rodar asyncio com Streamlit
    import nest_asyncio
    nest_asyncio.apply()
    main()
