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

# a generic class containing a given recipe from allrecipes.com
# saves the url, an instance of Recipe(), as well as a list of reviews
class AllRecipe:
    def __init__(self, url : str, max_reviews = 1000):
        rf = RecipeFetcher()
        
        self.url = url
        self.parsed_recipe = Recipe(rf.fetch_recipe(url))
        self.reviews = rf.fetch_reviews(url, max_amount = max_reviews)
        
    def __eq__(self, other):
        return self.url == other.url

# loads the list of recipes from allrecipes.com from a pickle file 
def load_allrecipe_database():
    return pickle.load(open('allrecipe_db.pickle', 'rb'))

# save the list of recipes from allrecipes.com into a pickle file 
def save_allrecipe_database(ardb):
    with open('allrecipe_db.pickle', 'wb') as handle:
        pickle.dump(ardb, handle, protocol=pickle.HIGHEST_PROTOCOL)

# removes duplicates from the database of recipes (not necessarily efficiently)
def remove_duplicates_in_allrecipe_database():
    removal_element = None
    ardb = load_allrecipe_database()
    for i in range(0, len(ardb)):
        for j in range(i+1, len(ardb)):
                if ardb[i].url == ardb[j].url:
                    removal_element = j
    # if a duplication is found, then we remove the element and invoke the function again
    if removal_element != None:
        print("Removing element at " + str(removal_element))
        del ardb[removal_element]
        save_allrecipe_database(ardb)
        remove_duplicates_in_allrecipe_database()
        
# fetches a max_recipes amount of recipes (maximum 10) from allrecipes.com containing a given keyword,
# each with at most a given maximum or reviews 
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
        
# returns a list of ingredients (passed as a list of strings) appearing in a given recipe
def basic_ingredients_in_recipe(r : Recipe, ings : list):
    result = set()
    for b in ings:
        for i in r.allIngredients:
            if b in i.name.lower():
                result.add(b)
    # print("Found " + str(len(result)) + " ings in this recipe")
    return result

# generates a list of basic culinary ingredients obtained from the allrecipes.com data
def load_basic_ingredients():
    # load the database of recipes
    ardb = load_allrecipe_database()
    
    # first create a set of all ingredients which appear in some recipe in the database
    basic_ingredients = []
    for ar in ardb:
        basic_ingredients = basic_ingredients + [i.name.lower() for i in ar.parsed_recipe.allIngredients]
    basic_ingredients = set(basic_ingredients)
    
    # we remove the longer versions of ingredients already appearing in the database
    def find_longer_duplicate(s : set):
        for i in s:
            for j in s:
                if i in j and (not j in i) and (len(i) > 1):
                    return j
        return None

    def remove_longer_duplicates(s : set):
        duplicate = find_longer_duplicate(s)
        if duplicate:
            s.remove(duplicate)
            remove_longer_duplicates(s)
    
    remove_longer_duplicates(basic_ingredients)
    
    # remove ingredients which contain ":" or " inch" because they're parsing artifacts
    basic_ingredients = set([i for i in basic_ingredients if not ':' in i])
    basic_ingredients = set([i for i in basic_ingredients if not 'inch' in i])
    
    # if an ingredient is too long, keep only the first two and last two words
    additions = set()
    for b in basic_ingredients:
        split = b.split()
        if len(split) > 2:
            additions.add(split[0] + " " + split[1])
            additions.add(split[-2] + " " + split[-1])
    basic_ingredients = set([b for b in basic_ingredients if len(b.split()) <= 2])
    for a in additions:
        basic_ingredients.add(a)

    # remove ingredients which don't appear at least twice among the recipes 
    appearance_rate = dict()
    for b in basic_ingredients:
        appearance_rate[b] = 0
    for ar in ardb:
        for i in basic_ingredients_in_recipe(ar.parsed_recipe, basic_ingredients):
            appearance_rate[i] = appearance_rate[i] + 1
    
    basic_ingredients = set([b for b in basic_ingredients if appearance_rate[b] > 1])
       
    return basic_ingredients