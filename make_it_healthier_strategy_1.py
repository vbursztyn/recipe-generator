import pickle


import itertools


import time


from recipe_fetcher import RecipeFetcher


from recipe import Recipe


from get_ingredient_nutrients import rank_matches


unhealthy_nutrients = ['Fatty acids, total saturated', 'Sugars, total', 'Sodium, Na']


similar_ingredients = pickle.load(open('ingredient_data/similar_ingredients.pickle', 'rb'))


ingredient_nutrients = pickle.load(open('ingredient_data/ingredient_nutrients.pickle', 'rb'))


def get_nutrient_for_ingredient(target_ingredient, nutrient):
    if not target_ingredient in ingredient_nutrients:
        return None
    result = [(ingredient['value'],ingredient['unit'])\
              for ingredient in ingredient_nutrients[target_ingredient]\
              if ingredient['name'] == nutrient]
    if not result:
        return None
    return result[0]


def best_substitutions(original_ingredient, substitutions, criterion):
    baseline = get_nutrient_for_ingredient(original_ingredient, criterion)
    if not baseline:
        return None
    
    candidates = {}
    for substitution in substitutions:
        substitution_quality = get_nutrient_for_ingredient(substitution, criterion)
        # If we find this bad nutrient (criterion) in this substitution's nutrient profile;
        # If units match, then comparisons are straightforward;
        # If our baseline has more of this bad nutrient (criterion) than the substitution:
        if (substitution_quality) and (baseline[1] == substitution_quality[1])\
                                  and (baseline[0] > substitution_quality[0]):
            candidates[substitution] = (substitution_quality[0] / baseline[0]) * 100
    
    top_cutoff = len(candidates)//10 if len(candidates) >= 20 else len(candidates)//2
    top_candidates = { k : v for k, v in itertools.islice(candidates.items(),top_cutoff) }
    
    return [(k, top_candidates[k]) for k in sorted(top_candidates, key=top_candidates.get)]


def minimize_bad_nutrient(recipe, bad_nutrient):
    results = '\nYou can make %s healthier by minimizing %s:\n\n' %(recipe['name'], bad_nutrient)
    
    ingredients = [ingredient.name for ingredient in Recipe(recipe).allIngredients]
    all_ingredients = similar_ingredients.keys()
    matches = []
    for ingredient in ingredients:
        query = ingredient.replace(' ','_')
        match = rank_matches(query, all_ingredients, cutoff=2)
        if match:
            matches.append((ingredient, match[0]))
    
    for match in matches:
        similar_to_match = similar_ingredients[match[1]]
        substitutions = best_substitutions(match[1], similar_to_match, bad_nutrient)
        if not substitutions:
            continue
        captions = ['%s (%.2f%% less %s)'\
                    %(substitution[0], 100.0 - substitution[1], bad_nutrient)\
                    for substitution in substitutions]
        results += '- You can replace %s by %s.\n' %(match[0], ', '.join(captions))
    
    return results


def find_healthier_ingredients(recipe):
    results = {}

    for bad_nutrient in unhealthy_nutrients:
        healthier_version = minimize_bad_nutrient(recipe, bad_nutrient)
        if '- You can replace' in healthier_version:
            results[healthier_version] = len(healthier_version)
    
    if len(results):
        print(sorted(results, key=results.get, reverse=True)[0])
    else:
        print('Couldn\'t make it healthier this way.')


if __name__ == '__main__':
	keywords = ['meat lasagna', 'ham sandwich', 'bean chili',\
				'mac and cheese', 'cheese meatloaf', 'quiche', 'omelette',\
				'Reuben', 'pizza', 'bacon risotto','lentil soup',\
	            'eggs and bacon', 'veal bolognese', 'thanksgiving leftovers']

	for keyword in keywords:
		rf = RecipeFetcher()
		recipe_url = rf.search_recipes(keyword, max_amount=10)[0]
		recipe = rf.fetch_recipe(recipe_url)
		find_healthier_ingredients(recipe)
		print('*'*30)
		time.sleep(2)

