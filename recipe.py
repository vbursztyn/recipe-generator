from ingredient import Ingredient
import RecipeStep
from guru import Guru

class Recipe(object):
    def __init__(self, rawRecipe, guru=None):
        self.rawRecipe = rawRecipe
        self.name = rawRecipe["name"]
        self.guru = guru if guru else Guru()
        self.parse_ingredients()
        self.assign_ingredient_roles()
        self.steps = RecipeStep.RecipeDirectionsParser(rawRecipe['directions'], self.allIngredients).get_steps()
        self.parse_nutrition_information()

    def parse_ingredients(self):
        self.allIngredients = []
        self.subcomponents = []
        self.ingredientsBySubcomponent = {}
        activeSubcomponent = None
        rawIngs = self.rawRecipe["ingredients"]
        for ing in rawIngs:
            ping = Ingredient(ing, self.guru)
            # is this a subcomponent delimiter?
            if ing.strip()[-1:] == ":" and not any([ping.quantity, ping.quantityModifier, ping.unit, ping.prepSteps]):
                # it's probably a subcomponent like "Seasoning Mix:"
                cleanSubc = ing.strip()[:-1]
                self.subcomponents.append(cleanSubc)
                activeSubcomponent = cleanSubc
                self.ingredientsBySubcomponent[cleanSubc] = []
            elif activeSubcomponent:
                self.ingredientsBySubcomponent[activeSubcomponent].append(ping)
            # always make the master list, too
            self.allIngredients.append(ping)

    def assign_ingredient_roles(self):
        # go through and assign ingredient.role on each ingredient
        # includes: protein, vegetables, spices, garnish...?
        pass

    def parse_steps(self):
        pass

    def parse_nutrition_information(self):
        pass

    # DEV HELPERS
    def __str__(self):
        # this is certainly hacky, but it seemed easier/faster to just nest prints
        # (given the subcomponents) than build a payload to return
        print("============")
        print(self.rawRecipe["name"].upper())
        print("\n[INGREDIENTS]")
        self.printIngredients()
        print('\n[STEPS]')
        RecipeStep.print_steps(self.steps)
        # self.print_nutrition_info()
        print("============")
        return("\n")

    def printIngredients(self):
        # are there subcomponents to worry about?
        if not self.subcomponents:
            for ing in self.allIngredients:
                print(ing)
        else:
            # print by subcomponent
            for subc in self.subcomponents:
                print(subc.upper() + ":")
                for ing in self.ingredientsBySubcomponent[subc]:
                    print(ing)
                print("----------")

    def verbosePrint(self):
        print("============")
        print(self.rawRecipe["name"].upper())
        print("\n[INGREDIENTS]")
        self.verbosePrintIngredients()
        print('\n[STEPS]')
        RecipeStep.print_steps(self.steps)
        print("\n[THE PARSED STEP REPRESENTATION]")
        for step in self.steps:
            print(step.internal_info_as_str())
        # self.print_nutrition_info()
        print("============")
        return("\n")

    def verbosePrintIngredients(self):
        # are there subcomponents to worry about?
        if not self.subcomponents:
            for ing in self.allIngredients:
                print(ing.verboseRep())
        else:
            # print by subcomponent
            for subc in self.subcomponents:
                print(subc.upper() + ":")
                for ing in self.ingredientsBySubcomponent[subc]:
                    print(ing.verboseRep())
                print("----------")
