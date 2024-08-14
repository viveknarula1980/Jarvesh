import speech_recognition as sr
import os
import webbrowser
import openai
from config import apikey
import datetime
import random
import numpy as np

chatStr = ""

# Function to interact with OpenAI's GPT-3 model and get a chat response
def chat(query):
    global chatStr
    print("Current conversation:\n", chatStr)
    openai.api_key = apikey
    chatStr += f"User: {query}\nJarvis: "
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=chatStr,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    # Send the response back to the user and update the conversation history
    say(response["choices"][0]["text"])
    chatStr += f"{response['choices'][0]['text']}\n"
    return response["choices"][0]["text"]

# Function to get a response from OpenAI based on a given prompt
def ai(prompt):
    openai.api_key = apikey
    text = f"OpenAI response for prompt: {prompt}\n*************************\n\n"
    
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        temperature=0.7,
        max_tokens=256,
        top_p=1,
        frequency_penalty=0,
        presence_penalty=0
    )
    
    text += response["choices"][0]["text"]
    
    # Create a directory for OpenAI responses if it doesn't exist
    if not os.path.exists("Openai"):
        os.mkdir("Openai")

    # Save the response to a file named after the prompt
    with open(f"Openai/{''.join(prompt.split('intelligence')[1:]).strip()}.txt", "w") as f:
        f.write(text)

# Function to use the system's speech synthesis to say the text aloud
def say(text):
    os.system(f'say "{text}"')

# Function to take a voice command from the user
def takeCommand():
    r = sr.Recognizer()
    with sr.Microphone() as source:
        print("Listening for user command...")
        audio = r.listen(source)
        try:
            print("Recognizing speech...")
            query = r.recognize_google(audio, language="en-in")
            print(f"User said: {query}")
            return query
        except Exception as e:
            return "An error occurred. Sorry from Jarvis."

# Main loop to run the Jarvis A.I. assistant
if __name__ == '__main__':
    print('Welcome to Jarvis A.I')
    say("Jarvis A.I")
    
    while True:
        query = takeCommand()
        
        # Predefined sites that Jarvis can open
        sites = [
            ["youtube", "https://www.youtube.com"], 
            ["wikipedia", "https://www.wikipedia.com"], 
            ["google", "https://www.google.com"],
        ]
        
        # Check if the user asked to open any predefined sites
        for site in sites:
            if f"Open {site[0]}".lower() in query.lower():
                say(f"Opening {site[0]}...")
                webbrowser.open(site[1])
        
        # Check if the user asked to play music
        if "open music" in query.lower():
            musicPath = "/Users/harry/Downloads/downfall-21371.mp3"
            os.system(f"open {musicPath}")

        # Check if the user asked for the current time
        elif "the time" in query.lower():
            hour = datetime.datetime.now().strftime("%H")
            minute = datetime.datetime.now().strftime("%M")
            say(f"The current time is {hour} hours and {minute} minutes.")

        # Check if the user asked to open FaceTime
        elif "open facetime" in query.lower():
            os.system(f"open /System/Applications/FaceTime.app")

        # Check if the user asked to open a specific application
        elif "open pass" in query.lower():
            os.system(f"open /Applications/Passky.app")

        # Check if the user mentioned artificial intelligence to trigger AI response
        elif "using artificial intelligence" in query.lower():
            ai(prompt=query)

        # Check if the user asked Jarvis to quit
        elif "jarvis quit" in query.lower():
            exit()

        # Check if the user wants to reset the chat history
        elif "reset chat" in query.lower():
            chatStr = ""

        # If the query doesn't match any of the above, use the chat function
        else:
            print("Processing chat response...")
            chat(query)
