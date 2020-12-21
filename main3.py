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
import nltk
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

import pprint
from nltk import Tree
import pdb
import api_calls

# Implementation of regex parser
#############################################################################
patterns="""
    NP: {<JJ>*<NN*>+}
    {<JJ>*<NN*><CC>*<NN*>+}
    {<NP><CC><NP>}
    {<RB><JJ>*<NN*>+}
    """

NPChunker = nltk.RegexpParser(patterns)

def prepare_text(string):
    sentences = nltk.sent_tokenize(string)
    sentences = [nltk.word_tokenize(sent) for sent in sentences] 
    sentences = [nltk.pos_tag(sent) for sent in sentences]
    sentences = [NPChunker.parse(sent) for sent in sentences]
    return sentences

def parsed_text_to_NP(sentences):
    nps = []
    for sent in sentences:
        tree = NPChunker.parse(sent)
        #print(tree)
        for subtree in tree.subtrees():
            if subtree.label() == 'NP':
                t = subtree
                t = ' '.join(word for word, tag in t.leaves())
                nps.append(t)
    return nps

def sent_parse(string):
    sentences = prepare_text(string)
    nps = parsed_text_to_NP(sentences)
    return nps
##############################################################################

# This function is to convert voice speech into string text
##############################################################################
def speechToText(r, source2):
    try:
        r.adjust_for_ambient_noise(source2, duration=0.2)
        audio2 = r.listen(source2)
        myText = r.recognize_google(audio2)
        myText = myText.lower()
        return myText
                
        #print("Did you say " + myText)
    except sr.RequestError as e:
        print("Could not request results; {0}".format(e))
            
    except sr.UnknownValueError:
        print("Unknown error occured")
##############################################################################        

def userCommand():
    r = sr.Recognizer() # Creating a recognizer instance
    # print(sr.Microphone.list_microphone_names())
    mic = sr.Microphone(device_index=0) # index = 0 is for Built-in Microphone 
    
    result = ''
    with mic as source:
        audio = r.listen(source)
        
        """
            recognize_google is speech recognition model created by Google
        """
        result = r.recognize_google(audio)
        
    #print(result)
    return result

if __name__ == '__main__':
    # Setting up computer in-built audio voice for the prompt
    #########################################################
    engine = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" 
    engine.setProperty('voice', voice_id) 
    engine.say("Please speak out the food item") 
    engine.runAndWait()
    ########################################################    
    
    string = userCommand()    
    #string = "I ate Soup" # Test String: 1
    #string = "I had apple" # Test String: 2
    #string = "I ate apple and banana" # Test string 3
    #string = "I ate apple and soup" # Test string 3
    print(string)


    print(sent_parse(string)) # pass the converted string text of the user voice to the regex parser. It will extract food items from the string text


    for word in sent_parse(string):
        foodItemDetails = api_calls.getFoodItems(word) # Sending the food name with upper case 
        
        newInputFromUser = ''
        if foodItemDetails is None:     
            engine.runAndWait()
            engine.say("Please be more specific about your food item that is") 
            engine.runAndWait()
            engine.say(word) 
            engine.runAndWait()
            newInputFromUser = userCommand() # JUST TAKING FOOD NAME - NO CASUAL TALK
        
        # After getting new voice command, we need to update foodItemDetails with new one
        if newInputFromUser: # Checking empty
            print('New input:', newInputFromUser)
            foodItemDetails = api_calls.getFoodItems(newInputFromUser)
        
        print('For Food item:',word)
        print(foodItemDetails)
            
    
    
    
    
