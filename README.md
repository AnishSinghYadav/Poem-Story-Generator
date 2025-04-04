# Poem-Story-Generator
# AI Literary Creator

## Overview
AI Literary Creator is a Streamlit web application that allows users to generate AI-powered poems and stories. It incorporates OpenAI's GPT model for text generation and TTS (text-to-speech) functionality to convert generated content into speech.

## Features
- **Poem Generation**: Create AI-generated poems based on user-input topics, styles, and lengths.
- **Story Generation**: Generate structured stories with specified titles, chapters, and authors.
- **Topic Restrictions**: Parents can specify allowed topics for poem generation.
- **Text-to-Speech (TTS)**: Convert generated poems and stories into speech using OpenAI TTS.
- **Session Management**: Users have a limited number of attempts (10 per session) to generate content.

## Installation
### Prerequisites
Ensure you have Python installed along with the required dependencies.

### Setup
1. Clone the repository or copy the script.
2. Install the required dependencies:
   ```sh
   pip install streamlit openai fpdf python-dotenv requests
   ```
3. Create a `.env` file in the root directory and add your OpenAI API key:
   ```env
   OPENAI_API_KEY=your_api_key_here
   ```
4. Run the Streamlit app:
   ```sh
   streamlit run app.py
   ```

## Usage
1. **Parent Settings**
   - Enter allowed topics for poem generation.
   - Manage topics in the sidebar.

2. **Creating a Poem**
   - Choose "Create a Poem."
   - Enter a topic, select a style, and choose a length.
   - Generate and edit the poem.

3. **Creating a Story**
   - Choose "Create a Story."
   - Enter a title, specify the number of chapters, and provide an author name.
   - Generate and edit the story.

4. **Text-to-Speech (TTS)**
   - Select a generated poem or story.
   - Choose a voice and speed.
   - Convert text to speech and listen to the generated audio.

## Dependencies
- `streamlit`
- `openai`
- `fpdf`
- `python-dotenv`
- `requests`

## License
This project is licensed under the MIT License.

## Author
Developed by Anish and Yuvika

