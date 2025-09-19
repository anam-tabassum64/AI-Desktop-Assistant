import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import pyttsx3
import time

chatStr = ""

openai.api_key = apikey
engine = pyttsx3.init()

def say(text):
    engine.say(text)
    engine.runAndWait()

def chat(query):
    global chatStr
    print(chatStr)
    chatStr += f"Harry: {query}\n Jarvis: "
    retry_delay = 1
    max_retries = 5

    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "system", "content": "You are Jarvis AI assistant."},
                    {"role": "user", "content": chatStr}
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            text_response = response['choices'][0]['message']['content']
            say(text_response)
            chatStr += f"{text_response}\n"
            return text_response
        except Exception as e:
            if "RateLimit" in str(e) or "rate limit" in str(e).lower():
                print(f"Rate limit hit. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("Error:", e)
                say("Sorry, I encountered an error. Please try again later.")
                break

    say("Sorry, I am experiencing high demand. Please try again later.")
    return "Rate limit exceeded."

def ai(prompt):
    text = f"OpenAI response for Prompt: {prompt} \n *************************\n\n"
    retry_delay = 1
    max_retries = 5
    for attempt in range(max_retries):
        try:
            response = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages=[
                    {"role": "user", "content": prompt}
                ],
                temperature=0.7,
                max_tokens=256,
                top_p=1,
                frequency_penalty=0,
                presence_penalty=0
            )
            text_response = response['choices'][0]['message']['content']
            text += text_response
            if not os.path.exists("Openai"):
                os.mkdir("Openai")
            with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
                f.write(text)
            return text_response
        except Exception as e:
            if "RateLimit" in str(e) or "rate limit" in str(e).lower():
                print(f"Rate limit hit. Retrying in {retry_delay} seconds...")
                time.sleep(retry_delay)
                retry_delay *= 2
            else:
                print("Error:", e)
                say("Sorry, I encountered an error. Please try again later.")
                return "Error"
    say("Sorry, I am experiencing high demand. Please try again later.")
    return "Rate limit exceeded."

def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        r.adjust_for_ambient_noise(source)
        r.pause_threshold = 1
        print("Listening...")
        audio = r.listen(source)
        try:
            print("Recognizing...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except sr.UnknownValueError:
            print("Google Speech Recognition could not understand audio")
            return "Sorry, I didn't catch that."
        except sr.RequestError as e:
            print(f"Could not request results from Google Speech Recognition service; {e}")
            return "Sorry, I am having trouble connecting to the speech service."
        except Exception as e:
            print(f"Speech recognition error: {e}")
            return "Some Error Occurred. Sorry from Jarvis"

if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    while True:
        query = takeCommand()
        sites = [["youtube", "https://www.youtube.com"], ["wikipedia", "https://www.wikipedia.com"], ["google", "https://www.google.com"]]
        for site in sites:
            if f"open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]} sir...")
                webbrowser.open(site[1])

        if "open music" in query.lower():
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"  # Update as needed
            os.system(f"start {musicPath}")  # For Windows, use 'start'

        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"Sir, time is {hour} bajke {minute} minutes")

        elif "open facetime" in query.lower():
            os.system("start /System/Applications/FaceTime.app")  # Update path for Windows

        elif "open pass" in query.lower():
            os.system("start /Applications/Passky.app")  # Update path for Windows

        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        elif "jarvis quit" in query.lower():
            exit()

        elif "reset chat" in query.lower():
            chatStr = ""

        else:
            print("Chatting...")
            chat(query)
