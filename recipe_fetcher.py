from bs4 import BeautifulSoup

from get_cuisine_characteristics import random_sleep

from config import get_config

import requests

import re

config = get_config()


class RecipeFetcher:


    search_base_url = 'https://www.allrecipes.com/search/results/?wt=%s&sort=re'


    def search_recipes(self, keyword, max_amount = 100):
        result = []
        
        search_url = self.search_base_url %('+'.join(keyword.split()))
        
        page = 1
        while len(result) < max_amount:
            request_url = search_url + '&page=' + str(page)
            page_html = requests.get(request_url)
            page_graph = BeautifulSoup(page_html.content, features="lxml")
            recipes_on_page = [recipe.a['href'] for recipe in\
               page_graph.find_all('div', {'class':'grid-card-image-container'})]
            for url in recipes_on_page:
                result.append(url)
            page = page + 1
            random_sleep(config['SAFE_REQUEST_INTERVAL'])
        return result[:max_amount]


    def fetch_nutrition_facts(self, recipe_url):
        results = []

        nutrition_facts_url = '%s/fullrecipenutrition' %(recipe_url)

        page_html = requests.get(nutrition_facts_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")

        r = re.compile("([0-9]*\.?[0-9]*)([a-zA-Z]+)")

        for nutrient_row in page_graph.find_all('div', {'class':'nutrition-row'}):
            nutrient = {}

            tokens = nutrient_row.find('span',{'class':'nutrient-name'}).text.split(':')
            nutrient['name'] = tokens[0]
            
            # some nutrient information starts with an inequality that we clean up 
            if tokens[1][:3] == ' < ':
                tokens[1] = tokens[1][2:]
                
            (nutrient['amount'], nutrient['unit']) = r.match(tokens[1].strip()).groups()
            nutrient['daily_value'] = nutrient_row.find('span',{'class':'daily-value'})
            if nutrient['daily_value']:
                nutrient['daily_value'] = nutrient['daily_value'].text
            results.append(nutrient)

        return results


    def fetch_recipe(self, recipe_url, include_nutrients=True):
        # print(recipe_url)
        results = {}

        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")

        results['name'] = page_graph.find("h1", {"id": "recipe-main-content", "itemprop": "name"}).text

        results['ingredients'] = [ingredient.text for ingredient in\
                                  page_graph.find_all('span', {'itemprop':'recipeIngredient'})]

        results['directions'] = [direction.text.strip() for direction in\
                                 page_graph.find_all('span', {'class':'recipe-directions__list--item'})
                                 if direction.text.strip()]

        if include_nutrients: # Made optional to avoid unnecessary requests
            results['nutrition'] = self.fetch_nutrition_facts(recipe_url)

        return results
    
    # fetches the first max_amount reviews of a given allrecipe, returning them as a list of strings
    def fetch_reviews(self, recipe_url : str, max_amount = 1000):
    
        # we first request the page of the recipe 
        page_html = requests.get(recipe_url)
        page_graph = BeautifulSoup(page_html.content, features="lxml")
    
        # we then check if there are any reviews
        result = []
        next_review_element = page_graph.find("a", class_="review-detail__link")
    
        review_counter = 0
        while next_review_element:
            review_html = requests.get(next_review_element['href'])
            review_graph = BeautifulSoup(review_html.content, features="lxml")
            result.append(review_graph.find_all("meta")[4]['content'])
            next_review_element = review_graph.find("link", attrs={'rel': 'next' })
            random_sleep(config['SAFE_REQUEST_INTERVAL'])
        
            # if we crossed the maximal amount of reviews, we break the loop
            review_counter = review_counter + 1
            if review_counter >= max_amount:
                break
            
        return result

    def parse(self):
        # TO-DO
        pass


# rf = RecipeFetcher()
# feijoada = rf.search_recipes('feijoada')[1]
# rf.fetch_recipe(feijoada)
