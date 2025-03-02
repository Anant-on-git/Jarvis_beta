import speech_recognition as sr
import pyttsx3
import weaviate
import threading
import time
import os
from weaviate.connect import ConnectionParams
from langchain.chat_models import ChatOllama
from langchain.schema import AIMessage, HumanMessage

# Initialize speech engine
engine = pyttsx3.init()

# Weaviate Client Setup
client = weaviate.WeaviateClient(
    connection_params=ConnectionParams.from_url(
        url="https://6t5iqoxszkoqfrzd3jvq.c0.asia-southeast1.gcp.weaviate.cloud",
        grpc_port=8080  # Default gRPC port for cloud instances
    )
)

# Initialize LangChain Ollama Model
chat_model = ChatOllama(model="mistral")

def speak(text):
    """Convert text to speech."""
    engine.say(text)
    engine.runAndWait()

def listen():
    """Listen for commands with a 5-second timeout."""
    recognizer = sr.Recognizer()
    recognizer.energy_threshold = 300  # Adjust sensitivity
    with sr.Microphone() as source:
        print("Listening for 5 seconds...")
        recognizer.adjust_for_ambient_noise(source, duration=1.5)  # Longer adjustment for noise
        try:
            audio = recognizer.listen(source, timeout=5)
            with open("test.wav", "wb") as f:
                f.write(audio.get_wav_data())  # Save audio for debugging
            command = recognizer.recognize_google(audio).lower()
            print(f"Heard: {command}")
            return command
        except sr.WaitTimeoutError:
            print("No command detected within 5 seconds. Turning off.")
            return ""
        except sr.UnknownValueError:
            print("Could not understand audio.")
            return ""
        except sr.RequestError:
            print("Speech service unavailable.")
            return ""

def chat_with_ollama(prompt):
    """Generate AI response using LangChain with Ollama."""
    try:
        response = chat_model([HumanMessage(content=prompt)])
        return response.content.strip()
    except Exception as e:
        print("Error communicating with Ollama:", e)
        return "I'm having trouble processing that."

def process_command():
    """Process user commands once assistant is activated."""
    command = listen()
    if not command:
        return
    if command.lower() == "exit":
        speak("Goodbye!")
        return
    response = chat_with_ollama(command)
    print("Assistant:", response)
    speak(response)

if __name__ == "__main__":
    while True:
        input("Press Enter to activate assistant...")
        process_command()
 """coding ends here"""