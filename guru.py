import os

import pandas as pd

from config import get_config

class Guru(object):
    '''Gets instantiated once per recipe and gets passed to Ingredient classes as a helper class.
    Do any heavy loading here (regex, pandas, etc) so it gets done once and passed around.'''
    def __init__(self):
        self.config = get_config()
        self.setup_ingredients()

    def setup_ingredients(self):
        ingredients_path = os.path.join(self.config["RAW_DATA"], self.config["INGREDIENT_FILE"])
        self.ingredientsDF = pd.read_csv(ingredients_path, sep="\t", index_col="# id", \
                                usecols=["# id", "ingredient name", "category"]) \
                                .rename_axis("ingredient id")

    def get_ingredient_base_type(self, ingredient):
        # takes the cleaned ingredient name and finds its base type
        # TODO: find another backbone source for this
        # this one comes back with some stuff that...might not be useful
        needle = ingredient.replace(" ", "_")
        suspicious_hay = self.ingredientsDF[self.ingredientsDF["ingredient name"] == needle]
        if len(suspicious_hay) > 0:
            return suspicious_hay["category"].values[0]
        else:
            return None
