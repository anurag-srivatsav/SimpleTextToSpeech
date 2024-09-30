import os
import google.generativeai as genai
from google.generativeai import configure
from gtts import gTTS
from IPython.display import Audio
import re
import random
import time
from textblob import TextBlob

# Set your API key as an environment variable
os.environ['GENAI_API_KEY'] = ''  # Replace with your actual API key

# Configure the SDK with the API key
api_key = os.getenv('GENAI_API_KEY')
if not api_key:
    raise ValueError("API key is missing. Please set it as an environment variable.")

configure(api_key=api_key)

# Function to clean the input text by removing special characters
def clean_text_for_speech(text):
    # Remove hashtags, asterisks, and any special characters that aren't relevant for speech
    cleaned_text = re.sub(r'[#*]', '', text)  # Removes # and * characters
    # Optionally, you can strip out other symbols or specific words if needed
    cleaned_text = re.sub(r'[_~^@]', '', cleaned_text)  # Add more symbols if required
    return cleaned_text.strip()

# Function to convert text to speech
def text_to_speech(text, lang='en', slow=False):
    try:
        # Clean the text before converting it to speech
        sanitized_text = clean_text_for_speech(text)
        # Convert cleaned text to speech
        tts = gTTS(text=sanitized_text, lang=lang, slow=slow)
        # Save the output audio
        tts.save("output.mp3")
        # Play the audio in Jupyter or Colab environment
        return Audio("output.mp3", autoplay=True)
    except Exception as e:
        print(f"Error during text-to-speech conversion: {e}")
        return None

# Function to detect emotion based on user input sentiment
def detect_emotion(input_text):
    sentiment = TextBlob(input_text).sentiment.polarity
    if sentiment > 0:
        return "Sounds great! Let me check..."
    elif sentiment < 0:
        return "Hmm, that's tricky. Let me think about it..."
    else:
        return random.choice(["Okay, now...", "Let me check that out..."])

# Function to generate a response based on emotion and add a human-like transitional phrase
def generate_emotion_based_response(input_text, response):
    transitional_phrase = detect_emotion(input_text)
    print(transitional_phrase)
    time.sleep(random.uniform(1, 3))  # Simulate thinking delay
    
    full_response = f"{transitional_phrase} {response}"
    return text_to_speech(full_response)

# Add a random thinking phrase before the actual response
def add_transitional_phrase():
    phrases = [
        "Let me think...",
        "Alright, give me a second...",
        "Okay, now...",
        "Hmm, let's see...",
        "Just a moment...",
    ]
    return random.choice(phrases)

# Function to simulate human-like response by adding random transitional phrases and delays
def generate_human_like_response(response):
    # Add a transitional phrase
    transitional_phrase = add_transitional_phrase()
    
    # Simulate thinking with a short delay
    print(transitional_phrase)
    time.sleep(2)  # Simulate a "thinking" pause
    
    # Combine the transitional phrase with the actual response
    full_response = f"{transitional_phrase} {response}"
    
    # Convert to speech
    return text_to_speech(full_response)

# Main interaction with Generative AI model
def generate_and_speak():
    # Model setup
    generation_config = {
        "temperature": 1,
        "top_p": 0.95,
        "top_k": 64,
        "max_output_tokens": 8192,
        "response_mime_type": "text/plain",
    }

    try:
        # Initialize the model
        model = genai.GenerativeModel(
            model_name="gemini-1.5-flash",
            generation_config=generation_config,
        )

        # Start the chat session
        chat_session = model.start_chat(history=[])
        input1 = input("Enter your query: ")

        # Get response from the model
        response = chat_session.send_message(input1)
        result = response.text
        print("Model response:", result)

        # Generate emotion-based response with human-like interactions
        emotion_response = generate_emotion_based_response(input1, result)

        if emotion_response:
            display(emotion_response)
        else:
            print("Unable to play the audio.")

    except Exception as e:
        print(f"An error occurred during model interaction: {e}")
#AIzaSyDzeATPLWRenJGapH8wOCtKEs_QFf6FPR0
# Run the function to generate and speak the response
generate_and_speak()
