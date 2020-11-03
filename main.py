import speech_recognition as sr
import audioop
import pyaudio as pa
import pyttsx3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser

import pandas as pd
import os

# Self defined modules
from modules import speechToText


print("Please speak out the food item")
r = sr.Recognizer()
string = speechToText(r)
print(string)

print("Please speak out the FDC ID of ", string, " you would like to know")
url = 'https://fdc.nal.usda.gov/fdc-app.html#/?query=' + string
webbrowser.open(url) 

# Program will wait until spoken
format1 = pa.paInt16
rate = 16000
channel = 1
chunk = 1024
threshold = 500

# intialise microphone stream
audio = pa.PyAudio()
stream = audio.open(format=format1, 
                    channels=channel,
                    rate=rate,
                    input=True,
                    frames_per_buffer=chunk)

while True:
    data = stream.read(chunk)
    rms = audioop.rms(data,2) #get input volume
    if rms > threshold: #if input volume greater than threshold
        #print(rms, threshold, " Detected")
        break
r1 = sr.Recognizer()
string1 = speechToText(r1)
#string1 = string.replace(" ", "")
url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + string1 + '/nutrients'
print(string1)
webbrowser.open(url) 

# Export datafile into the data frame
#path = r"C:\Users\dfsdfsdsdf\Desktop\NLP\nutrition-assistant"
#path1 = r"data\FoodData_Central_foundation_food_csv_2020-04-29"
#data = os.path.join(path, path1, "food.csv")

#df = pd.read_csv(data)
#print(df.head())