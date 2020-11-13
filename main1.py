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
    string = speechToText(r, source2)
    print(string)
    words = string.split()
#string = "I cheese"
string = string.upper()
words = string.split()

path = r"C:\Users\dfsdfsdsdf\Desktop\NLP\nutrition-assistant"
path1 = r"data\FoodData_Central_foundation_food_csv_2020-04-29"
data = os.path.join(path, path1, "food.csv")
df = pd.read_csv(data)
df = df.drop_duplicates(subset = ["description"])
df["description"] = df["description"].str.upper()
df["description"] = df["description"].str.split(", | | -")
#print(df["description"])
df1 = pd.DataFrame(columns = ['fdc_id', 'description']) 
for word in words:
    df['flag'] = df.apply(lambda x: int(word in x['description']), axis=1)
    df1 = df1.append(df[df['flag'] == 1].iloc[1:2,[0, 2]])

for ids in df1["fdc_id"]:
    ids = str(ids)
    url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + ids + '/nutrients'
    webbrowser.open(url)

    



    
    
    
