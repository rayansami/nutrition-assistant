import speech_recognition as sr
import pyttsx3
import requests
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import webbrowser


from modules import speechToText

r = sr.Recognizer()

string = speechToText(r)

print(string)



url = 'https://fdc.nal.usda.gov/fdc-app.html#/?query=' + string
webbrowser.open(url) 

