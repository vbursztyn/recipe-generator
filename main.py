import os
import sys

from guru import Guru
from recipe import Recipe
from recipe_fetcher import RecipeFetcher

class InteractionManager(object):
    def __init__(self):
        # a list of pretty print + method branch to follow in this interaction
        self.verbose = False
        self.recipe = None
        self.changeStatement = ""
        self.validChoices = [
            ("Make it vegetarian", self.vegIt),
            ("Make it un-vegetarian", self.unVegIt),
            ("Make it healthier", self.makeHealthier),
            ("Make it less healthy (but why?)", self.makeLessHealthy),
            ("Switch it to a different cuisine", self.cuisineSwitcherOptions),
            ("Nevermind, let's start over with a different recipe.", self.recipePrompt),
            ("Toggle verbosity of recipe printing (between simple and verbose)", self.toggleVerbosity),
        ]
        # and a list of our supported cuisines...edit at will!
        self.fetcher = RecipeFetcher()
        self.guru = Guru()
        self.knownCuisines = self.guru.knownCuisines

    def startInteraction(self):
        print("\nWelcome to RecipeGuru.")
        self.recipePrompt()

    def recipePrompt(self):
        print("Which recipe should we load up? ")
        recipeURL = input("Enter a URL: ")
        if recipeURL:
            try:
                self.rawRecipe = self.fetcher.fetch_recipe(recipeURL)
            except:
                self.recipeInputFail()
                return False
            self.originalRecipe = Recipe(self.rawRecipe, self.guru) # so we can hang on to the original as we mutate it
            self.recipe = self.originalRecipe
            self.clearConsole()
            print("Okay, this is what I got:")
            print(self.recipe)
            self.presentRecipeOptions()
        else:
            self.recipeInputFail()

    def recipeInputFail(self):
        print("\n\nYou have to give me a valid recipe URL to get started. Try again?")
        self.recipePrompt()

    def presentRecipeOptions(self, returned=False):
        if returned:
            print("Once you've taken in the recipe above, just let me know if there's anything else you want to do with "+str(self.recipe.name)+".")
            print("(Note that any changes listed below will be changes to the original recipe, not the latest altered version.)")
        else:
            print("\n\nWhat do you want to do to this "+str(self.recipe.name)+" recipe?")
        for i, option in enumerate(self.validChoices):
            print("["+str(i)+"] " + option[0])
        try:
            choice = input("Pick a number to continue: ")
        except EOFError:
            print('exit')
            sys.exit(0)
        try:
            choiceNum = int(choice)
        except:
            print("You've got to a pick a number to continue.")
            self.presentRecipeOptions()
            return False
        self.runWithChoice(choiceNum)

    def runWithChoice(self, choiceNum):
        numOfChoices = len(self.validChoices)
        if choiceNum < numOfChoices and choiceNum >= 0:
            self.validChoices[choiceNum][1]()
        else:
            # illegitimate choice
            print("\n\nSorry, that's not a valid option. Try again?")
            self.presentRecipeOptions()

    #
    #
    #
    #
    # the follow-on interactions
    # the GURU gets hooked in here
    def clearConsole(self):
        try:
            print(chr(27) + "[2J")
            # os.system('cls' if os.name == 'nt' else 'clear')
        except:
            pass

    def revealResults(self):
        if not self.recipe: return False
        print(self.changeStatement)
        if self.verbose:
            self.recipe.verbosePrint()
        else:
            print(self.recipe)

    def vegIt(self):
        self.recipe, self.changeStatement = self.guru.transformRecipeStyle(self.originalRecipe, "meatToVeg")
        self.clearConsole()
        print("Recipe with less meat, coming right up!")
        self.revealResults()
        print("\n\n")
        self.presentRecipeOptions(returned=True)

    def unVegIt(self):
        self.recipe, self.changeStatement = self.guru.transformRecipeStyle(self.originalRecipe, "vegToMeat")
        self.clearConsole()
        print("You're a real meat-eater, huh?")
        self.revealResults()
        print("\n\n")
        self.presentRecipeOptions(returned=True)

    def makeHealthier(self):
        self.recipe, self.changeStatement = self.guru.transformRecipeStyle(self.originalRecipe, "toHealthy")
        self.clearConsole()
        print("Behold, a healthier take on this recipe!")
        self.revealResults()
        print("\n\n")
        self.presentRecipeOptions(returned=True)

    def makeLessHealthy(self):
        self.recipe, self.changeStatement = self.guru.transformRecipeStyle(self.originalRecipe, "toUnhealthy")
        self.clearConsole()
        print("You want it to be worse for you? Weird, but okay.")
        self.revealResults()
        print("\n\n")
        self.presentRecipeOptions(returned=True)

    def cuisineSwitcherOptions(self):
        print("\nOh, neat. You want to try this in a different style? Which one?")
        for i, cuisine in enumerate(self.knownCuisines):
            print("["+str(i)+"] " + cuisine.capitalize())
        print("["+str(len(self.knownCuisines))+"] Nevermind, go back to the previous option list.")
        choice = input("Pick a number to continue: ")
        try:
            choiceNum = int(choice)
        except:
            print("You've got to a pick a number to continue.")
            self.cuisineSwitcherOptions()
            return False
        if choiceNum >= 0 and choiceNum < len(self.knownCuisines):
            self.switchCuisineTo(self.knownCuisines[choiceNum])
        elif choiceNum == len(self.knownCuisines):
            # retreat!
            self.presentRecipeOptions(returned=True)
        else:
            # out of bounds...
            print("\n\nThat seems like an invalid choice. Try again?")
            self.cuisineSwitcherOptions()

    def switchCuisineTo(self, cuisine):
        self.clearConsole()
        print("Aha, I like " + cuisine.capitalize() + " food, too!")
        self.recipe, self.changeStatement = self.guru.transformRecipeStyle(self.originalRecipe, cuisine)
        self.revealResults()
        print("\n\n")
        self.presentRecipeOptions(returned=True)

    def toggleVerbosity(self):
        self.verbose = False if self.verbose else True
        self.clearConsole()
        if self.verbose:
            print("Okay, I'll give you all the gory details...")
        else:
            print("Okay, I'll keep it simple...")
        if self.recipe:
            print("Let me reprint that last recipe for you:")
            self.revealResults()
        self.presentRecipeOptions()

    # dev-time helper
    def run_recipes(self, searchTerm="mexican", displayCount=5):
        results = self.fetcher.search_recipes(searchTerm)
        for i in range(0, displayCount):
            rawRecipe = self.fetcher.fetch_recipe(results[i], False)
            recipe = Recipe(rawRecipe)
            print(recipe)


if __name__ == "__main__":
    im = InteractionManager()
    # im.run_recipes("italian", 5)
    im.startInteraction()
