import os 
import json
import pickle
from operator import itemgetter

from allrecipe_db import AllRecipe, load_allrecipe_database, basic_ingredients_in_recipe
from basic_ingredients import load_basic_ingredients
from guru import Guru
from recipe import Recipe
from config import get_config
from ingredient import Ingredient

config = get_config()

# a set of ingredients which are common spices
common_spices = ['salt', 'pepper', 'garlic']

# creates pairs of distinct basic ingredients
def compute_pairs_of_ingredients():
    basic_ingredients = load_basic_ingredients()
    result = set()
    for b in basic_ingredients:
        for c in basic_ingredients:
            if b != c:
                result.add((b,c))
    return result

# returns a dictionary, indexed by basic_ingredients, which keeps track in what proportion of recipes 
# a given ingredient appears 
def compute_appearance_rate():
    ardb = load_allrecipe_database()
    basic_ingredients = load_basic_ingredients()

    result = dict()
    for b in basic_ingredients:
        result[b] = 0
    
    number_of_recipes = len(ardb)
    
    for ar in ardb:
        appearing = basic_ingredients_in_recipe(ar.parsed_recipe, basic_ingredients)
        for a in appearing:
            result[a] = result[a] + 1
            
    for b in basic_ingredients:
        result[b] = result[b] / number_of_recipes
    return result

# returns a dictionary, indexed by pairs of distinct basic ingredients (a, b), which keeps "similarity coefficients", ie. the
# percentage of dishes containing a which also contain b, stored as a float in [0, 1] 
def compute_similarity_coefficients():
    appearance_rate = compute_appearance_rate()
    pairs_of_ingredients = compute_pairs_of_ingredients()
    basic_ingredients = load_basic_ingredients()
    ardb = load_allrecipe_database()
    
     # initializing the dictionary
    similarity_coefficients = dict()  
    for p in pairs_of_ingredients: 
        similarity_coefficients[p] = 0
   
    # we count in how many recipes a given iongredient appears
    appearances = dict()
    for b in basic_ingredients:
        appearances[b] = 0
    
    # add one point for each recipe in which they appear together
    for ar in ardb:
        appearing = basic_ingredients_in_recipe(ar.parsed_recipe, basic_ingredients)
        for a in appearing:
            appearances[a] = appearances[a] + 1
            for b in appearing:
                if a != b:
                    similarity_coefficients[(a,b)] = similarity_coefficients[(a,b)] + 1
    
    # then normalize the results by dividing by the amount of recipes in which ingredient appears
    for p in pairs_of_ingredients:
        # if the coefficients is equal to one, then it is considered noise and ignored
        if similarity_coefficients[p] > 1:
            similarity_coefficients[p] = similarity_coefficients[p] / appearances[p[0]]
        else:
            similarity_coefficients[p] = 0
                    
    return similarity_coefficients

# returns a dictionary, indexed by pairs of distinct basic ingredients (a, b), which keeps "equivalence index", ie. the number of 
# ingredients which often go both with a and b, weighted in reverse proportion to how a, b go together
# (that is, a pair (a, b) has a high "equivalence index" if there are many ingredients which often go with a and b, themselves
# but a, b don't often go together
def compute_equivalence_index(cutoff = 0.5):
    basic_ingredients = load_basic_ingredients()
    pairs_of_ingredients = compute_pairs_of_ingredients()    
    sc = compute_similarity_coefficients()
    
    # initialize the result dictionary
    equiv_index = dict()
    for p in pairs_of_ingredients:
        equiv_index[p] = 0
    
    # we count the amount of other ingredients that often go together with both p[0] and p[1],
    # common spices are excluded
    for p in pairs_of_ingredients:
        for b in basic_ingredients:
            if b not in common_spices:
                if b != p[0] and b != p[1]:
                    if sc[(p[0], b)] >= cutoff and sc[(p[1], b)] >= cutoff:
                        equiv_index[p] = equiv_index[p] + 1
            
    # we check how often p[0] and p[1] go together
    for p in pairs_of_ingredients:
#        if equiv_index[p] > 0: 
#            print(str(p) + " go often together and they have sc " + str(sc[p]))
        equiv_index[p] = equiv_index[p] * (1 - sc[p])
    return equiv_index

# returns a dictionary of replacements, indexed by basic_ingredient
# the value compute_best_replacements()[b] at an ingredient b is a list of ingredients sorted 
# from ones that are the best replacements of b to the worst 
# (here, we measure what is a good replacement using the "equivalence index" of compute_equivalence_index()
def compute_best_replacements():
    ei = compute_equivalence_index()
    basic_ingredients = load_basic_ingredients()
    pairs_of_ingredients = compute_pairs_of_ingredients()
    appearance_rate = compute_appearance_rate()
    
    result = dict()

    for b in basic_ingredients:
        result[b] = []

    for p in pairs_of_ingredients:
        # we penalize ingredients that appear in less than 0.5% of all recipes
        cut_appearance_rate = max(appearance_rate[p[1]], 0.005)
        result[p[0]].append((p[1], ei[p]*cut_appearance_rate))
    
    for b in basic_ingredients:
        result[b].sort(key=itemgetter(1))
        result[b].reverse()
        simplified_result = [p[0] for p in result[b]]
        result[b] = simplified_result
    return result

def compute_typed_best_replacements(): 
    g = Guru() 
    br = compute_best_replacements()
    basic_ingredients = load_basic_ingredients()
    
    result = dict()
    ing_type = dict()
    for i in basic_ingredients:
        result[i] = []
        ing_type[i] = g.getIngredientBaseType(i)
        
    for i in basic_ingredients:
        if ing_type[i] != None:
            def matching_type(s : str):
                if ing_type[i] == 'meat' or ing_type[i] == 'vegprotein':
                    return s == 'meat' or s == 'vegprotein'
                else:
                    return s == ing_type[i]
            result[i] = [j for j in br[i] if matching_type(ing_type[j])]
        else:
            result[i] = br[i]
    return result
    
def load_best_replacements_table():
    with open(os.path.join(config['ALLRECIPE_DATA'], config['REPLACEMENT_TABLE']),'r') as br_file:
        return json.load(br_file)
    
def load_typed_best_replacements_table():
    with open(os.path.join(config['ALLRECIPE_DATA'], config['TYPED_REPLACEMENT_TABLE']),'r') as tbr_file:
        return json.load(tbr_file)

def create_datafiles():
    sc = compute_similarity_coefficients()
    with open(os.path.join(config['ALLRECIPE_DATA'], config['SIMILARITY_COEFFICIENT']),'wb') as sc_file:
        pickle.dump(sc, sc_file)
        
    ei = compute_equivalence_index()
    with open(os.path.join(config['ALLRECIPE_DATA'], config['EQUIVALENCE_INDEX']),'wb') as ei_file:
        pickle.dump(ei, ei_file)

    br = compute_best_replacements()
    with open(os.path.join(config['ALLRECIPE_DATA'], config['REPLACEMENT_TABLE']),'w') as br_file:
        json.dump(br, br_file)
        
    tbr = compute_typed_best_replacements()
    with open(os.path.join(config['ALLRECIPE_DATA'], config['TYPED_REPLACEMENT_TABLE']),'w') as tbr_file:
        json.dump(tbr, tbr_file)
        
if __name__ == "__main__":
    create_datafiles()