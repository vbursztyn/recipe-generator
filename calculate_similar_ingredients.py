import pandas as pd


from itertools import product


import os


import pickle


from config import get_config


config = get_config()


def Jaccard_coefficient(list_A, list_B):
    set_A = set(list_A)
    set_B = set(list_B)
    return len(set_A.intersection(set_B)) / float(len(set_A.union(set_B)))


if __name__ == '__main__':
	ingredients_path = os.path.join(config['RAW_DATA'], config['INGREDIENT_FILE'])
	df_ingredients = pd.read_csv(ingredients_path, sep='\t',\
	                             index_col='# id',\
	                             usecols=['# id', 'ingredient name'])\
	                             .rename_axis('# ingredient id')

	ingredient_flavors_path = os.path.join(config['RAW_DATA'], config['INGREDIENT_FLAVORS'])
	df_ingrs_flavs = pd.read_csv(ingredient_flavors_path, sep='\t',\
	                             usecols=['# ingredient id','compound id'],\
	                             index_col=['# ingredient id','compound id'])


	df_flavs_by_ingrs = df_ingredients.join(df_ingrs_flavs).reset_index()\
	                    .drop('# ingredient id', axis=1).groupby(['ingredient name'])


	flavs_by_ingrs = {}

	for ingredient, flavors in df_flavs_by_ingrs:
	    if len(flavors['compound id'].values) > 1: # Minimum complexity of flavor profile
	        flavs_by_ingrs[ingredient] = list(flavors['compound id'].values)


	ingredient_pairs = []

	for pair in product(flavs_by_ingrs.keys(), repeat=2):
	    ingredient_A = pair[0]
	    ingredient_B = pair[1]
	    
	    if ingredient_A == ingredient_B:
	        continue
	        
	    similarity = Jaccard_coefficient(flavs_by_ingrs[ingredient_A],\
	                                     flavs_by_ingrs[ingredient_B])
	    
	    if similarity > 0.2: # Minimum similarity
	        ingredient_pairs.append((ingredient_A, ingredient_B, similarity))


	df_similar_ingredients = pd.pivot_table(\
	                                        pd.DataFrame(ingredient_pairs,\
	                                        columns=['ingredient_A', 'ingredient_B', 'similarity']),\
	                                        index='ingredient_A', columns='ingredient_B', values='similarity')



	similar_ingredients = {}

	for ingredient in df_similar_ingredients:
	    row_as_dict = df_similar_ingredients.loc[[ingredient]].dropna(axis=1).to_dict()
	    similar_ingredients[ingredient] = [k for k, v in\
	                                       sorted(row_as_dict.items(),\
	                                              key=lambda x: x[1][ingredient], reverse=True)]


	pickle.dump(similar_ingredients,\
				open(os.path.join(config['INGREDIENT_DATA'], config['SIMILAR_INGREDIENTS']),'wb'))

