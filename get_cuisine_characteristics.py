from time import sleep


from random import randint


from itertools import combinations


from collections import Counter


import os


import pickle


from recipe_fetcher import *


from recipe import *


from config import get_config


config = get_config()


def random_sleep(interval): # Use a randomized wait (otherwise your IP may be blocked)
    sleep_time = randint(interval[0], interval[1])
    sleep(sleep_time)


cuisine_keywords = {'italian'   : ['italian'],
                    'french'    : ['french'],
                    'mexican'   : ['mexican'],
                    'indian'    : ['indian'],
                    'japanese'  : ['japanese']}

"""
cuisine_keywords = {'italian'   : ['italian', 'parmegiana', 'napolitana'], # Meant to be expanded like this
                    'french'    : ['french'],
                    'mexican'   : ['mexican'],
                    'indian'    : ['indian'],
                    'japanese'  : ['japanese'],
                    'chinese'   : ['chinese'], # And along this axis too
                    'spanish'   : ['spanish'],
                    'brazilian' : ['brazilian'],
                    'peruvian'  : ['peruvian'],
                    'polish'    : ['polish'],
                    'swedish'   : ['swedish'],
                    'german'    : ['german'],
                    'portuguese': ['portuguese']}
"""


if __name__ == '__main__':
	cuisine_recipes = {}

	for cuisine in cuisine_keywords:
	    cuisine_recipes[cuisine] = []
	    for kw in cuisine_keywords[cuisine]:
	        cuisine_recipes[cuisine] += RecipeFetcher().search_recipes(kw)
	        random_sleep(config['SAFE_REQUEST_INTERVAL'])


	cuisine_ingredients = {}

	for cuisine in cuisine_recipes:
	    print('Fetching recipes for %s cuisine' %cuisine)
	    cuisine_ingredients[cuisine] = {}
	    cuisine_ingredients[cuisine]['top_ingredients'] = []
	    cuisine_ingredients[cuisine]['top_pairings'] = []
	    for recipe in cuisine_recipes[cuisine]:
	        raw_recipe = RecipeFetcher().fetch_recipe(recipe, include_nutrients=False)
	        ingredients = [ingredient.name.lower()\
	                       for ingredient in Recipe(raw_recipe).ingredients]
	        cuisine_ingredients[cuisine]['top_ingredients'] += ingredients
	        cuisine_ingredients[cuisine]['top_pairings'] += [pair for pair in\
	                                                         combinations(ingredients, 2)]
	        random_sleep(config['SAFE_REQUEST_INTERVAL'])


	cuisine_characteristics = {}

	for cuisine in cuisine_ingredients:
	    cuisine_characteristics[cuisine] = {}
	    cuisine_characteristics[cuisine]['top_ingredients'] = [t for t in\
	                                                           Counter(cuisine_ingredients[cuisine]['top_ingredients']).most_common()\
	                                                           if t[1] > 3]
	    cuisine_characteristics[cuisine]['top_pairings'] = [t for t in\
	                                                        Counter(cuisine_ingredients[cuisine]['top_pairings']).most_common()\
	                                                        if t[1] > 3]


	pickle.dump(cuisine_characteristics,\
	            open(os.path.join(config['CUISINE_DATA'], config['CUISINE_CHARACTERISTICS']),'wb'))

