import pickle


import os


import itertools


from get_ingredient_nutrients import rank_matches


from config import get_config


class NutritionalTransformation(object):


    def __init__(self):
        config = get_config()

        self.unhealthy_nutrients = ['Fatty acids, total saturated', 'Sugars, total', 'Sodium, Na']

        similar_ingredients_path = os.path.join(config['INGREDIENT_DATA'], config['SIMILAR_INGREDIENTS'])
        self.similar_ingredients = pickle.load(open(similar_ingredients_path, 'rb'))

        ingredient_nutrients_path = os.path.join(config['INGREDIENT_DATA'], config['INGREDIENT_NUTRIENTS'])
        self.ingredient_nutrients = pickle.load(open(ingredient_nutrients_path, 'rb'))


    def get_nutrient_for_ingredient(self, target_ingredient, nutrient):
        if not target_ingredient in self.ingredient_nutrients:
            return None
        result = [(ingredient['value'],ingredient['unit'])\
                  for ingredient in self.ingredient_nutrients[target_ingredient]\
                  if ingredient['name'] == nutrient]
        if not result:
            return None
        return result[0]


    def get_substitutions(self, original_ingredient, substitutions, criterion, healthier=True):
        baseline = self.get_nutrient_for_ingredient(original_ingredient, criterion)
        if not baseline:
            return None
        
        candidates = {}
        for substitution in substitutions:
            substitution_quality = self.get_nutrient_for_ingredient(substitution, criterion)
            # If we find this bad nutrient (criterion) in this substitution's nutrient profile;
            # If units match, then comparisons are straightforward;
            if (substitution_quality) and (baseline[1] == substitution_quality[1]):
                # Make it: HEALTHIER
                if healthier:
                    # If our baseline has more of this bad nutrient (criterion) than the substitution:
                    if (baseline[0] > substitution_quality[0]):
                        candidates[substitution] = (substitution_quality[0] / baseline[0]) * 100
                # Make it: TRASHIER
                else:
                    # If our baseline has less of this bad nutrient (criterion) than the substitution:
                    if (baseline[0] < substitution_quality[0]):
                        candidates[substitution] = substitution_quality[0] / (baseline[0] + 0.01) * 100
        
        top_cutoff = len(candidates)//10 if len(candidates) >= 20 else len(candidates)//2
        top_candidates = { k : v for k, v in itertools.islice(candidates.items(),top_cutoff) }
        
        if healthier: # HEALTHIER
            return [(k, top_candidates[k]) for k in sorted(top_candidates, key=top_candidates.get)]
        # TRASHIER
        return [(k, top_candidates[k]) for k in sorted(top_candidates, key=top_candidates.get, reverse=True)]


    def caption_substitutions(self, substitutions, bad_nutrient):
        captions = []
        bad_nutrient = bad_nutrient.split(',')[0]

        for substitution in substitutions:
            subst_name = substitution[0].replace('_',' ')
            if not substitution[1]:
                captions.append('%s (has approx. 0%% of %s)' %(subst_name, bad_nutrient))
            else:
                if substitution[1] < 100.0:
                    captions.append('%s (%.2f%% less %s)' %(subst_name, 100.0 - substitution[1], bad_nutrient))
                else:
                    captions.append('%s (%.2fx more %s)' %(subst_name, substitution[1] / 100.0, bad_nutrient))

        return captions


    def optimize_bad_nutrient(self, recipe, bad_nutrient, minimize=True):
        if minimize:
            results = '\nYou can make %s healthier by minimizing %s:\n\n' %(recipe.name, bad_nutrient)
        else:
            results = '\nYou can make %s unhealthier by maximizing %s:\n\n' %(recipe.name, bad_nutrient)
        
        ingredients = [ingredient.name for ingredient in recipe.allIngredients]
        all_ingredients = self.similar_ingredients.keys()
        matches = []
        for ingredient in ingredients:
            query = ingredient.replace(' ','_')
            match = rank_matches(query, all_ingredients, cutoff=2)
            if match:
                matches.append((ingredient, match[0]))
        
        for match in matches:
            similar_to_match = self.similar_ingredients[match[1]]
            # Make it: HEALTHIER
            if minimize:
                substitutions = self.get_substitutions(match[1], similar_to_match, bad_nutrient)
            # Make it: TRASHIER
            else:
                substitutions = self.get_substitutions(match[1], similar_to_match, bad_nutrient,\
                                                       healthier=False)
            if not substitutions:
                continue
            captions = self.caption_substitutions(substitutions, bad_nutrient)
            results += '- You can replace %s by %s.\n' %(match[0], ', '.join(captions))
        
        return results


    def find_healthier_ingredients(self, recipe):
        results = {}

        for bad_nutrient in self.unhealthy_nutrients:
            healthier_version = self.optimize_bad_nutrient(recipe, bad_nutrient)
            if '- You can replace' in healthier_version:
                results[healthier_version] = len(healthier_version)
        
        if len(results):
            return sorted(results, key=results.get, reverse=True)[0]

        return None


    def find_trashier_ingredients(self, recipe):
        results = {}

        for bad_nutrient in self.unhealthy_nutrients:
            healthier_version = self.optimize_bad_nutrient(recipe, bad_nutrient, minimize=False)
            if '- You can replace' in healthier_version:
                results[healthier_version] = len(healthier_version)
        
        if len(results):
            return sorted(results, key=results.get, reverse=True)[0]

        return None

