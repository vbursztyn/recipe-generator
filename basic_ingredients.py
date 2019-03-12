# This short file contains the method to load the list of basic ingredients obtained from the database of
# allrecipes.com recipes. 

import os

import json

from config import get_config

config = get_config()

# loads a list of basic ingredients (saved as a pickle file)
def load_basic_ingredients():
    with open(os.path.join(config['ALLRECIPE_DATA'], config['BASIC_INGREDIENTS']),'r') as bi_file:
        return json.load(bi_file)
    
basic_ingredients = load_basic_ingredients()
    
# returns a basic ingredient corresponding to a given string (or else returns None)
def close_basic_ingredient(s : str):
    for i in basic_ingredients:
        if i in s:
            return i
    return None