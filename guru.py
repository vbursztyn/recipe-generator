from copy import copy, deepcopy
import os
from random import randint
import re

from fuzzywuzzy import fuzz
import pandas as pd

from basic_ingredients import close_basic_ingredient
from config import get_config
from keywords.transforms import TRANSFORMS
from ingredient import Ingredient
from nutritional_transformation import NutritionalTransformation
import RecipeStep
import gnureadline

# NOTE: A few of the raw list ingredient data sources imported below contain elements
# sourced from one of either https://github.com/rkm660/Group10Recipe/blob/master/foods.txt
# or https://raw.githubusercontent.com/tejaswineesohoni/Recipe-Transformer/master/source/vocabulary/ingredientTypes.json
# the others are either scraped, assembled programatically via statistical methods, or hand-assembled


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
        self.knownCuisines = ["italian", "mexican", "japanese"] # IN SYNC WITH keywords/transforms.py
        self.strongSpices = {
            "japanese":["ginger","soy sauce"],
            "mexican": ["chili powder", "cumin", "cilantro"],
            "italian": ["italian seasoning", "oregano", "basil"]
        }
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
        self.staples = pd.read_csv("keywords/staples.csv")
        self.staples["category"] = "staples"
        # This is paste as in miso paste, not as in misspelled pasta
        self.paste = pd.read_csv("keywords/paste.csv")
        self.paste["category"] = "paste"
        self.alcohol = pd.read_csv("keywords/alcohol.csv")
        self.alcohol["category"] = "alcohol"
        self.pasta = pd.read_csv("keywords/pasta.csv")
        self.pasta["category"] = "pasta"
        self.eggDairy = pd.read_csv("keywords/eggdairy.csv")
        self.eggDairy["category"] = "eggdairy"
        self.knownIngredients = self.meats.append([self.vegproteins, self.spices, self.sauces, self.oils, self.herbs, self.vegetables, self.fruits, self.cheeses, self.staples, self.paste, self.alcohol, self.pasta, self.eggDairy], sort=True)
        self.knownIngredients["name"] = self.knownIngredients["name"].str.lower()

    def getIngredientBaseType(self, ingredient):
        # what is it? a meat, spice/condiment or what?

        # if it contains the word cheese, then it's a cheese, same for sauce
        if "cheese" in ingredient:
            return "cheese"
        if "sauce" in ingredient:
            return "sauce"
        if "bread" in ingredient:
            return "staples"
        if "bell pepper" in ingredient:
            return "vegetable"

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

        # for tracking changes and printing them at the end
        # just append new statements to this list:
        changeLog = []

        if newRecipe.subcomponents:
            # do it by subcomponent
            allNewIngs = []
            for subc in newRecipe.subcomponents:
                newIngs, changeLog = self.transformIngredients(newRecipe.ingredientsBySubcomponent[subc], transformType, changeLog, newRecipe)
                newRecipe.ingredientsBySubcomponent[subc] = newIngs
                allNewIngs.append(subc)
                allNewIngs.extend(newIngs)
            newRecipe.allIngredients = allNewIngs
        else:
            # do it all at once
            newRecipe.allIngredients, changeLog = self.transformIngredients(newRecipe.allIngredients, transformType, changeLog, newRecipe)

        # okay, we've got new ingredients
        # update the steps
        ingr_subs = {ingr.statement: ingr for ingr in newRecipe.allIngredients if ingr.altered}
        RecipeStep.modify_steps(newRecipe.steps, ingr_subs)
        if transformType == 'meatToVeg':
            for step in newRecipe.steps:
                step._processed_text = re.sub(r'\bmeat\b', '"meat"', step._processed_text)
        elif transformType == 'vegToMeat':
            for step in newRecipe.steps:
                step._processed_text = re.sub(r'"meat"', 'meat', step._processed_text)

        changeStatement = self.assembleChangeStatement(changeLog)

        return newRecipe, changeStatement

    def assembleChangeStatement(self, changeLog):
        changeStatement = "\n=============\n==CHANGELOG==\n"
        if changeLog:
            changesList = "\n - ".join(changeLog)
            changeStatement += "Based on the requirements, I've made the following updates: \n - " + changesList
        else:
            changeStatement += "Given what you asked for, this recipe already seems pretty good to go!"
        changeStatement += "\n=============\n"
        return changeStatement

    #
    # NOW, THE INGREDIENT TRANSFORM FUNCTIONS (USING HARDCODED STUFF IN keywords/transforms.py)
    #

    def transformIngredients(self, allIngredients, type, changeLog, newRecipe):
        newIngList = []
        replacedIngs = [] # for dev bookkeeping
        replaceCount = 0
        # temp hack for some testing
        # ni = deepcopy(allIngredients[5])
        # allIngredients.append(ni)
        # end hack
        for i,ing in enumerate(allIngredients):
            # get the hardcoded cases first, if possible
            rollingIngs = [ring for ring in newIngList+allIngredients[i:] if ing.name != ring.name]
            swappedIng = self.ingredientTransformer(ing, type, rollingIngs)
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

        # if we're making this non-vegetarian, is/was there meat in it?
        if type == "vegToMeat" and not [ing for ing in newIngList if ing.baseType == "meat"]:
            # if not, add some meat...
            addedIng = Ingredient("1/4 pound of bacon, cut into 1/4 inch squares", self)
            addedOil = Ingredient("1 tablespoon of olive oil", self)
            directionsParser = RecipeStep.RecipeDirectionsParser("", [addedIng, addedOil])
            newStep1 = directionsParser.direction_to_recipe_step("Fry the bacon with olive oil on medium high heat until crisp.")
            newStep2 = directionsParser.direction_to_recipe_step("Allow bacon to cool, and then sprinkle it on top.")

            addedIng.addedByTransform = True
            addedOil.addedByTransform = True

            newIngList.append(addedIng)
            newIngList.append(addedOil)
            newRecipe.steps.append(newStep1)
            newRecipe.steps.append(newStep2)
            changeLog.append("Added some homemade bacon crumbles")

        if replaceCount == 0 and type in self.knownCuisines:
            spices = self.strongSpices[type]
            presentSpices = [ing.name for ing in newIngList if ing.baseType in ["spice","herb"]]
            matched = False
            for name in presentSpices:
                for spice in spices:
                    if name in spice or spice in name:
                        matched = True
            if not matched and presentSpices:
                addedSpices = []
                for spice in spices:
                    addedSpices.append(Ingredient("1 teaspoon of "+spice, self))

                # addedSpices is now a list of spices to add
                # presentSpices[0] is the name (string) of a spice in the existing steps
                # TODO: RecipeStep.add_ingredents_alongside(steps, reference_ingr, addedSpices)

        if type in ["toHealthy", "toUnhealthy"]:
            # if type is toHealthy, 1/2 unhealthy ingredients/baseTypes
            # if type is toUnhealthy, double unhealthy ingredients/baseTypes
            # see lists in keywords/transforms.py
            modifier = 0.5 if type == "toHealthy" else 2
            modifierKeyword = "Halved" if type == "toHealthy" else "Doubled"
            for i, ing in enumerate(newIngList):
                if ing.name in TRANSFORMS["unhealthyIngredients"] or ing.baseType in TRANSFORMS["unhealthyBaseTypes"]:
                    newIngList[i] = ing * modifier
                    newIngList[i].altered = True
                    changeLog.append(modifierKeyword+" the "+str(ing.name))

        return newIngList, changeLog

    def ingredientTransformer(self, ingredient, type, currentIngs):
        # NOTE: CURRENTLY RETURNS A STRING NAME OF INGREDIENT TO MATCH SIGNATURE METHOD OF OTHER TRANSFORMERS
        # type is one of meatToVeg, vegToMeat, toHealthy, toUnhealthy -- as defined in keywords/transforms.py
        # iterates over the ingredient maps below and returns a swapout
        # DOES NOT MANAGE THINGS LIKE: "hey, this item is already elsewhere in the recipe"
        # incredibly flatfooted for now -- we can build this out as we see fit
        # also, feel free to make this a class if we need to manage more state

        # make sure we've got what we need
        if type not in TRANSFORMS:
            return None

        # get some blockers to avoid dupes
        blockers = [ing.name for ing in currentIngs]

        # if ingredient.name in TRANSFORMS[type].keys()
        # first check if there's a fitting key in the database
        fitting_keys = [k for k in TRANSFORMS[type].keys() if k in ingredient.name]
        if fitting_keys != []:
            keys_length = [len(k.split()) for k in fitting_keys]
            key = fitting_keys[keys_length.index(max(keys_length))]
            # optionCount = len(TRANSFORMS[type][key])
            # optSelection = randint(0,optionCount-1) if optionCount > 1 else 0
            # NO LONGER RANDOM -- NOW ITERATES THROUGH LIST UNTIL IT HITS A NON-BLOCKED OPTION
            # MAKES SURE TO PREVENT LIKE-KIND SWAPS
            for option in TRANSFORMS[type][key]:
                matches = [match for match in blockers if match in option or option in match]
                if not matches and ingredient.name not in [option, option[0:-1], option+"s"]:
                    return option

        # else if this is meatToVeg, check if this thing is a meat type -- use the "generic" transform
        if type == "meatToVeg" and ingredient.baseType == "meat":
            candidates = TRANSFORMS["meatToVeg"]["generic"]
            optionCount = len(candidates)
            optSelection = randint(0,optionCount-1) if optionCount > 1 else 0
            return candidates[optSelection]

        return None
