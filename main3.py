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


if __name__ == '__main__':
    # Setting up computer in-built audio voice for the prompt
    #########################################################
    engine = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" 
    engine.setProperty('voice', voice_id) 
    engine.say("Please speak out the food item") 
    engine.runAndWait()
    ########################################################
    
    r = sr.Recognizer() # Function to be sent as an argument for the speech into text function
    with sr.Microphone() as source2:
        string = speechToText(r, source2) # Temporary commenting needed for work
        string = "I ate an Apple" # Test String: 1
        print(string)

        # Defining the relative path of the food data in PC
        ##################################################################
        
        cwd = os.getcwd() # gets the current working directory
        data = os.path.realpath(r"food.csv") # gives absolute path regardless the OS
        
        ##################################################################
        
        df = pd.read_csv(data) # Read the data file as a data frame
        #df = df.drop_duplicates(subset = ["description"])
        print(sent_parse(string)) # pass the converted string text of the user voice to the regex parser. It will extract food items from the string text

        # Computing the cosine similarity for the list of user defined food items
        ##########################################################################
        #vectorizer = TfidfVectorizer()
        #df["description"] = df["description"].str.upper() # Convert all the contents of the data frame with "description" into upper case
        #temp = vectorizer.fit_transform(df["description"])
        for word in sent_parse(string):
            api_calls.getFoodItems(word)
            """
            query_tfidf = vectorizer.transform([word])
            cosineSimilarities = cosine_similarity(query_tfidf, 
                                                   temp).flatten()
            df["cosineSimilarities"] = cosineSimilarities # adding a new column for the data frame
            if df["cosineSimilarities"][df["cosineSimilarities"].values.argmax()] <= 0.7: # if the maximum cosine similarity between the food item of the user and the food item in the data base is less than 70%
                engine.say("The food item") 
                engine.runAndWait()
                engine.say(word) 
                engine.runAndWait()
                engine.say("is not present in the database") 
                engine.runAndWait()
                engine.say("Do you mean") 
                engine.runAndWait()
                engine.say(df["description"][df["cosineSimilarities"].values.argmax()]) 
                engine.runAndWait()
                engine.say("say yes or no") 
                engine.runAndWait()

                # Program will wait until user says yes or no
                ################################################################################
                format1 = pa.paInt16
                rate = 16000
                channel = 1
                chunk = 1024
                threshold = 600
            
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
                        audio2 = r.listen(source2, timeout=1,phrase_time_limit=10)
                        string = r.recognize_google(audio2)
                        string = string.lower()
                        #print(rms, threshold, " Detected")
                        break
                #################################################################################
                    
                string = speechToText(r, source2)
                if string == "yes": # if yes then display nutritions of that food item
                    ids = str(df["fdc_id"][df["cosineSimilarities"].values.argmax()])
                    #ids = str(df["fdc_id"][temp])
                    url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + ids + '/nutrients'
                    webbrowser.open(url)
                elif string == "no": # if no then switch to the next food item in the list
                    continue
                
            else:
                #print(df.sort_values('cosineSimilarities', ascending = False))
                ids = str(df["fdc_id"][df["cosineSimilarities"].values.argmax()])
                #ids = str(df["fdc_id"][temp])
                url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + ids + '/nutrients'
                webbrowser.open(url)
                print(df["cosineSimilarities"][df["cosineSimilarities"].values.argmax()])
            #print(df["cosineSimilarities"][df["cosineSimilarities"].values.argmax()])
            """
    
    
    
    
    
