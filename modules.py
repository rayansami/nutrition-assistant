import speech_recognition as sr
import pyttsx3

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