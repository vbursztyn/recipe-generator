import pandas as pd


from Levenshtein import distance


import os


import pickle


from config import get_config


config = get_config()


similar_ingredients = pickle.load(open(os.path.join(config['INGREDIENT_DATA'],\
													config['SIMILAR_INGREDIENTS']), 'rb'))


def rank_matches(query, candidates, n_matches=1, cutoff=None):   
    if not cutoff:
        cutoff = len(query) - 1
    
    matches = {}
    for candidate in candidates:
        if not isinstance(candidate, str):
            continue
        edit_dist = distance(query, candidate)
        if edit_dist <= cutoff:
            matches[candidate] = edit_dist
    
    if not len(matches):
        return None

    ranked_matches = sorted(matches, key=matches.get)
    
    if len(matches) >= n_matches:
        ranked_matches = ranked_matches[:n_matches]
    
    return ranked_matches


def get_nutrients_for_ingredient(df_nutrs_by_prods, ingredient_name):
    df_grouped_nutrients = df_nutrs_by_prods[ df_nutrs_by_prods['long_name'] == ingredient_name ].groupby(level=0)
    df_nutrients = df_grouped_nutrients.get_group( list(df_grouped_nutrients.groups)[0] )
    col_names = { 'Nutrient_name' : 'name',\
                  'Output_value' : 'value',\
                  'Output_uom' : 'unit' }
    return df_nutrients[['Nutrient_name', 'Output_value', 'Output_uom']]\
           .rename(columns=col_names).to_dict('records')


if __name__ == '__main__':
	products_path = os.path.join(config['RAW_DATA'], config['USDA_PRODUCTS'])
	df_products = pd.read_csv(products_path,\
	                          index_col='NDB_Number', usecols=['NDB_Number', 'long_name'])
	nutrients_path = os.path.join(config['RAW_DATA'], config['USDA_NUTRIENTS'])
	df_nutrients = pd.read_csv(nutrients_path,\
	                           usecols=['NDB_No','Nutrient_name','Output_value','Output_uom'],\
	                           index_col=['NDB_No'])


	df_nutrs_by_prods = df_products.join(df_nutrients)


	matches = []
	all_products = df_products['long_name'].values
	for ingredient in similar_ingredients:
	    query = ingredient.replace('_',' ').upper()
	    match = rank_matches(query, all_products, cutoff=1)
	    if match:
	        match = match[0]
	        print('Found a match for %s: %s' %(ingredient, match))
	    matches.append((ingredient, match))


	nutrs_by_ingrs = { match[0] : get_nutrients_for_ingredient(df_nutrs_by_prods, match[1])\
					   for match in matches if match[1] }


	pickle.dump(nutrs_by_ingrs,\
				open(os.path.join(config['INGREDIENT_DATA'], config['INGREDIENT_NUTRIENTS']),'wb'))

