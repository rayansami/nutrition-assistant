import speech_recognition as sr
import pyttsx3
import pandas as pd
import os
import audioop
import pyaudio as pa

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
        

def FDC_ID(r, source2):
    # Program will wait until spoken
    format1 = pa.paInt16
    rate = 16000
    channel = 1
    chunk = 1024
    threshold = 400

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
    url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + string + '/nutrients'
    #print(string1)
    return url

    
    
