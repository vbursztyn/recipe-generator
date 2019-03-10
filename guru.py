from copy import copy, deepcopy
import os
from random import randint

from fuzzywuzzy import fuzz
import pandas as pd

from basic_ingredients import close_basic_ingredient
from config import get_config
from nutritional_transformation import NutritionalTransformation
from keywords.transforms import TRANSFORMS

# note, some of the raw list ingredient data sources imported below
# contain some elements from
# https://github.com/rkm660/Group10Recipe/blob/master/foods.txt
# and https://raw.githubusercontent.com/tejaswineesohoni/Recipe-Transformer/master/source/vocabulary/ingredientTypes.json

# a helper function used in the search/matching below
def fuzzyFind(row, col, searchTerm):
    name = row[col]
    name = name.lower()
    return fuzz.ratio(name, searchTerm.lower())

class Guru(object):
    '''Gets instantiated once per recipe and gets passed to Ingredient classes as a helper class.
    Do any heavy loading here (regex, pandas, etc) so it gets done once and passed around.'''
    def __init__(self):
        self.config = get_config()
        self.setUpIngredients()

    def setUpIngredients(self):
        self.meats = pd.read_csv("keywords/meats.csv")
        self.meats["category"] = "meat"
        self.vegproteins = pd.read_csv("keywords/vegproteins.csv")
        self.vegproteins["category"] = "vegprotein"
        self.spices = pd.read_csv("keywords/spices.csv")
        self.spices["category"] = "spice"
        self.sauces = pd.read_csv("keywords/sauces.csv")
        self.sauces["category"] = "sauce"
        self.oils = pd.read_csv("keywords/oils.csv")
        self.oils["category"] = "oil"
        self.herbs = pd.read_csv("keywords/herbs.csv")
        self.herbs["category"] = "herb"
        self.vegetables = pd.read_csv("keywords/vegetables.csv")
        self.vegetables["category"] = "vegetable"
        self.fruits = pd.read_csv("keywords/fruits.csv")
        self.fruits["category"] = "fruit"
        self.cheeses = pd.read_csv("keywords/cheeses.csv")
        self.cheeses["category"] = "cheese"
        self.eggDairy = pd.read_csv("keywords/eggdairy.csv")
        self.eggDairy["category"] = "eggdairy"
        self.knownIngredients = self.meats.append([self.vegproteins, self.spices, self.sauces, self.oils, self.herbs, self.vegetables, self.fruits, self.cheeses, self.eggDairy], sort=True)
        self.knownIngredients["name"] = self.knownIngredients["name"].str.lower()

    def getIngredientBaseType(self, ingredient):
        # what is it? a meat, spice/condiment or what?
        needle = ingredient.lower()
        bestMatch = self.getClosestIngredientMatch(needle)
        if bestMatch:
            return bestMatch[1]
        else:
            return None

    def getClosestIngredientMatch(self, ingredient):
        # use the list of basic ingredients from allrecipes.com to try to find a shorter form
        short_form = close_basic_ingredient(ingredient)
        if short_form:
            ingredient = short_form
        ingredient = ingredient.lower()
        matchThreshold = 80 # must be 80% similar at least -- we can tweak this as necessary
        matches = self.knownIngredients[self.knownIngredients.apply(lambda row: fuzzyFind(row, "name", ingredient), axis=1) > matchThreshold]
        if len(matches) > 1:
            # let's pick the closest
            # if multiple tie as best, we'll revert to providing options
            # make pairs
            sets = zip(matches["name"].values, matches["category"].values)
            # order by closeness
            wrappedPairs = [(fuzz.ratio(ingredient, s[0].lower()), s) for s in sets]
            wrappedPairs.sort()
            wrappedPairs.reverse()
            highScore = wrappedPairs[0][0]
            # do we have ties for first place?
            topScorers = [wp[1] for wp in wrappedPairs if wp[0] == highScore]
            if len(topScorers) == 1:
                return topScorers[0]
            else:
                # do something else? be ruthless for now...
                return topScorers[0]
        elif len(matches) == 1:
            # there's just one -- run with it
            matchedName = matches["name"].values[0]
            foundCategory = matches["category"].values[0]
            return (matchedName, foundCategory)
        else:
            # we've got nothing?
            return None


