from recipe_fetcher import RecipeFetcher
from recipe import Recipe

class InteractionManager(object):
    def __init__(self):
        self.fetcher = RecipeFetcher()

    def recipe_prompt(self):
        pass

    # dev-time helper
    def run_recipes(self, searchTerm="mexican", displayCount=5):
        results = im.fetcher.search_recipes(searchTerm)
        for i in range(0, displayCount):
            rawRecipe = im.fetcher.fetch_recipe(results[i])
            recipe = Recipe(rawRecipe)
            recipe.print()


if __name__ == "__main__":
    im = InteractionManager()
    im.run_recipes("vegetarian")
