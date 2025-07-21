import streamlit as st
import asyncio
import edge_tts
import io

async def text_to_speech(text):
    """Converts text to speech using edge_tts and returns audio bytes."""
    try:
        tts = edge_tts.Communicate(text, "pt-BR-AntonioNeural")
        audio_buffer = io.BytesIO()
        async for chunk in tts.stream():
            if chunk["type"] == "audio":
                audio_buffer.write(chunk["data"])
        audio_buffer.seek(0)
        return audio_buffer
    except Exception as e:
        st.error(f"Erro ao gerar áudio: {str(e)}")
        return None

# Streamlit app
st.title("Texto para Fala")
st.write("Digite o texto para converter em fala usando a voz pt-BR-AntonioNeural.")

# Text input
user_text = st.text_area("Texto para converter:", height=150)

# Button to trigger conversion
if st.button("Converter para Fala"):
    if user_text.strip():
        # Run async function in Streamlit
        audio_buffer = asyncio.run(text_to_speech(user_text))
        if audio_buffer:
            st.audio(audio_buffer, format="audio/mp3")
            st.success("Áudio gerado com sucesso!")
    else:
        st.warning("Por favor, insira um texto válido.")