import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import google.generativeai as genai

# Configure Gemini API
GEMINI_API_KEY = 'AIzaSyAaYG20ej1AuJPzvp7nsxEwVzJoYkcC5xU'  
genai.configure(api_key=GEMINI_API_KEY)

class SimpleSpeechAI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        pygame.mixer.init()
        
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"You said: {text}")
                return text.lower()
            except:
                print("Could not understand audio")
                return ""
    
    def speak(self, text):
        print(f"AI: {text}")
        filename = f"response_{os.getpid()}.mp3"
        try:
            tts = gTTS(text=text, lang='en', tld='co.in')
            tts.save(filename)
            pygame.mixer.music.load(filename)
            pygame.mixer.music.play()
            while pygame.mixer.music.get_busy():
                pygame.time.Clock().tick(10)
            pygame.mixer.music.unload()
            if os.path.exists(filename):
                os.remove(filename)
        except Exception as e:
            print(f"Speech error: {e}")
    
    def get_ai_response(self, user_input):
        prompt = f"""You are a friendly AI assistant speaking in Hinglish (mix of Hindi and English).
        Keep responses very short and conversational.
        User said: {user_input}
        Respond naturally in 1-2 sentences."""
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except:
            return "Sorry, I'm having trouble understanding. Can you try again?"
    
    def start_conversation(self):
        print("Simple Speech AI Started")
        print("Say 'bye' to exit")
        
        # Initial greeting
        greeting = "Hello! Main ek AI assistant hun. How can I help you today?"
        self.speak(greeting)
        
        while True:
            user_input = self.listen()
            
            if user_input and any(word in user_input for word in ["bye", "goodbye", "exit"]):
                self.speak("Goodbye! Have a great day!")
                break
                
            if user_input:
                response = self.get_ai_response(user_input)
                self.speak(response)

def main():
    ai = SimpleSpeechAI()
    ai.start_conversation()

if __name__ == "__main__":
    main()