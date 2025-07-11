# Autor: Jefferson O. Santos

import streamlit as st
import asyncio
import edge_tts
import os
from pathlib import Path

async def list_voices():
    voices = await edge_tts.list_voices()
    return voices

async def generate_speech(text, voice, output_file):
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(output_file)
    return output_file

def get_languages_and_voices(voices):
    languages = sorted(set(voice['Locale'] for voice in voices))
    language_voice_map = {lang: [v for v in voices if v['Locale'] == lang] for lang in languages}
    return languages, language_voice_map

def main():
    st.set_page_config(page_title="Voz-Neural", page_icon="🎙️")
    st.title("Voz-Neural: Conversor de Texto para Fala")
    st.write("Digite um texto para gerar e ouvir o áudio em português (pt-BR) com a voz AntonioNeural.")

    # Carregar vozes disponíveis
    voices = asyncio.run(list_voices())
    languages, language_voice_map = get_languages_and_voices(voices)

    # Verificar se pt-BR e pt-BR-AntonioNeural estão disponíveis
    if 'pt-BR' not in languages:
        st.error("Idioma pt-BR não disponível. Verifique a biblioteca edge-tts.")
        return
    if not any(voice['ShortName'] == 'pt-BR-AntonioNeural' for voice in language_voice_map['pt-BR']):
        st.error("Voz pt-BR-AntonioNeural não disponível. Verifique a biblioteca edge-tts.")
        return

    # Interface do Streamlit
    text = st.text_area("Texto para converter em fala", placeholder="Digite seu texto aqui...")
    
    # Idioma fixo como pt-BR, com opção de mudar
    selected_language = st.selectbox("Selecione o idioma", languages, index=languages.index('pt-BR') if 'pt-BR' in languages else 0)
    
    # Voz fixa como pt-BR-AntonioNeural
    selected_voice = 'pt-BR-AntonioNeural'
    st.write(f"Voz selecionada: pt-BR-AntonioNeural (Masculina)")

    # Botão para gerar e tocar áudio
    output_file = "output.mp3"
    if st.button("Gerar e Tocar Áudio"):
        if not text:
            st.error("Por favor, insira um texto para converter.")
        else:
            with st.spinner("Gerando áudio..."):
                try:
                    # Gerar o áudio
                    audio_file = asyncio.run(generate_speech(text, selected_voice, output_file))
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