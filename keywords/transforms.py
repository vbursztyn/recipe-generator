def transformer(type, ingredient):
    # is the base type worth looking at?
    if type == "meatToVeg" and ingredient.baseType != "meatbase":
        return ingredient

meatToVegMap = {
    "generic": ["tofu", "tempeh", "seitan"],
    "chicken": ["tofu", "tempeh", "seitan"],
    "turkey": ["Tofurkey"],
    "turkey breast": ["Tofurkey"],
    "gelatin": ["pectin"],
    "bacon": ["Morningstar Farms Veggie Bacon Strips"],
    "bacon bit": ["Bac'n Pieces (Vegan)"],
    "bacon bits": ["Bac'n Pieces (Vegan)"],
    "burger": ["Impossible Burger", "Beyond Burger", "tofu"],
    "burgers": ["Impossible Burgers", "Beyond Burgers", "tofu"],
    "hamburger": ["Impossible Burger", "Beyond Burger", "tofu"],
    "hamburgers": ["Impossible Burgers", "Beyond Burgers", "tofu"],
    "hot dog": ["Smart Dog"],
    "hot dogs": ["Smart Dogs"],
    "beef": ["portobello mushrooms", "jackfruit"],
    "ground beef": ["Morningstar Farms Veggie Crumbles"],
    "beef bouillon": ["vegetable bouillon"],
    "beef broth": ["vegetable broth"],
    "beef stock": ["vegetable stock"],
    "dashi stock": ["vegetable stock"],
    "dashi broth": ["vegetable broth"],
    "chicken bouillon": ["vegetable bouillon"],
    "chicken broth": ["vegetable broth"],
    "chicken stock": ["vegetable stock"],
    "pork bouillon": ["vegetable bouillon"],
    "pork broth": ["vegetable broth"],
    "pork stock": ["vegetable stock"],
    "lard": ["margarine"],
    "shortening": ["margarine"],
    "gelatin": ["pectin"],
    "meatball": ["Gardein Classic Meatless Meatball"],
    "meatballs": ["Gardein Classic Meatless Meatballs"],
    "rib": ["tempeh"],
    "ribs": ["tempeh"],
    "marshmallow": ["Dandies Vegan Marshmallows"],
    "marshmallows": ["Dandies Vegan Marshmallows"],
    "sausage": ["Field Roast Vegan Sausage"],
    "sausages": ["Field Roast Vegan Sausages"],
    "oyster sauce": ["soy sauce"],
    "sushi": ["avocado"]
}

vegToMeatMap = {
    "tofu": ["chicken"],
    "tempeh": ["beef"],
    "seitan": ["pork"],
    "vegetable bouillon": ["chicken bouillon"],
    "vegetable broth": ["chicken broth"],
    "vegetable stock": ["chicken stock"],
    "vegetarian refried black beans": ["refried beans with lard"],
    "vegetarian black beans": ["pinto beans with lard"],
    "vegetarian beans": ["pinto beans with lard"],
    "black beans": ["pinto beans with lard"],
    "vegetarian baked beans": ["baked beans with lard"]
}

toHealthyMap = {
    "white rice": ["brown rice"],
    "lard": ["low-fat margarine"],
    "shortening": ["low-fat margarine"],
    "heavy cream": ["skim milk"],
    "cream": ["skim milk"],
    "milk": ["skim milk"],
    "egg": ["egg white"],
    "eggs": ["egg whites"],
    "lettuce": ["kale"],
    "mayonnaise": ["low-fat salad dressing"],
    "vegetable oil": ["olive oil", "coconut oil"],
    "canola oil": ["olive oil", "coconut oil"]
}

toUnhealthyMap = {
    "margarine": ["butter"],
    "butter": ["lard"],
    "egg white": ["egg"],
    "egg whites": ["eggs"],
    "brown rice": ["white rice"],
    "milk": ["heavy cream"],
    "skim milk": ["heavy cream"],
    "kale": ["lettuce"],
    "salad dressing": ["mayonnaise"],
    "olive oil": ["canola oil"],
    "coconut oil": ["canola oil"],
    "cooking spray": ["lard"],
    "black beans": ["pinto beans with lard"],
    "extra virgin olive oil": ["canola oil"]
}

reduceForHealth = ["salt","sugar","cream"]
