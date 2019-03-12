# recipe-generator
Project 2 for Northwestern's EECS 337.  
Developed by: Andrew Paley, Mike D'Arcy, Piotr Pstragowski, Victor Bursztyn.
Github: https://github.com/vbursztyn/recipe-generator

Basic setup and execution:

* pip install -r requirements.txt
* python main.py

---

How to use it?:  

After running, the program first asks the user to provide an url to a recipe from allrecipes.com. The given recipe is then fetched and parsed, and the user is presented with the following choices to modify it. 

0. Make it vegetarian: 

- This will modify the recipe by making it vegetarian while keeping it as close to the original as possible. This means that meat products will be replaced by their closest vegetarian substitutes. 

- After modifying the recipe, the program will print out the new version in a human-readable format, as a list of ingredients followed by a list of steps that should be followed by the user. To make it easier to spot the differneces between this and the original recipe, the program will also highlight the changes which were made. 

- The user will then be presented with an option to apply a different transformation or start working with a different recipe. Note that these changes are not cumulative, one always starts with the original recipe. This applies to all of the transformations below. 

1. Make it un-vegetarian: 

- These will modify the recipe by making it non-vegetarian, that is, by adding in meat products. 

2. Make it healthier: 

- This will try to make the recipe healthier. This will be done by trying to find healthier substitutes of given ingredients (for example, replacing white rice with brown rice) but also by trying to change the amounts of certain ingredients known to be unhealthy in large amounts (for example, the program might suggest to halve the amount of salt).
- If the program identifies that one or more of said healthier substitutes decrease a bad nutrient (saturated fat, sugars or sodium), the measurable benefits are indicated, e.g., "replaced cheese A with cheese B (50% less fat)" or "replaced bean A with bean B (50% less sodium)."

3. Make it less healthy: 

- This does the opposite of the previous transformation. That is, it will suggest to replace certain ingredients with less healthy ones (for example, to replace chicken with steak) as well as to increase the amount of unhealthy ingredients.
- If the program identifies that one or more of said unhealthy substitutes increase a bad nutrient (saturated fat, sugars or sodium), the measurable disadvantages are indicated, e.g., "replaced cheese B with cheese A (2x more fat)" or "replaced bean B with bean A (2x more sodium)."

4. Switch it to a different cuisine: 

- The program will ask the user to specify the cuisine to which the recipe should be transformed, with three choices: Italian, Mexican and Japanese.

- The recipe will be transformed by substituting ingredients towards ones which are more popular in a given cuisine. For example, a transformation towards Italian cuisine might replace ketchup with marinara sauce, and a transformation towards Japanese might replace potatoes with rice. Note that these are stereotypical examples, but in fact the list of ingredients which can be substituted is quite extensive. 

5. Start over with a new recipe.

- This asks the user to provide another url to allrecipes.com, the recipe will then be loaded and the above transformations can be applied to it. 

How does it work?: 

Recipe Parsing: The url containing the requested allrecipes.com recipe is fetched using requests and then the relevant data is extracted using BeautifulSoup. 

The ingredients on allrecipes.com are conveniently listed one-by-one and so can be parsed separately. When parsing each such ingredient, the program looks for words that describe size ("large" etc.), flavour ("sweet"), type ("dried"), healthiness ("lean") as well as for descriptions of quantity (ie. the amount and units, of which there is a variety). The words that are left are assumed to be the proper name of the ingredient, this is then matched against lists of ingredients to determine the type (lists of ingredients of given type are stored in meats.csv, cheeses.csv, etc. in keywords/). 

The steps are then parsed by using regular expressions involving the ingredients (which are known from the step before) and an extensive list of cooking verbs. The steps are stored in their entirity, together with the additional information of the cooking verbes and ingredients involved. 

Recipe Transformations: 

All transformations use ingredient substitutions lists, for example, that suggest that if one wants to make a recipe vegetable then a good substitute for chicken is tofu, and that in italian cuisine zucchini would often be used instead of eggplant. Since the cooking steps are already parsed with ingredients extracted, the substitution is also done there. 

These lists are long and for any given ingredient they might be several good substitutes, one is then chosen randomly. Care is taken to not make too many substitutions and to not to overuse any ingredient, with the exception of "to vegetarian" transformation which will indiscriminately replace all meat. 

Additionally, in some cases an ingredient might be added on its own, without replacing another one. This happens, for example, in the case of "to non-vegetarian" transformation if there is no suitable ingredient that could be replaced by meat, similarly in the case of "to given cuisine" transformations. 

Moreover, in the case of "to healthy" and "to unhealthy" transformations, some ingredients will be kept but the program will suggest to change the amount. An example here is lowering the salt content, or the amount of saturated fats. 

All of the ingredient substitution lists are stored in keywords/transforms.py. 

In the case of "to healthy/unhealthy", the ingredient substitutions were obtained by parsing the USDA nutritional data and matching it against the list of ingredients, the results are saved in ingredient_data/ingredient_nutrients.pickle. This data is not accessed at runtime, only the prepared generated substitution lists are. 

In the case of "to Italian/Mexican/Japanese", the ingredient subtitution lists were obtained by downloading a large sample of recipes from allrecipes.com (stored in allrecipe_data/allrecipes_db.pickle) and computing which ingredients occur disproportianately often in recipes corresponding to a given cuisine. The lists were then created by mapping an ingredient of a given-type to a "highly-scoring" ingredient of the same type. These were then cleaned-up by hand to remove subtitutions that seem unlikely to yield satisfactory results. 

In the case of "to vegetarian/non-vegetarian" the lists were written by hand and follow standard vegetarian guidelines for making a recipe meatless (for example, replacing chicken by tofu and beef by jackfruit) or their reverse.

---

The following datasets were partially included or consulted in the course of this project:

1. USDA - Food Composition Database at https://www.ars.usda.gov/ARSUserFiles/80400525/Data/BFPDB/BFPD_csv_07132018.zip (used in "2. Make it healthier" and "3. Make it less healthy")

2. FooDB - Food Component Database at http://foodb.ca/ (used as seed for our manually enriched lists, which in turn are used in all transformations)