# EVERYTHING BELOW HERE IS 100% UP FOR GRABS AND ANY/ALL CHANGES SHOULD BE SAFE/NOT INTERFERE WITH ANYTHING ABOVE

    #
    # MAIN TWO TRANSFORMER STUBS
    #

    def transformRecipeStyle(self, recipe, transformType):
        newRecipe = deepcopy(recipe)
        if transformType == "meatToVeg":
            # STUBBED WITH THE METHOD I (DREW) WROTE TO USE HARDCODED STUFF FROM keywords/transforms.py
            newIngredients = self.transformIngredients(recipe, transformType)
        elif transformType == "vegToMeat":
            # STUBBED WITH THE METHOD I (DREW) WROTE TO USE HARDCODED STUFF FROM keywords/transforms.py
            newIngredients = self.transformIngredients(recipe, transformType)
        elif transformType == "toHealthy":
            # STUBBED WITH VICTOR'S METHOD
             newIngredients = NutritionalTransformation().find_healthier_ingredients(recipe)
        elif transformType == "toUnhealthy":
            # STUBBED WITH VICTOR'S METHOD
            newIngredients = NutritionalTransformation().find_trashier_ingredients(recipe)
        else:
            return newRecipe
        # okay, we've got new ingredients
        # TODO: update the newRecipe.allIngredients and newRecipe.subcomponents / newRecipe.ingredientsBySubcomponent as necessary
        # TODO: change the instructions based on the ingredient shift
        # NOTE THAT: newIngredients and recipe.allIngredients should be mirrored lists (for tracking what's changed)
        return newRecipe

    def transformToCuisine(self, recipe, toCuisine):
        # TODO: Implement this!
        return recipe


    #
    # NOW, THE INGREDIENT TRANSFORM FUNCTIONS (USING HARDCODED STUFF IN keywords/transforms.py)
    # Currently used for vegToMeat and meatToVeg transforms above
    #

    def transformIngredients(self, recipe, type):
        newIngs = []
        replaceCount = 0
        for ing in recipe.allIngredients:
            newIng = self.ingredientTransformer(type, ing)
            if newIng:
                replaceCount += 1
                if newIng.name in [ning.name for ning in newIngs]:
                    # TODO: go replace this with something else (?)
                    pass
                newIngs.append(newIng)
            else:
                newIngs.append(ing)

        if replaceCount == 0:
            # special cases!
            # if replaceCount == 0 and type is vegToMeat, add meat
            # TODO

            # if replaceCount == 0 and type is toUnhealthy, double unhealthy ingredients: salt, sugar, baseType oil
            # TODO
            pass

        return newIngs

    def ingredientTransformer(self, type, ingredient):
        # type is one of meatToVeg, vegToMeat, toHealthy, toUnhealthy -- as defined in keywords/transforms.py
        # iterates over the ingredient maps below and returns a swapout
        # DOES NOT MANAGE THINGS LIKE: "hey, this item is already elsewhere in the recipe"
        # incredibly flatfooted for now -- we can build this out as we see fit
        # also, feel free to make this a class if we need to manage more state

        # we could also use the fuzzy matching here, too

        if ingredient.name in TRANSFORMS[type].keys():
            # we're basically done here
            optionCount = len(TRANSFORMS[type][ingredient])
            optSelection = randint(0,optionCount-1) if optionCount > 1 else 0
            return TRANSFORMS[type][ingredient][optSelection]

        # else if this is meatToVeg, check if this thing is a meat type -- use the "generic" transform
        if type == "meatToVeg" and ingredient.baseType == "meat":
            candidates = TRANSFORMS["meatToVeg"]["generic"]
            optionCount = len(candidates)
            optSelection = randint(0,optionCount-1) if optionCount > 1 else 0
            return candidates[optSelection]
