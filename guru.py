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
        self.knownCuisines = ["indian", "italian", "mexican"] # TODO: KEEP THIS IN SYNC WITH keywords/transforms.py
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
        
        # if it contains the word cheese, then it's a cheese, same for sauce 
        if "cheese" in ingredient:
            return "cheese"
        if "sauce" in ingredient:
            return "sauce"
        
        # if it's not that easy, we look for the best match
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

    #
    # MAIN TRANSFORMER METHOD
    #

    def transformRecipeStyle(self, recipe, transformType):
        newRecipe = deepcopy(recipe)

        # for tracking changes and printing them at the end, just append new statements to this list:
        changeLog = []

        if newRecipe.subcomponents:
            # do it by subcomponent
            allNewIngs = []
            for subc in newRecipe.subcomponents:
                newIngs, changeLog = self.transformIngredients(newRecipe.ingredientsBySubcomponent[subc], transformType, changeLog)
                newRecipe.ingredientsBySubcomponent[subc] = newIngs
                allNewIngs.append(subc)
                allNewIngs.extend(newIngs)
            newRecipe.allIngredients = allNewIngs
        else:
            # do it all at once
            newRecipe.allIngredients, changeLog = self.transformIngredients(newRecipe.allIngredients, transformType, changeLog)

        # okay, we've got new ingredients
        # TODO: change the instructions based on the ingredient shift
        # NOTE: anything in newRecipe.allIngredients or newRecipe.ingredientsBySubcomponent will have either
        # self.altered = True or self.addedByTransform = True if it was changed/added during transform

        # THOUGHT: DEDUPE!
        # Example: we might have added water to a recipe with water already in it and need to combine those things
        # However, we only want to do this if they appear in the same step (like broth (now water) + water in a soup base)
        # TODO

        changeStatement = "\n=============\n==CHANGELOG==\n"
        if changeLog:
            changesList = "\n - ".join(changeLog)
            changeStatement += "Based on the requirements, I've made the following updates: \n - " + changesList
        else:
            changeStatement += "Given what you asked for, this recipe already seems pretty good to go!"
        changeStatement += "\n=============\n"

        return newRecipe, changeStatement

    #
    # NOW, THE INGREDIENT TRANSFORM FUNCTIONS (USING HARDCODED STUFF IN keywords/transforms.py)
    #

    def transformIngredients(self, allIngredients, type, changeLog=[]):
        newIngList = []
        addedIngs = []
        replacedIngs = [] # for dev bookkeeping
        replaceCount = 0
        for ing in allIngredients:
            # get the hardcoded cases first, if possible
            swappedIng = self.ingredientTransformer(ing, type)
            reason = None
            # special cases for Victor's methods
            # call these second for anything we don't have hard-coded cases for
            if not swappedIng and type == "toHealthy":
                swappedIng, reason = NutritionalTransformation().find_healthier_ingredients(ing)
            elif not swappedIng and type == "toUnhealthy":
                swappedIng, reason = NutritionalTransformation().find_trashier_ingredients(ing)

            if swappedIng:
                replaceCount += 1
                # copy over the particulars
                replacerIng = deepcopy(ing)
                replacerIng.name = swappedIng
                replacerIng.altered = True
                replacerIng.baseType = self.getIngredientBaseType(swappedIng)
                # TODO: update anything else?
                newIngList.append(replacerIng)
                replacedIngs.append(replacerIng)
                changedStatement = "Replaced "+str(ing.name)+" with "+str(replacerIng.name)
                if reason:
                    changedStatement += " ("+str(reason)+")"
                changeLog.append(changedStatement)
            else:
                # no replacement found...add the old ing back to the new list
                newIngList.append(ing)

        if replaceCount == 0:
            # we didn't replace anything in the recipe
            # special cases!
            # if replaceCount == 0 and type is vegToMeat, add meat to addedIngs
            # TODO
            # REMEMBER TO USE: changeLog.append("Added "+str(ing.name))

            # if replaceCount == 0 and type in ["italian", "indian", "mexican"], add some relevant spices to addedIngs
            # TODO
            pass

        if type in ["toHealthy", "toUnhealthy"]:
            # if type is toHealthy, 1/2 unhealthy ingredients/baseTypes
            # if type is toUnhealthy, double unhealthy ingredients/baseTypes
            # see lists in keywords/transforms.py
            modifier = 0.5 if type == "toHealthy" else 2
            modifierKeyword = "Halved" if type == "toHealthy" else "Doubled"
            for i, ing in enumerate(newIngList):
                if ing.name in TRANSFORMS["unhealthyIngredients"] or ing.baseType in TRANSFORMS["unhealthyBaseTypes"]:
                    newIngList[i] = ing * modifier
                    changeLog.append(modifierKeyword+" the "+str(ing.name))
        for ai in addedIngs:
            # flag the things that are being added as such
            ai.addedByTransform = True

        outputIngs = newIngList + addedIngs

        return outputIngs, changeLog

    def ingredientTransformer(self, ingredient, type):
        # NOTE: CURRENTLY RETURNS A STRING NAME OF INGREDIENT TO MATCH SIGNATURE METHOD OF OTHER TRANSFORMERS
        # type is one of meatToVeg, vegToMeat, toHealthy, toUnhealthy -- as defined in keywords/transforms.py
        # iterates over the ingredient maps below and returns a swapout
        # DOES NOT MANAGE THINGS LIKE: "hey, this item is already elsewhere in the recipe"
        # incredibly flatfooted for now -- we can build this out as we see fit
        # also, feel free to make this a class if we need to manage more state

        # we could also use the fuzzy matching here, too
        if type not in TRANSFORMS:
            return None

        if ingredient.name in TRANSFORMS[type].keys():
            # we're basically done here
            optionCount = len(TRANSFORMS[type][ingredient.name])
            optSelection = randint(0,optionCount-1) if optionCount > 1 else 0
            return TRANSFORMS[type][ingredient.name][optSelection]

        # else if this is meatToVeg, check if this thing is a meat type -- use the "generic" transform
        if type == "meatToVeg" and ingredient.baseType == "meat":
            candidates = TRANSFORMS["meatToVeg"]["generic"]
            optionCount = len(candidates)
            optSelection = randint(0,optionCount-1) if optionCount > 1 else 0
            return candidates[optSelection]

        return None
