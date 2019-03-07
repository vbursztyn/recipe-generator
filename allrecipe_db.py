# This file contains an AllRecipe class, which remembers data associated to a given recipe on allrecipes.com:
# that is, the url, the parsed version of the recipe, as well as the reviews.
# Moreover, it contains methods used to manipulate a database of such recipes, which is a list stored in a pickle file.
# In particular, the database can be automatically populated by fetching recipes of a given keyword. 

# (The database is not necessarily of interest to itself, but rather, it contains interesting data we might want to work with. 
# For example, it contains answers to questions like: 
# - which ingredients appear in italian cuisine? 
# - which ingredients often appear together? 
# - what are the substitutions suggested in the comments? 
# The idea of creating one database file is because of IP blocking, allrecipes.com is relatively difficult to access in short 
# amount of time. 

import os
import pickle
from recipe import Recipe 
from recipe_fetcher import RecipeFetcher

class AllRecipe:
    def __init__(self, url : str, max_reviews = 1000):
        rf = RecipeFetcher()
        
        self.url = url
        self.parsed_recipe = Recipe(rf.fetch_recipe(url))
        self.reviews = rf.fetch_reviews(url, max_amount = max_reviews)
        
    def __eq__(self, other):
        return self.url == other.url
        
def load_allrecipe_database():
    return pickle.load(open('allrecipe_db.pickle', 'rb'))

def save_allrecipe_database(ardb):
    with open('allrecipe_db.pickle', 'wb') as handle:
        pickle.dump(ardb, handle, protocol=pickle.HIGHEST_PROTOCOL)

def populate_allrecipe_database(key, max_recipes = 10, max_reviews = 15):
    ardb = load_allrecipe_database()

    print("Looking for recipes of keyword " + str(key))
    recipes = RecipeFetcher().search_recipes(key, max_recipes)
    for url in recipes:
        print("Fetching data for " + url)
        ardb.append(AllRecipe(url, max_reviews))
        
    print("Saving the database of allrecipes to a pickle file!")
    with open('allrecipe_db.pickle', 'wb') as handle:
        pickle.dump(ardb, handle, protocol=pickle.HIGHEST_PROTOCOL)