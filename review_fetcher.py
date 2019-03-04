from bs4 import BeautifulSoup
import Levenshtein
import time
import os
import pickle
import requests
import pickle

from get_cuisine_characteristics import random_sleep
from recipe_fetcher import RecipeFetcher
from config import get_config

config = get_config()

# this returns a list of possible ingredients 
# right now it uses Victor's "similar_ingredients" list, but in time could be something better
def get_list_of_ingredients():
    similar_ingredients = pickle.load(open(os.path.join(config['INGREDIENT_DATA'],config['SIMILAR_INGREDIENTS']), 'rb'))
    return list(similar_ingredients.keys())

ingredients = get_list_of_ingredients()

# finds the closest match (using Levenshtein distance) to a given word among the ingredients and returns it 
# if no ingredient is at least as close as the given cutoff, returns Null instead
def identify_ingredient(word : str, cutoff = 1):
    ingredients_similarity = dict()
    for i in ingredients:
        ingredients_similarity[i] = Levenshtein.distance(word, i)
    best_match = min(ingredients_similarity, key=ingredients_similarity.get)
    
    if ingredients_similarity[best_match] <= cutoff:
        return best_match
    else:
        return None
    return word

# given an allrecipes.com url, scrapes and returns the list of reviews of the given recipe
def fetch_reviews(url : str):
    
    # we first request the page of the recipe 
    page_html = requests.get(url)
    page_graph = BeautifulSoup(page_html.content, features="lxml")
    
    # we then check if there are any reviews
    result = []
    next_review_element = page_graph.find("a", class_="review-detail__link")
    
    # counter = 0 # TEST LINE
    while next_review_element:
        review_html = requests.get(next_review_element['href'])
        review_graph = BeautifulSoup(review_html.content, features="lxml")
        result.append(review_graph.find_all("meta")[4]['content'])
        next_review_element = review_graph.find("link", attrs={'rel': 'next' })
        random_sleep(config['SAFE_REQUEST_INTERVAL'])
    #    counter = counter + 1 # TEST LINE
    #    if counter > 10: # TEST LINE
    #        break # TEST LINE
    return result

# finds substitutions appearing in a given review
# returns a list of tuples (in_ing, out_ing), where in_ing is the ingredient that is added 
# and out_ing is the ingredient that is being replaced
def substitutions_in_a_review(review : str):
    
    # these are the patterns we use to look for substitutions in a review, hard-coded for now
    patterns = [['IN_ING', 'instead', 'of', 'OUT_ING'],
               ['replace', 'OUT_ING', 'with', 'IN_ING'],
                ['replaced', 'OUT_ING', 'with', 'IN_ING'],
                ['substitute', 'IN_ING', 'for', 'OUT_ING'],
               ['substituted', 'IN_ING', 'for', 'OUT_ING']]
    
    # tries to match a given word to either an ingredient or a given word
    # returns an ingredient or True if successful, None or False otherwise
    def match_symbol(word, symbol):
        if symbol == 'IN_ING' or symbol == 'OUT_ING':
            return identify_ingredient(word)
        else:
            return word == symbol
        
    # tries to match a given pattern to a list of words, both the list and pattern 
    # need to be of the same length - returns the pair of in/out ingredients if successful
    # or Null otherwise
    def match_pattern(pattern, list_of_words):
        for j in range(len(pattern)):
            match = match_symbol(list_of_words[j], pattern[j])
            if match: 
                if pattern[j] == 'IN_ING':
                    in_ing = match
                elif pattern[j] == 'OUT_ING':
                    out_ing = match
            else:
                return None
        return (in_ing, out_ing)
    
    split_review = review.split()
    result = []
    for pat in patterns:
        for j in range(len(split_review)-len(pat)+1):
            match = match_pattern(pat, split_review[j:j+len(pat)])
            if match:
                result.append(match)
    
    return result

# returns a list of substitutions made in reviews of a given recipe (passed as an url)
def find_substitutions_in_reviews(url : str):
    reviews = fetch_reviews(url)
    result = []
    for r in reviews:
        result = result + substitutions_in_a_review(r)
    return result

# if run on its own, it will create a substitution dictionary by searching through the reviews 
# of recipes containing one of the hard-coded keywords,
# the dictionary is then saved into a pickle file 
if __name__ == '__main__':
    keywords = ['italian', 'beef', 'ramen', 'burger', 'chicken', 'indian', 'tofu', 
                'soup', 'potato', 'vegetable', 'vegan', 'fish']
                
    sub_dictionary = dict()
    rf = RecipeFetcher()
    
    def populate_dictionary(key : str):
        print("Looking for recipes of keyword " + str(key))
        recipes = rf.search_recipes(key)
        for url in recipes:
            print("Finding reviews for " + str(url))
            subs = find_substitutions_in_reviews(url)
            print("Found " + str(len(subs)) + " substitutions!")
            for sub in subs:
                if sub[0] in sub_dictionary:
                    sub_dictionary[sub[0]].append(sub[1])
                else:
                    sub_dictionary[sub[0]] = [sub[1]]
                    
    for key in keywords:   
        populate_dictionary(key)
        
    print("Saving dictionary of substitutions as a pickle file")
    with open('sub_dictionary.pickle', 'wb') as handle:
        pickle.dump(sub_dictionary, handle, protocol=pickle.HIGHEST_PROTOCOL)