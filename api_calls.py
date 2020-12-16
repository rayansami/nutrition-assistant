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


api_key = "Za6qWk9XQkvBWOL5m0mqwf04W9tk6eoUfZt5HpZV"
url = 'https://api.nal.usda.gov/fdc/v1/foods/search'
global foodNutrient

def getFoodItems(fooditem):
    parammeter = {'api_key': api_key, 'query': fooditem}
    
    response = requests.get(url, params = parammeter)
    
    # Loading the response data into a dict variable
    # json.loads takes in only binary or string variables so using content to fetch binary content
    # Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    jsonData = response.json()
    
    #print(jsonData)    
    
    if jsonData['foods'][0]['description'] == fooditem.upper(): # Case 1: if the search item matches exactly with the first item of the Json list
        foodNutrient = jsonData['foods'][0]['foodNutrients']
        print(foodNutrient)
    #else: # Case 2: If the first item doesn't match exactly, check cosine similarity in the list and Take the highest one (with over 80%)
    #    for index in range(0,len(jsonData['foods'])): # Starting from 0 index of the foods array
    #        nameOnList = jsonData['foods'][index]['foodNutrients']
    #vectorizer = TfidfVectorizer()
    #fooditem = fooditem.upper() # Convert all the contents of the data frame with "description" into upper case
    #temp = vectorizer.fit_transform(df["description"])
    """
    print("The response contains {0} properties".format(len(jsonData)))
    print("\n")
    
    for key in jsonData:
        print(key + " : " + jsonData[key])
    """