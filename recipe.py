from ingredient import Ingredient
from guru import Guru

class Recipe(object):
    def __init__(self, rawRecipe):
        self.rawRecipe = rawRecipe
        self.guru = Guru()
        self.parse_ingredients()
        self.parse_steps()
        self.parse_nutrition_information()

    def parse_ingredients(self):
        self.ingredients = []
        rawIngs = self.rawRecipe["ingredients"]
        for ing in rawIngs:
            self.ingredients.append(Ingredient(ing, self.guru))

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
        # self.print_steps()
        # self.print_nutrition_info()
        print("============\n\n")

    def print_ingredients(self):
        # dev helper
        for ing in self.ingredients:
            ing.express_components()
