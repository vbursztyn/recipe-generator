TRANSFORMS = {}

# THESE FIRST TWO ARE LISTS USED BY INGREDIENT TRANSFORMER WHEN DECIDING WHAT TO DOUBLE OR HALVE FOR toHealthy/toUnhealthy
# Please add whatever makes sense...
TRANSFORMS["unhealthyIngredients"] = ["salt", "sugar", "brown sugar", "molasses", "cream"]
TRANSFORMS["unhealthyBaseTypes"] = ["oil", "cheese"]

TRANSFORMS["meatToVeg"] = {
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

TRANSFORMS["vegToMeat"] = {
    "tofu": ["chicken"],
    "tempeh": ["beef"],
    "seitan": ["pork"],
    "vegetable bouillon": ["chicken bouillon"],
    "vegetable broth": ["chicken broth"],
    "vegetable stock": ["chicken stock"],
    "refried black beans": ["refried beans with lard"],
    "black beans": ["pinto beans with lard"],
    "beans": ["pinto beans with lard"],
    "baked beans": ["baked beans with lard"],
    "kidney beans": ["pinto beans with lard"]
}

TRANSFORMS["toHealthy"] = {
    "beef": ["chicken"],
    "hamburger": ["turkey burger"],
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
    "canola oil": ["olive oil", "coconut oil"],
    "vegetable broth": ["water"],
    "beef broth": ["water"],
    "chicken broth": ["water"]
}

TRANSFORMS["toUnhealthy"] = {
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
