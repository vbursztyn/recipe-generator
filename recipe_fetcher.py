from bs4 import BeautifulSoup


import requests


import re


class RecipeFetcher:

    
    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'
    
    
    def search_recipes(self, keyword): 
        search_url = self.search_base_url %('+'.join(keyword.split()))

        page_html = requests.get(search_url)
        page_graph = BeautifulSoup(page_html.content)

        return [recipe.a['href'] for recipe in\
               page_graph.find_all('div', {'class':'grid-card-image-container'})]
    
    
    def fetch_nutrition_facts(self, recipe_url):
        results = []

        nutrition_facts_url = '%s/fullrecipenutrition' %(recipe_url)

        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content)

        r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")

        for nutrient_row in page_graph.find_all('div', {'class':'nutrition-row'}):
            nutrient = {}

            tokens = nutrient_row.find('span',{'class':'nutrient-name'}).text.split(':')
            nutrient['name'] = tokens[0]
            (nutrient['amount'], nutrient['unit']) = r.match(tokens[1].strip()).groups()
            nutrient['daily_value'] = nutrient_row.find('span',{'class':'daily-value'})
            if nutrient['daily_value']:
                nutrient['daily_value'] = nutrient['daily_value'].text
            results.append(nutrient)

        return results
    
    
    def fetch_recipe(self, recipe_url):
        results = {}

        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content)

        results['ingredients'] = [ingredient.text for ingredient in\
                                  page_graph.find_all('span', {'itemprop':'recipeIngredient'})]

        results['directions'] = [direction.text.strip() for direction in\
                                 page_graph.find_all('span', {'class':'recipe-directions__list--item'})
                                 if direction.text.strip()]

        results['nutrition'] = self.fetch_nutrition_facts(recipe_url)

        return results
    
    def parse(self):
        # TO-DO
        pass


# rf = RecipeFetcher()
# feijoada = rf.search_recipes('feijoada')[1]
# rf.fetch_recipe(feijoada)