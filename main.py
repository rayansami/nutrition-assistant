import speech_recognition as sr
import audioop
import pyaudio as pa
import pyttsx3

import webbrowser


# Self defined modules
from modules import speechToText

engine = pyttsx3.init()
voice_id = "HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens\TTS_MS_EN-US_ZIRA_11.0"
# Use female voice 
engine.setProperty('voice', voice_id) 
engine.say("Please speak out the food item") 
engine.runAndWait()

r = sr.Recognizer()
with sr.Microphone() as source2:
    string = speechToText(r, source2)
    print(string)

    engine.say("Please speak out the FDC ID of ") 
    engine.say(string)
    engine.say(" you would like to know")
    engine.runAndWait()
    #print("Please speak out the FDC ID of ", string, " you would like to know")
    url = 'https://fdc.nal.usda.gov/fdc-app.html#/?query=' + string
    webbrowser.open(url) 

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
            string1 = r.recognize_google(audio2)
            string1 = string1.lower()
            #print(rms, threshold, " Detected")
            break


    url = 'https://fdc.nal.usda.gov/fdc-app.html#/food-details/' + string1 + '/nutrients'
    print(string1)
    webbrowser.open(url) 

# Export datafile into the data frame
#path = r"C:\Users\dfsdfsdsdf\Desktop\NLP\nutrition-assistant"
#path1 = r"data\FoodData_Central_foundation_food_csv_2020-04-29"
#data = os.path.join(path, path1, "food.csv")

#df = pd.read_csv(data)
#print(df.head())