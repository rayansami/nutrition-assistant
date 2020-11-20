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
        


if __name__ == '__main__':
    engine = pyttsx3.init()
    voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0" 
    engine.setProperty('voice', voice_id) 
    engine.say("Please speak out the food item") 
    engine.runAndWait()    
    r = sr.Recognizer()
    with sr.Microphone() as source2:
        string = speechToText(r, source2)
        print(string)
        
    #string = 'I would like to get information about bacon or cheese'
    path = r"C:\Users\dfsdfsdsdf\Desktop\NLP\nutrition-assistant"
    path1 = r"data\FoodData_Central_foundation_food_csv_2020-04-29"
    data = os.path.join(path, path1, "food.csv")
    df = pd.read_csv(data)
    #df = df.drop_duplicates(subset = ["description"])
    print(sent_parse(string))
    vectorizer = TfidfVectorizer()
    df["description"] = df["description"].str.upper()
    temp = vectorizer.fit_transform(df["description"])
    for word in sent_parse(string):
        query_tfidf = vectorizer.transform([word])
        cosineSimilarities = cosine_similarity(query_tfidf, 
                                               temp).flatten()
        df["cosineSimilarities"] = cosineSimilarities
        if df["cosineSimilarities"][df["cosineSimilarities"].values.argmax()] >= 0.4:
            #print(df.sort_values('cosineSimilarities', ascending = False))
            ids = str(df["fdc_id"][df["cosineSimilarities"].values.argmax()])
            #ids = str(df["fdc_id"][temp])
            url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + ids + '/nutrients'
            webbrowser.open(url)
            print(df["cosineSimilarities"][df["cosineSimilarities"].values.argmax()])
        print(df["cosineSimilarities"][df["cosineSimilarities"].values.argmax()])
    
    
    
    
    
    