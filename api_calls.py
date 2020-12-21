#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 15 15:33:56 2020

@author: rayansami
"""
import requests
import CosineCalculation
import utility # Custom module, only returns FDC API key. Not available inside git repo for preventing abuse

"""
    ### If you want to use this program, get FDC API key and change the value below ###
"""
api_key = utility.get_api_key()
url = 'https://api.nal.usda.gov/fdc/v1/foods/search'

def checkForMaxCosineSimilarItems(fooditem,jsonData):
    print('Checking item:',fooditem)
    print('Checking json:',jsonData['foods'][0]['description'])
    
    listi = []        
    for index in range(0,len(jsonData['foods'])): # Starting from 0 index of the foods array
        descriptionOnList = jsonData['foods'][index]['description']
        cosine_value = CosineCalculation.calculate_cosine_between_strings(fooditem.upper(),descriptionOnList.upper())
        dictionary = {}    
        dictionary['fdcId'] = jsonData['foods'][index]["fdcId"]
        dictionary['cosineValue'] = cosine_value
        listi.append(dictionary)
    
    # Ranking based on cosine similarity
    return sorted(listi, key=lambda fooditem: fooditem['cosineValue'])

def topTenHasSameCosine(listWithFdcidAndCosine):
    # Checking top ten if they all have same cosine similarity
    allAreCosineSimilar = False
    maxCosineSimilarity = listWithFdcidAndCosine[-1]['cosineValue']
    print('Max:', maxCosineSimilarity)
    count = 1
    for item in listWithFdcidAndCosine[-10:-1]: # -1 is the max, and we are comparing with that. So removing it while making the loop
        print(maxCosineSimilarity, item)
        if item['cosineValue'] == maxCosineSimilarity:
            count = count + 1 # Counting uptp 10. If it's 10 then we gotta invoke CASE 1, else Case 2 for this scenerio
            
    if count == 10:
        allAreCosineSimilar = True
        
    print(allAreCosineSimilar)
    return allAreCosineSimilar

def getFoodItems(fooditem):
    print('hit on getFooditems')
    foodNutrient = None
    
    """
        Get the food data using RESTful API from FDC database
    """
    parammeter = {'api_key': api_key, 'query': fooditem}
    response = requests.get(url, params = parammeter)
    
    """
      Loading the response data into a dict variable
      json.loads takes in only binary or string variables so using content to fetch binary content
      Loads (Load String) takes a Json file and converts into python data structure (dict or list, depending on JSON)
    """
    jsonData = response.json()    
    listWithFdcidAndCosine = checkForMaxCosineSimilarItems(fooditem, jsonData)
    

    if topTenHasSameCosine(listWithFdcidAndCosine):
        print('Case 1')
        """
            Case 1 [Revisit&Research]: More then 10 items with 100% cosine similarity
            There can be a case where there are many items with 100% cosine similarity (e.g. Soup). In these cases we'll ask the user again                    
        """
        return foodNutrient

    elif jsonData['foods'][0]['description'] == fooditem.upper(): 
        print('Case 2')
        """
            Case 2: if the search item matches exactly with the first item of the Json list
        """
        foodNutrient = jsonData['foods'][0]['foodNutrients']
        return foodNutrient
    else:         
        print('Case 3') 
        """
            Case 3: Max similar item with more then 80% cosine similarity 
            If the first item doesn't match exactly, check cosine similarity in the list and Take the highest one (with over 80%)        
                
            This can get hit in 2 scenerios:
                1. Case 1 & 2 are False. And Case 3 got hit for the first time
                2. Case 1 was true first time. As the user input was vague. Then system asked for more specific details
                   and user gave specific name. Then Case 3 got hit
        """
        
        # TODO: fix naming - listi to listWithFdcidAndCosine
        listi = listWithFdcidAndCosine
        
        # Check if this list have cosine similarity value more then 80%. Get the highest one
        # If not then ite'll return None to main file to ask the user again 
        if(listi[-1]['cosineValue'] >= 0.8):
            for index in range(0,len(jsonData['foods'])):
                if jsonData['foods'][index]['fdcId'] == listi[-1]['fdcId']:
                    print('Got match')
                    foodNutrient =  jsonData['foods'][index]['foodNutrients']
                    break
            
        return foodNutrient