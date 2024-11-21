import google.generativeai as genai
import streamlit as st
from streamlit_lottie import st_lottie
import json
import os
import time

# Function to load Lottie animations
def load_lottie_url(url: str):
    import requests
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    else:
        return None

# Set up Google Generative AI (GenAI) API key
with open("keys/Gemini_Api.txt") as f:
    key = f.read()
genai.configure(api_key=key)

# Set up the main title and theme
st.set_page_config(page_title="AI Assistive App", page_icon="🤖", layout="wide")

# Sidebar: Welcome dashboard with description and icons
st.sidebar.title("Welcome to the AI-Powered Assistive App 💡")
st.sidebar.markdown("""
**This AI app helps you with real-time feedback and tasks using images or code analysis.**
""")
st.sidebar.markdown("📝 **How It Works:**\n1. Upload an image.\n2. Select features you want.\n3. Receive AI feedback or conversion!")

# Lottie animation for the main interface (using a public URL for demonstration)
lottie_animation_url = "https://assets7.lottiefiles.com/packages/lf20_hz6jzprc.json"  # Replace with a suitable Lottie URL
lottie_animation = load_lottie_url(lottie_animation_url)
if lottie_animation:
    st_lottie(lottie_animation, height=200, key="animation")

# Main title and subtitle
st.title("AI-Powered Assistive Technology App 🤖")
st.subheader("Upload your image or code, and let AI assist you with real-time feedback!")

# File Upload Section (for image uploads)
uploaded_file = st.file_uploader("Choose an image to analyze...", type=["jpg", "jpeg", "png"])

if uploaded_file:
    st.image(uploaded_file, caption="Uploaded Image", use_container_width=True)
    image = uploaded_file

# Checkboxes for Feature Selection in the sidebar (placed vertically)
st.sidebar.title("Select Features")
scene_desc_checkbox = st.sidebar.checkbox("Real-Time Scene Understanding", key="scene_desc")
personalized_assistance_checkbox = st.sidebar.checkbox("Personalized Assistance for Tasks", key="personalized_assistance")
text_to_speech_checkbox = st.sidebar.checkbox("Text-to-Speech Conversion", key="text_to_speech")

# Function to generate scene description using AI
def generate_scene_description(image_path):
    try:
        # Request a scene description from Google Generative AI
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        ai_assistant = model.start_chat(history=[])
        
        prompt = "Generate a detailed description of the image for accessibility purposes."
        response = ai_assistant.send_message(prompt)
        
        return response.text.strip() if response and response.text else "No description generated."
    except Exception as e:
        return f"Error generating description: {str(e)}"

# Function to provide personalized assistance based on image
def provide_personalized_assistance(description):
    try:
        model = genai.GenerativeModel("models/gemini-1.5-flash")
        ai_assistant = model.start_chat(history=[])
        
        prompt = f"Provide personalized assistance based on the following scene description: {description}"
        response = ai_assistant.send_message(prompt)
        
        return response.text.strip() if response and response.text else "No assistance generated."
    except Exception as e:
        return f"Error generating assistance: {str(e)}"

# Text-to-Speech Function
def text_to_speech(text):
    from gtts import gTTS
    import os
    
    try:
        tts = gTTS(text)
        audio_file = "output.mp3"
        tts.save(audio_file)
        return audio_file
    except Exception as e:
        return f"Error generating speech: {str(e)}"

# Processing the selected features when buttons are clicked
if uploaded_file:
    if scene_desc_checkbox or personalized_assistance_checkbox or text_to_speech_checkbox:
        with st.spinner("Processing..."):
            time.sleep(2)  # Simulating processing time

            # Real-Time Scene Understanding
            if scene_desc_checkbox:
                st.header("Real-Time Scene Understanding")
                description = generate_scene_description(uploaded_file)
                if "Error" in description:
                    st.error(description)
                else:
                    st.write(description)

            # Personalized Assistance for Tasks
            if personalized_assistance_checkbox:
                st.header("Personalized Assistance for Tasks")
                description = generate_scene_description(uploaded_file)
                if "Error" in description:
                    st.error(description)
                else:
                    assistance = provide_personalized_assistance(description)
                    if "Error" in assistance:
                        st.error(assistance)
                    else:
                        st.write(assistance)

            # Text-to-Speech Conversion
            if text_to_speech_checkbox:
                st.header("Text-to-Speech Conversion")
                extracted_text = generate_scene_description(uploaded_file)
                if "Error" in extracted_text:
                    st.error(extracted_text)
                else:
                    st.write("Extracted Text:")
                    st.write(extracted_text)
                    audio_file = text_to_speech(extracted_text)
                    if "Error" in audio_file:
                        st.error(audio_file)
                    else:
                        st.audio(audio_file, format="audio/mp3")

# Footer
st.markdown("---")
st.markdown("🔍 Powered by Google's Generative AI | Built with ❤️ using Streamlit")
