# recipe-generator
Project 2 for Northwestern's EECS 337.

1. pip install requirements.txt

If you want to regenerate contents in folder 'ingredient_data':

2. python populate_raw_data.py
3. Check if folder 'raw_data' has new files ('Products.csv' and 'Nutrients.csv'), then:
4. python calculate_similar_ingredients.py
5. Check if folder 'ingredient_data' has a new file ('similar_ingredients.pickle'), then:
6. python get_ingredient_nutrients.py

---

Current functionality:

* Search AllRecipes by keyword
* Given a recipe, extract ingredients and directions (unstructured)
* Given a recipe, extract nutritional data (structured)
* File 'similar_ingredients.pickle' has a dictionary with lists of substitutions for 780 ingredients based on similar flavor profile
* File 'ingredient_nutrients.pickle' has a dictionary with nutritional data for 243 of those 780 ingredients, i.e., ~31% of successful string matches on the USDA Food Composition Database
* Immediate TO-DO: A helper class to interface with the two pickle files
* Please see Issues for extended backlog