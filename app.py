import streamlit as st
import whisper
import torch
from diffusers import StableDiffusionPipeline
from PIL import Image

# Title
st.title("Speech-to-Image AI")

# Load Whisper Model
@st.cache_resource
def load_whisper():
    return whisper.load_model("base")

whisper_model = load_whisper()

# Load Stable Diffusion Model
@st.cache_resource
def load_stable_diffusion():
    model = StableDiffusionPipeline.from_pretrained(
        "runwayml/stable-diffusion-v1-5", torch_dtype=torch.float16 if torch.cuda.is_available() else torch.float32
    )
    model.to("cuda" if torch.cuda.is_available() else "cpu")
    return model

stable_diffusion_model = load_stable_diffusion()

# Upload Audio File
uploaded_file = st.file_uploader("Upload an audio file (MP3, WAV, M4A)", type=["mp3", "wav", "m4a"])

if uploaded_file:
    st.audio(uploaded_file, format="audio/mp3")
    
    # Transcribe Audio
    with st.spinner("Transcribing..."):
        transcription = whisper_model.transcribe(uploaded_file.name)
        prompt_text = transcription["text"]
        st.success("Transcription Complete!")
        st.write(f"**Transcription:** {prompt_text}")

    # Generate Image Button
    if st.button("Generate Image"):
        with st.spinner("Generating Image..."):
            image = stable_diffusion_model(prompt_text, height=512, width=512, guidance_scale=7.5).images[0]
            image.save("generated_image.png")
            st.image(image, caption="Generated Image", use_column_width=True)

st.write("🚀 Powered by Whisper & Stable Diffusion")
