import streamlit as st
import openai
import base64
import tempfile
import os
from io import BytesIO
from fpdf import FPDF
import requests
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Retrieve OpenAI API Key from environment
openai.api_key = os.getenv("OPENAI_API_KEY")

if not openai.api_key:
    st.error("OpenAI API key is missing. Please set it in the .env file.")
# Available TTS Voices
openai_voices = ["alloy", "echo", "fable", "onyx", "nova", "shimmer"]

# Session State for Enhanced Functionality
if 'attempts_left' not in st.session_state:
    st.session_state.attempts_left = 10
if 'allowed_topics' not in st.session_state:
    st.session_state.allowed_topics = []
if 'generated_poem' not in st.session_state:
    st.session_state.generated_poem = ""
if 'generated_story' not in st.session_state:
    st.session_state.generated_story = ""
if 'audio_content' not in st.session_state:
    st.session_state.audio_content = None
if 'edited_text' not in st.session_state:
    st.session_state.edited_text = ""

def check_topic_relevance(child_input):
    prompt = f"Determine if the topic '{child_input}' is related to the following approved topics: {', '.join(st.session_state.allowed_topics)}. Respond with 'Yes' or 'No'."
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content.strip().lower() == "yes"

def generate_story(title, chapters, author):
    prompt = f"Write a structured story titled '{title}' with {chapters} chapters, including dialogues, emotions, and detailed descriptions. Author: {author}."
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_poem(topic, style, length):
    style_prompt = {
        "Rhyming": "Write a rhyming poem.",
        "Free Verse": "Write a deep, emotional free-verse poem.",
        "Haiku": "Write a haiku (5-7-5 syllable format)."
    }
    
    length_prompt = {
        "Short": "Make it concise and meaningful.",
        "Medium": "Make it moderately detailed with strong imagery.",
        "Long": "Make it expressive, vivid, and deep."
    }
    
    prompt = f"{style_prompt[style]} {length_prompt[length]} Write a poem about {topic}"
    
    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "system", "content": prompt}]
    )
    return response.choices[0].message.content

def generate_tts(text, voice="alloy", speed="1.0"):
    response = openai.audio.speech.create(
        model="tts-1",
        voice=voice,
        input=text,
        speed=float(speed)
    )
    return response.content

def main():
    st.title("AI Literary Creator")
    
    # Display remaining attempts
    st.sidebar.header(f"Attempts Left: {st.session_state.attempts_left}/10")
    
    # Parent Interface
    st.sidebar.header("Parent Settings")
    allowed_topic = st.sidebar.text_input("Enter an allowed topic:")
    if st.sidebar.button("Add Topic"):
        if allowed_topic and allowed_topic not in st.session_state.allowed_topics:
            st.session_state.allowed_topics.append(allowed_topic)
    
    st.sidebar.write("**Allowed Topics:**", st.session_state.allowed_topics)
    
    choice = st.radio("Choose an option:", ("Create a Poem", "Create a Story"))
    
    if st.session_state.attempts_left > 0:
        if choice == "Create a Poem":
            st.subheader("Poem Generator")
            if not st.session_state.allowed_topics:
                st.warning("No topics available. Parents need to set allowed topics first.")
                return
            
            poem_topic = st.text_input("Enter a topic for your poem:")
            poem_style = st.radio("Choose a Poem Style:", ["Rhyming", "Free Verse", "Haiku"])
            poem_length = st.select_slider("Select Poem Length:", options=["Short", "Medium", "Long"])
            
            if st.button("Generate Poem"):
                if check_topic_relevance(poem_topic):
                    st.session_state.generated_poem = generate_poem(poem_topic, poem_style, poem_length)
                    st.session_state.edited_text = st.session_state.generated_poem
                    st.session_state.attempts_left -= 1
                else:
                    st.error("The above topic is not accepted.")
            
            st.text_area("Edit Your Poem:", key="edited_text", height=300)
        
        elif choice == "Create a Story":
            st.subheader("Story Generator")
            story_title = st.text_input("Enter a Story Title:")
            story_chapters = st.slider("Number of Chapters:", 1, 10, 3)
            story_author = st.text_input("Author Name:")
            
            if st.button("Generate Story"):
                st.session_state.generated_story = generate_story(story_title, story_chapters, story_author)
                st.session_state.edited_text = st.session_state.generated_story
                st.session_state.attempts_left -= 1
            
            st.text_area("Edit Your Story:", key="edited_text", height=300)
        
        voice_choice = st.selectbox("Choose Voice for TTS:", openai_voices)
        speed_choice = st.select_slider("TTS Speed:", options=["0.75", "1.0", "1.25"], value="1.0")
        text_to_convert = st.radio("Select Content for TTS:", ("Poem", "Story"))
        
        if st.button("Convert to Speech"):
            if text_to_convert == "Poem" and st.session_state.edited_text:
                st.session_state.audio_content = generate_tts(st.session_state.edited_text, voice=voice_choice, speed=speed_choice)
            elif text_to_convert == "Story" and st.session_state.edited_text:
                st.session_state.audio_content = generate_tts(st.session_state.edited_text, voice=voice_choice, speed=speed_choice)
            
            if st.session_state.audio_content:
                st.audio(st.session_state.audio_content, format="audio/mp3")
    else:
        st.error("You have reached the maximum of 10 attempts per session.")

if __name__ == "__main__":
    main()
