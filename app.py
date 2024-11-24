import streamlit as st
from PIL import Image
import pytesseract
import pyttsx3
import os
import google.generativeai as genai
from langchain_google_genai import GoogleGenerativeAI

# Set Tesseract executable path
pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

# Initialize Google Generative AI with API Key
GEMINI_API_KEY = ("Gemini_Api_Key")  # Replace with your valid API key
os.environ["Gemini_Api_Key"] = GEMINI_API_KEY

llm = GoogleGenerativeAI(model="gemini-1.5-pro", api_key=GEMINI_API_KEY)

# Initialize Text-to-Speech engine
engine = pyttsx3.init()

# Set up Streamlit page with custom configurations (excluding favicon argument)
st.set_page_config(page_title="AI Assistant for Visually Impaired", initial_sidebar_state="expanded")

# Add favicon directly using HTML
st.markdown("""
    <link rel="icon" href="path_to_your_icon.ico" type="image/x-icon">
""", unsafe_allow_html=True)

# Custom CSS to change title color and add chatbot icon
st.markdown("""
    <style>
    .title {
        color: #4CAF50;  /* Green color for project title */
        font-size: 40px;
        font-weight: bold;
        display: flex;
        align-items: center;
    }
    .title img {
        width: 30px;
        height: 30px;
        margin-right: 10px;
    }
    </style>
""", unsafe_allow_html=True)

# Display custom-colored title with AI chatbot icon
st.markdown('<p class="title"><img src="https://www.cioinsight.com/wp-content/uploads/2022/08/Chatbots-in-Machine-Learning-scaled.jpeg" alt="AI Chatbot Icon">AI Assistant for Visually Impaired</p>', unsafe_allow_html=True)  # Replace with actual chatbot icon URL

# Sidebar with project description and features
st.sidebar.title("🤖 Welcome to AI Assistant for Visually Impaired!")

# Sidebar project description
st.sidebar.markdown("""
Welcome to **AI Assistant for Visually Impaired** 🎉, your AI-powered assistant designed to enhance accessibility for visually impaired individuals. 
This project leverages advanced AI capabilities to interpret images, generate meaningful descriptions, and assist in various daily tasks with personalized guidance.
""")

# Sidebar features section
st.sidebar.markdown("### 🌟 Key Features")
st.sidebar.markdown("""
- **🔍 Scene Understanding**: Provides a detailed description of the content in uploaded images, helping users understand their surroundings.
- **🔊 Text-to-Speech**: Converts the scene description or extracted text into audio for seamless interaction.
- **📋 Personalized Assistance**: Offers task-specific guidance based on the detected objects or scene in the uploaded image.
- **⚠️ Object & Obstacle Detection**: Identifies objects and potential obstacles to enhance situational awareness.
""")

# Sidebar usage instructions
st.sidebar.markdown("### 📖 How to Use")
st.sidebar.markdown("""
1. Upload an image in the main section.
2. Choose a feature, such as **Describe Scene**, **Text-to-Speech**, or **Personalized Assistance**.
3. Let the app process the image and provide assistance.
""")

# Functions for processing
def generate_scene_description(input_prompt, image_data):
    """Generates a scene description using Google Generative AI."""
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([input_prompt, image_data[0]])
    return response.text

def generate_task_guidance_assistant(input_prompt, image_data):
    """Generates task-specific guidance based on the image."""
    task_prompt = f"""
    You are an AI assistant helping visually impaired individuals by recognizing objects and providing task-specific guidance.
    Based on the image, identify useful items (e.g., food, clothing, products) and provide suggestions for daily tasks.
    Provide instructions on how to interact with recognized items, read labels, or identify objects for tasks such as cooking, dressing, or other activities.
    """
    model = genai.GenerativeModel('gemini-1.5-pro')
    response = model.generate_content([task_prompt, image_data[0]])
    return response.text

