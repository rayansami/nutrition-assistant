#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:33:56 2020

@author: rayansami
"""
import requests
from requests.auth import HTTPDigestAuth
import json
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity
import CosineCalculation

api_key = "Za6qWk9XQkvBWOL5m0mqwf04W9tk6eoUfZt5HpZV"
url = 'https://api.nal.usda.gov/fdc/v1/foods/search'

def getFoodItems(fooditem):
    foodNutrient = None
    parammeter = {'api_key': api_key, 'query': fooditem}
    
    response = requests.get(url, params = parammeter)
    
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jsonData = response.json()
    
    #print(jsonData)    
    
    if jsonData['foods'][0]['description'] == fooditem.upper(): # Case 1: if the search item matches exactly with the first item of the Json list
        print('Hit If') 
        foodNutrient = jsonData['foods'][0]['foodNutrients']
        #print(foodNutrient)
    else: # Case 2: If the first item doesn't match exactly, check cosine similarity in the list and Take the highest one (with over 80%)
        print('Hit Else')    
        listi = []        
        for index in range(0,len(jsonData['foods'])): # Starting from 0 index of the foods array
            descriptionOnList = jsonData['foods'][index]['description']
            cosine_value = CosineCalculation.calculate_cosine_between_strings(fooditem,descriptionOnList)
            dictionary = {}    
            dictionary['fdcId'] = jsonData['foods'][index]["fdcId"]
            dictionary['cosineValue'] = cosine_value
            listi.append(dictionary)
        print(sorted(listi, key=lambda fooditem: fooditem['cosineValue']))
        # Ranking based on cosine similarity
        listi = sorted(listi, key=lambda fooditem: fooditem['cosineValue'])
        
        # Check if this list have cosine similarity value more then 80%. If not then return None to main file to ask the user again 
        if(listi[-1]['cosineValue'] >= 0.6):
            for index in range(0,len(jsonData['foods'])):
                if jsonData['foods'][index]['fdcId'] == listi[-1]['fdcId']:
                    foodNutrient =  jsonData['foods'][index]['description']
                    break
        print(foodNutrient)
        
    #vectorizer = TfidfVectorizer()
    #fooditem = fooditem.upper() # Convert all the contents of the data frame with "description" into upper case
    #temp = vectorizer.fit_transform(df["description"])
    """
    print("The response contains {0} properties".format(len(jsonData)))
    print("\n")
    
    for key in jsonData:
        print(key + " : " + jsonData[key])
    """