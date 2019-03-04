from ingredient import Ingredient
import RecipeStep
from guru import Guru

class Recipe(object):
    def __init__(self, rawRecipe):
        self.rawRecipe = rawRecipe
        self.guru = Guru()
        self.parse_ingredients()
        self.assign_ingredient_roles()
        self.steps = RecipeStep.directions_to_recipe_steps(rawRecipe['directions'], self.ingredients)
        self.parse_nutrition_information()

    def parse_ingredients(self):
        self.ingredients = []
        rawIngs = self.rawRecipe["ingredients"]
        for ing in rawIngs:
            self.ingredients.append(Ingredient(ing, self.guru))

    def assign_ingredient_roles(self):
        # go through and assign ingredient.role on each ingredient
        # includes: protein, vegetables, spices, garnish...?
        pass

    def parse_steps(self):
        pass

    def parse_nutrition_information(self):
        pass

    # DEV HELPERS
    def print(self):
        print("\n\n============")
        print(self.rawRecipe["name"].upper())
        print("\n[INGREDIENTS]")
        self.print_ingredients()
        print('\n[STEPS]')
        RecipeStep.print_steps(self.steps)
        # self.print_nutrition_info()
        print("============\n\n")

    def print_ingredients(self):
        # dev helper
        for ing in self.ingredients:
            ing.express_components()