def input_image_setup(uploaded_file):
    """Prepares the uploaded image for processing."""
    if uploaded_file is not None:
        bytes_data = uploaded_file.getvalue()
        image_parts = [
            {
                "mime_type": uploaded_file.type,
                "data": bytes_data
            }
        ]
        return image_parts
    else:
        raise FileNotFoundError("No file uploaded.")

# Main app functionality
uploaded_file = st.file_uploader("📤 Upload an image...", type=["jpg", "jpeg", "png"])

# Layout: two columns for buttons and image
col1, col2 = st.columns([1, 3])  # Button section on the left (col1), image on the right (col2)

with col1:
    # Make all buttons the same size by using 'use_container_width=True'
    scene_button = st.button("🔍 Describe Scene", use_container_width=True)
    tts_button = st.button("🔊 Text-to-Speech", use_container_width=True)
    task_button = st.button("📝 Personalized Assistance", use_container_width=True)

with col2:
    # Display the uploaded image if it exists, resized to a smaller size
    if uploaded_file:
        image = Image.open(uploaded_file)
        st.image(image, caption="Uploaded Image", width=500)  # Resize image to 500px wide, further to the right

# Input Prompt for AI Scene Understanding
input_prompt = """
You are an AI assistant helping visually impaired individuals by describing the scene in the image. Provide:
1. List of items detected in the image with their purpose.
2. Overall description of the image.
3. Suggestions for actions or precautions for the visually impaired.
"""

# Process based on user interaction
if uploaded_file:
    image_data = input_image_setup(uploaded_file)

    if scene_button:
        with st.spinner("Generating scene description..."):
            response = generate_scene_description(input_prompt, image_data)
            st.subheader("Scene Description")
            st.write(response)

            # Convert the scene description to speech
            st.write("🔊 Audio Output:")
            engine.save_to_file(response, 'scene_description.mp3')
            engine.runAndWait()

            # Play audio
            audio_file = open('scene_description.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.success("Scene description read aloud!")

    if tts_button:
        with st.spinner("Converting scene description to speech..."):
            # Generate the scene description for Text-to-Speech conversion
            scene_description = generate_scene_description(input_prompt, image_data)

            # Show the generated scene description as text
            st.subheader("Scene Description ✍️:")
            st.text(scene_description)

            # Convert text to speech
            st.write("🔊 Audio Output:")
            engine.save_to_file(scene_description, 'scene_description.mp3')
            engine.runAndWait()

            # Play audio
            audio_file = open('scene_description.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.success("Text-to-Speech Conversion Completed!")

    if task_button:
        with st.spinner("Generating personalized assistance..."):
            # Generate task-specific guidance based on the uploaded image
            task_guidance = generate_task_guidance_assistant(input_prompt, image_data)

            # Show the generated task guidance as text
            st.subheader("Personalized Assistance_For_Daily_Tasks ✍️:")
            st.text(task_guidance)

            # Convert task guidance to speech
            st.write("🔊 Audio Output:")
            engine.save_to_file(task_guidance, 'task_guidance_assistant.mp3')
            engine.runAndWait()

            # Play audio
            audio_file = open('task_guidance_assistant.mp3', 'rb')
            audio_bytes = audio_file.read()
            st.audio(audio_bytes, format="audio/mp3")
            st.success("Task guidance_assistant read aloud!")

# Add footer with project details and icons
st.markdown("""
    <footer style= padding:20px; text-align:center; font-size:14px;">
        <p><strong>AI Assistant for Visually Impaired</strong> | <i class="fas fa-cogs"></i> Features</p>
        <p>
            <i class="fas fa-eye"></i> Scene Understanding | 
            <i class="fas fa-volume-up"></i> Text-to-Speech | 
            <i class="fas fa-hand-paper"></i> Personalized Assistance |
            <i class="fas fa-exclamation-circle"></i> Object & Obstacle Detection
        </p>
        <p>Made with ❤️ for visually impaired users. &copy; 2024</p>
    </footer>
""", unsafe_allow_html=True)
