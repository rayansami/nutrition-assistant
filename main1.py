import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser
import time
import pandas as pd
import os 
import audioop
import pyaudio as pa
import re

# Self defined modules
from modules1 import speechToText

engine = pyttsx3.init()

#voice_id ="HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_RU-RU_IRINA_11.0"
#engine.setProperty('voice', voice_id) 

voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" 
engine.setProperty('voice', voice_id) 
engine.say("Please speak out the food item") 
engine.runAndWait()

r = sr.Recognizer()
with sr.Microphone() as source2:
    userVoiceInText = speechToText(r, source2)
    print("Voice to Text test:",userVoiceInText)    
    
#string = "I cheese"
userVoiceInText = userVoiceInText.upper()
words = userVoiceInText.split()

# Get the food CSV using absolute path 
cwd = os.getcwd() # gets the current working directory
foodData = os.path.realpath(r"food.csv") # gives absolute path regardless the OS


df = pd.read_csv(foodData)
df = df.drop_duplicates(subset = ["description"])  # Drop any description duplicates
df["description"] = df["description"].str.upper()
df["description"] = df["description"].str.split(", | | -")
#print(df["description"])

""" 
 TODO: Revisit this section for future optimization
"""
df1 = pd.DataFrame(columns = ['fdc_id', 'description']) 
# For each word got over the voice, go over the Food-data and get FDC-ID
for word in words:
    df['flag'] = df.apply(lambda x: int(word in x['description']), axis=1)
    df1 = df1.append(df[df['flag'] == 1].iloc[1:2,[0, 2]])

# Call on webbrowser and reachout FDC website with the filtered out fdc-id
for ids in df1["fdc_id"]:
    ids = str(ids)
    url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + ids + '/nutrients'
    webbrowser.open(url)

    



    
    
    
