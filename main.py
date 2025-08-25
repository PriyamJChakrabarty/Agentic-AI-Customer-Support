import speech_recognition as sr
from gtts import gTTS
import pygame
import os
import google.generativeai as genai
from dotenv import load_dotenv
import json

load_dotenv()

GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")
genai.configure(api_key=GEMINI_API_KEY)

class IIITAllahabadAdmissionAI:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.model = genai.GenerativeModel("gemini-1.5-flash")
        pygame.mixer.init()
        
        self.admission_data = {
            "courses": {
                "btech": {
                    "name": "Bachelor of Technology",
                    "branches": ["Computer Science Engineering", "Electronics and Communication Engineering", 
                               "Information Technology", "Artificial Intelligence"],
                    "duration": "4 years",
                    "seats": 480,
                    "fee": "₹1,25,000 per semester"
                },
                "mtech": {
                    "name": "Master of Technology",
                    "branches": ["Computer Science", "Electronics and Communication", 
                               "Artificial Intelligence", "Cybersecurity"],
                    "duration": "2 years", 
                    "seats": 120,
                    "fee": "₹95,000 per semester"
                },
                "phd": {
                    "name": "Doctor of Philosophy",
                    "branches": ["Computer Science", "Electronics", "Mathematics", "Physics"],
                    "duration": "3-6 years",
                    "seats": 60,
                    "fee": "₹25,000 per semester"
                }
            },
            
            "admission_process": {
                "btech": "JEE Main rank-based admission through JoSAA counselling",
                "mtech": "GATE score required, followed by institute counselling", 
                "phd": "Written test and interview, minimum 60% in qualifying degree"
            },
            
            "eligibility": {
                "btech": "12th pass with Physics, Chemistry, Mathematics. Minimum 75% aggregate",
                "mtech": "Bachelor's degree in relevant engineering field with minimum 60%",
                "phd": "Master's degree in relevant field with minimum 60% or GATE qualification"
            },
            
            "cutoffs_2024": {
                "btech_cse": "JEE Main rank: 8000-12000 (General), 15000-20000 (OBC), 25000-35000 (SC/ST)",
                "btech_ece": "JEE Main rank: 12000-18000 (General), 20000-28000 (OBC), 35000-45000 (SC/ST)",
                "mtech_cse": "GATE score: 650+ (General), 550+ (OBC), 450+ (SC/ST)"
            },
            
            "important_dates": {
                "application_start": "March 15, 2025",
                "application_deadline": "May 20, 2025", 
                "entrance_exam": "June 1-15, 2025",
                "counselling": "July 10-25, 2025",
                "classes_start": "August 1, 2025"
            },
            
            "facilities": [
                "24/7 WiFi campus",
                "Modern computer labs with latest software",
                "Well-stocked library with digital resources", 
                "Sports facilities including cricket, football, basketball courts",
                "Separate hostels for boys and girls",
                "Medical center with qualified doctors",
                "Canteen with hygienic food",
                "Placement cell with 85% placement record"
            ],
            
            "placement_stats": {
                "average_package": "₹12.5 lakhs per annum",
                "highest_package": "₹45 lakhs per annum", 
                "top_recruiters": ["Google", "Microsoft", "Amazon", "TCS", "Infosys", "Wipro", "Adobe", "Samsung"],
                "placement_percentage": "85%"
            },
            
            "contact_info": {
                "address": "IIIT Allahabad, Jhalwa, Prayagraj, Uttar Pradesh - 211015",
                "phone": "+91-532-2922000",
                "email": "admissions@iiita.ac.in",
                "website": "www.iiita.ac.in"
            }
        }
        
    def listen(self):
        with sr.Microphone() as source:
            print("Listening...")
            self.recognizer.adjust_for_ambient_noise(source)
            try:
                audio = self.recognizer.listen(source, timeout=10)
                text = self.recognizer.recognize_google(audio, language="en-IN")
                print(f"You said: {text}")
                return text.lower()
            except sr.WaitTimeoutError:
                print("Listening timeout")
                return ""
            except sr.UnknownValueError:
                print("Could not understand audio")
                return ""
            except Exception as e:
                print(f"Error: {e}")
                return ""
    
    def speak(self, text):
        print(f"IIIT Assistant: {text}")
        filename = f"iiit_response_{os.getpid()}.mp3"
        try:
            tts = gTTS(text=text, lang='en', tld='co.in', slow=False)
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
    
    def find_relevant_data(self, user_input):
        """Extract relevant admission data based on user query"""
        relevant_info = ""
        
        if any(word in user_input for word in ["course", "courses", "branch", "branches", "program"]):
            if "btech" in user_input or "bachelor" in user_input or "engineering" in user_input:
                course_info = self.admission_data["courses"]["btech"]
                relevant_info += f"B.Tech courses: {', '.join(course_info['branches'])}. Duration: {course_info['duration']}. Total seats: {course_info['seats']}. Fee: {course_info['fee']}. "
            elif "mtech" in user_input or "master" in user_input:
                course_info = self.admission_data["courses"]["mtech"] 
                relevant_info += f"M.Tech courses: {', '.join(course_info['branches'])}. Duration: {course_info['duration']}. Total seats: {course_info['seats']}. Fee: {course_info['fee']}. "
            elif "phd" in user_input or "doctorate" in user_input:
                course_info = self.admission_data["courses"]["phd"]
                relevant_info += f"PhD programs: {', '.join(course_info['branches'])}. Duration: {course_info['duration']}. Total seats: {course_info['seats']}. Fee: {course_info['fee']}. "
            else:
                relevant_info += "Available courses: B.Tech, M.Tech, and PhD in various specializations. "
        
        if any(word in user_input for word in ["admission", "process", "how to apply", "apply"]):
            if "btech" in user_input:
                relevant_info += f"B.Tech admission: {self.admission_data['admission_process']['btech']}. "
            elif "mtech" in user_input:
                relevant_info += f"M.Tech admission: {self.admission_data['admission_process']['mtech']}. "
            elif "phd" in user_input:
                relevant_info += f"PhD admission: {self.admission_data['admission_process']['phd']}. "
            else:
                relevant_info += "Admission processes vary by course. B.Tech through JEE Main, M.Tech through GATE, PhD through entrance test. "
        
        if any(word in user_input for word in ["eligibility", "eligible", "qualification", "requirement"]):
            if "btech" in user_input:
                relevant_info += f"B.Tech eligibility: {self.admission_data['eligibility']['btech']}. "
            elif "mtech" in user_input:
                relevant_info += f"M.Tech eligibility: {self.admission_data['eligibility']['mtech']}. "
            elif "phd" in user_input:
                relevant_info += f"PhD eligibility: {self.admission_data['eligibility']['phd']}. "
        
        if any(word in user_input for word in ["cutoff", "cut off", "rank", "score", "marks"]):
            if "cse" in user_input or "computer science" in user_input:
                relevant_info += f"CSE cutoffs 2024: {self.admission_data['cutoffs_2024']['btech_cse']}. "
            elif "ece" in user_input or "electronics" in user_input:
                relevant_info += f"ECE cutoffs 2024: {self.admission_data['cutoffs_2024']['btech_ece']}. "
            elif "mtech" in user_input:
                relevant_info += f"M.Tech CSE cutoffs 2024: {self.admission_data['cutoffs_2024']['mtech_cse']}. "
            else:
                relevant_info += "2024 cutoffs available for CSE, ECE branches. Varies by category. "
        
        if any(word in user_input for word in ["date", "dates", "when", "deadline", "timeline"]):
            dates = self.admission_data["important_dates"]
            relevant_info += f"Important dates: Application starts {dates['application_start']}, deadline {dates['application_deadline']}, exam {dates['entrance_exam']}, counselling {dates['counselling']}, classes start {dates['classes_start']}. "
        
        if any(word in user_input for word in ["fee", "fees", "cost", "expense", "money"]):
            relevant_info += f"Fees: B.Tech {self.admission_data['courses']['btech']['fee']}, M.Tech {self.admission_data['courses']['mtech']['fee']}, PhD {self.admission_data['courses']['phd']['fee']}. "
        
        if any(word in user_input for word in ["facility", "facilities", "campus", "hostel", "library"]):
            facilities = ', '.join(self.admission_data["facilities"][:4])  # First 4 facilities
            relevant_info += f"Campus facilities include: {facilities} and more. "
        
        if any(word in user_input for word in ["placement", "placements", "job", "salary", "package", "companies"]):
            placement = self.admission_data["placement_stats"]
            relevant_info += f"Placement stats: {placement['placement_percentage']} students placed, average package {placement['average_package']}, highest {placement['highest_package']}. Top recruiters: {', '.join(placement['top_recruiters'][:4])} and more. "
        
        if any(word in user_input for word in ["contact", "phone", "email", "address", "location"]):
            contact = self.admission_data["contact_info"]
            relevant_info += f"Contact details: Address - {contact['address']}, Phone - {contact['phone']}, Email - {contact['email']}, Website - {contact['website']}. "
        
        return relevant_info
    
    def get_ai_response(self, user_input):
        relevant_data = self.find_relevant_data(user_input)
        
        if relevant_data:
            prompt = f"""You are an IIIT Allahabad admission assistant speaking in formal yet friendly Hinglish (mix of Hindi and English).
            
            TONE GUIDELINES:
            - Use formal, respectful language appropriate for educational institution
            - Mix Hindi and English naturally but maintain professionalism
            - Avoid casual expressions like "arrey yaar", "bhai", "dekho", "achha", "matlab" 
            - Use respectful terms like "aap", "ji", "sir/madam" when appropriate
            - Keep responses concise (2-3 sentences) but informative
            - Sound helpful and courteous, like a professional admission counselor
            
            User asked: {user_input}
            Relevant admission data: {relevant_data}
            
            Answer the query using ONLY the provided data. Be helpful, formal yet friendly."""
        else:
            return "Maaf kijiye, mere paas ye information abhi available nahin hai. Kripaya admission office se contact kariye +91-532-2922000 par ya admissions@iiita.ac.in par email kariye."
        
        try:
            response = self.model.generate_content(prompt)
            return response.text
        except Exception as e:
            print(f"AI Error: {e}")
            return "Maaf kijiye, kuch technical issues aa rahe hain. Kripaya phir se try kariye ya admission office se contact kariye."
    
    def start_conversation(self):
        print("IIIT Allahabad Admission Assistant Started")
        print("Say 'bye' or 'goodbye' to exit")
        
        greeting = "Namaskar! Main IIIT Allahabad ki admission assistant hun. Aap ke admission related queries mein main aap ki help kar sakti hun. Kya jaanna chahte hain aap?"
        self.speak(greeting)
        
        while True:
            user_input = self.listen()
            
            if user_input and any(word in user_input for word in ["bye", "goodbye", "exit", "quit", "stop"]):
                farewell = "Dhanyawad! IIIT Allahabad mein admission ke liye contact kariye +91-532-2922000 par. Aap ka din shubh ho!"
                self.speak(farewell)
                break
                
            if user_input:
                response = self.get_ai_response(user_input)
                self.speak(response)
            else:
                self.speak("Main aap ki baat samajh nahin payi. Kripaya apna sawal repeat kar dijiye.")

def main():
    
    try:
        ai = IIITAllahabadAdmissionAI()
        ai.start_conversation()
    except KeyboardInterrupt:
        print("\nProgram stopped by user.")
    except Exception as e:
        print(f"Error starting assistant: {e}")
        print("Please ensure all dependencies are installed and API key is configured.")

if __name__ == "__main__":
    main()