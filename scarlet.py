from gtts import gTTS
import speech_recognition as sr 
from pygame import mixer
import random, re, requests, bs4, os, time
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import urllib.request
import urllib.parse
from datetime import date, datetime


# using count here to switch between audio0 and audio1 
# because when we used only one file - audio.mp3, TTS was already using that file once 
# and couldn't find way to open it again. So now when we have two files,
# TTS switches between both files which makes space of one file to open up and the other to close 
count = 0

sleepFlag = False

# the voice system of Scarlet
def talk(audio):
    global count 
    print(audio)
    file = f'audio{count%2}.mp3'
    for line in audio.splitlines():
        textToSpeech = gTTS(text=audio, lang='en-US')
        textToSpeech.save(file)
        mixer.init()
        mixer.music.load(file)
        mixer.music.play()
        count += 1

    
def listenCommand():
    r = sr.Recognizer()

    with sr.Microphone() as source:
        print("...")
        r.pause_threshold = 1
        # this waits and adjusts our voice energy threshold to the surrounding noise level
        r.adjust_for_ambient_noise(source, duration=1)

        # listens for the users input
        audio = r.listen(source)

    try:
        command = r.recognize_google(audio).lower()
        print('You said - ' + command + '\n')

    # loop back to continue to listen for commands if unrecognizable speech is received 
    except sr.UnknownValueError:
        print('Sorry your last command couldn\'t be heard')
        command = listenCommand()

    return command

def googleSearch(searchFor):
    
    talk('Okay searching...')
    
    # Add the path to chromedriver.exe below in the executable_path variable
    driver = webdriver.Chrome(executable_path="")
    driver.get('http://www.google.com')
    search = driver.find_element_by_name('q')
    search.send_keys(str(searchFor))
     # hit return after you enter search text
    search.send_keys(Keys.RETURN)

def openApplication(command):

    if 'chrome' in command:
        talk("Opening Chrome...")
        # add the path of chrome.exe from your system below
        os.startfile("")
        return 
    
    elif 'vba' in command or 'vs code' in command or 'visual studio code' in command: 
        talk("Opening VS Code...")
        # add the path of code.exe from your system below
        os.startfile("")
        return 
    
    elif 'command prompt' in command or 'command line' in command or 'cmd' in command:
        talk("Opening Command Line...")
        # add the path of cmd.exe from your system below
        os.startfile("")
        return

    elif 'open my programming space' in command: 
        talk("Initializing your programming space...")

        # add the path of chrome.exe from your system below
        # add the path of code.exe from your system below
        # add the path of cmd.exe from your system below
        os.startfile("")
        os.startfile("")
        os.startfile("")

        time.sleep(5)
        return 

def scarlet(command): 

    global sleepFlag
    errors = [
        "I don't know what you mean",
        "That is outside the scope of my development but I will definitely let my developer know to include that!",
        "Can you repeat it please?",
    ]

    if 'sleep scarlet' in command:
        talk("Wake me up when you need me. Nighty night")
        sleepFlag = True

    if 'hey scarlet' in command:
        
        talk("Hey! How can I help you?")
        sleepFlag = False

    elif not sleepFlag:
        if 'hello' == command or 'hey' == command:
            talk("Hey! How can I help you?")

        elif 'who are you' in command:
            talk("I'm Scarlet, your personal virtual assistant")

        elif 'who created you' in command or 'who made you' in command:
            talk("I am created by Utkarsh")

        elif 'how are you' in command:
            talk("I'm great! How about you?")
        
        elif 'open google and search for' in command or 'open google and search' in command: 
            if 'open google and search for' in command: 
                google = re.search('open google and search for (.*)', command)
                searchFor = command.split("for",1)[1]
                if google:
                    googleSearch(searchFor)
            else:
                google = re.search('open google and search (.*)', command)
                searchFor = command.split("search",1)[1]
                if google:
                    googleSearch(searchFor)
        
        elif 'open' in command: 
            openApplication(command)
            if 'open my programming space' in command:
                talk("Do you want me to start music for you?")
                scarlet(listenCommand())

        elif 'yes start music' in command: 
            os.system('start Spotify')

        elif 'the time' in command:

            talk(datetime.now().strftime("%I:%M %p"))
            
        elif 'the date' in command:
            talk(date.today().strftime("%B %d, %Y"))
        
        elif 'the year' in command:
            talk(date.today().strftime("%Y"))

        elif 'the month' in command:
            talk(date.today().strftime("%B"))
        
        elif 'the day' in command:
            talk(date.today().strftime("%d"))

        else:
            error = random.choice(errors)
            talk(error)

# Activating scarlet
talk('Scarlet is ready!')

while True:    
    scarlet(listenCommand())
    
 
