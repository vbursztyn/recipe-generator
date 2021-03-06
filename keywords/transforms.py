# This file contains the ingredient subtitution lists for the needed recipe transformations

TRANSFORMS = {}

transformer = []

# THESE FIRST TWO ARE LISTS USED BY INGREDIENT TRANSFORMER WHEN DECIDING WHAT TO DOUBLE OR HALVE FOR toHealthy/toUnhealthy
TRANSFORMS["unhealthyIngredients"] = ["salt", "sugar", "brown sugar", "molasses", "cream", "mayonnaise"]
TRANSFORMS["unhealthyBaseTypes"] = ["oil", "cheese"]

TRANSFORMS["italian"] = {
    # Piotr's automatically generated list now blended with Victor's found keywords and hand-culled
    'garam masala': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'elbow macaroni': ['spaghetti', 'gnocchi'],
    'monterey jack cheese': ['ricotta cheese','mozzarella cheese'],
    'ketchup': ['marinara sauce'],
    'saffron': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'cabbage': ['kale', 'yellow squash', 'zucchini', 'spinach'],
    'bacon': ['pancetta'],
    'green chiles': ['red bell pepper'],
    'green chilies': ['red bell peppers'],
    'kielbasa': ['italian sausage'],
    'bay leaves': ["parsley", "oregano"],
    'margarine': ['olive oil'],
    'cauliflower': ['yellow squash', 'zucchini'],
    'teriyaki sauce': ['balsamic vinaigrette'],
    'mirin': ['balsamic vinaigrette'],
    'sesame oil': ["olive oil"],
    'pinto beans': ['kidney beans'],
    'rice vinegar': ["balsamic vinegar"],
    'fresh chives': ['red onion'],
    'chives': ['red onion'],
    'broccoli': ['yellow squash', 'zucchini'],
    'american cheese': ['mozzarella cheese'],
    'chili beans': ['kidney beans'],
    'sesame seeds': ["fennel seed"],
    'barbeque sauce': ['marinara sauce','italian-style salad dressing'],
    'processed cheese food': ['ricotta cheese','mozzarella cheese'],
    'cumin': ['italian seasoning', 'oregano','crushed red pepper'],
    'cumin seeds': ['fennel seeds'],
    'worcestershire sauce': ['italian-style salad dressing'],
    'gochujang': ['pumpkin puree'],
    'shortening': ['olive oil', 'butter'],
    'poppy seeds': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'enchilada sauce': ['marinara sauce','italian-style salad dressing'],
    'swiss cheese': ['mozzarella cheese'],
    'sake': ['red wine'],
    'refried beans': ['kidney beans'],
    'cardamom': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'cottage cheese': ['ricotta cheese'],
    'ginger': ['kale', 'yellow squash', 'zucchini', 'spinach'],
    'dashi': ['polenta'],
    'curry powder': ["crushed red pepper", "black pepper", "garlic powder"],
    'cayenne pepper': ["crushed red pepper", "black pepper", "garlic powder"],
    'chili sauce': ['marinara sauce','italian-style salad dressing'],
    'taco seasoning': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'black beans': ['kidney beans'],
    'green beans': ['zucchini'],
    'star anise': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'bean sprouts': ['kale', 'yellow squash', 'zucchini', 'spinach'],
    'cilantro': ['sage', 'basil'],
    'coriander': ['sage', 'basil'],
    'feta cheese': ['ricotta cheese','mozzarella cheese','parmesan cheese','romano cheese'],
    'hoisin sauce': ['balsamic glaze'],
    'chili powder': ["crushed red pepper", "black pepper", "garlic powder"],
    'seafood seasoning': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'sherry': ['marsala'],
    'salsa': ['marinara sauce'],
    'soy sauce': ["extra virgin olive oil"],
    'cajun seasoning': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'paprika': ["crushed red pepper", "black pepper", "garlic powder"],
    'turmeric': ["italian seasoning", "oregano", "basil", "parsley", "black pepper"],
    'cheddar cheese': ['ricotta cheese','mozzarella cheese'],
    'barbecue sauce': ["balsamic glaze"],
    'beer': ['red wine'],
    'turkey': ['italian sausage'],
    'ranch dressing': ['balsamic vinaigrette'],
    'poultry seasoning': ['italian seasoning', 'oregano', 'parsley'],
    'mushrooms': ['porcini mushrooms'],
    'hot sauce': ['Naples Drizzle'],
    'cucumber': ['yellow squash', 'zucchini'],
    'jalapeño': ["red pepper"],
    'jalapeno': ["red pepper"]
 }

TRANSFORMS['mexican'] = {
# beginning of Piotr's automatically generated list
 'garam masala': ['taco seasoning', 'cumin', 'chili powder'],
 'ketchup': ['enchilada sauce'],
 'beef': ['flank steak'],
 'mozzarella cheese': ['monterey jack cheese', 'cheddar cheese'],
 'rice': ['corn kernel', 'quinoa'],
 'saffron': ['cumin'],
 'scallops': ['shrimp'],
 'thyme': ['fresh cilantro', 'salsa', 'fresh mint'],
 'bacon': ['flank steak'],
 'fresh mint': ['fresh cilantro', 'salsa', 'fresh mint'],
 'green chiles': ['chili beans', 'black beans'],
 'sage': ['fresh cilantro', 'salsa', 'fresh mint'],
 'veal': ['flank steak'],
 'italian-style salad dressing': ['enchilada sauce'],
 'green chilies': ['chili beans'],
 'round steak': ['flank steak'],
 'yellow squash': ['chili beans', 'black beans'],
 'leeks': ['fresh cilantro', 'salsa', 'fresh mint'],
 'peas': ['corn kernel'],
 'parsley': ['fresh cilantro', 'salsa', 'fresh mint'],
 'butter': ['olive oil'],
 'white bread': ['tortillas'],
 'cannellini beans': ['chili beans', 'black beans'],
 'pear': ['avocado'],
 'miso paste': ['taco seasoning', 'cumin', 'chili powder'],
 'oil': ['olive oil'],
 'kielbasa': ['flank steak'],
 'bay leaves': ['fresh cilantro', 'salsa', 'fresh mint'],
 'italian seasoning': ['taco seasoning', 'cumin', 'chili powder'],
 'margarine': ['olive oil'],
 'dried cranberries': ['avocado'],
 'capers': ['black olives'],
 'oyster sauce': ['enchilada sauce'],
 'teriyaki sauce': ['enchilada sauce'],
 'carrot': ['black olives'],
 'cinnamon': ['cumin'],
 'pinto beans': ['refried beans', 'black beans'],
 'fresh chives': ['fresh cilantro', 'salsa', 'fresh mint'],
 'pork': ['flank steak'],
 'american cheese': ['monterey jack cheese','cheddar cheese'],
 'fish sauce': ['enchilada sauce'],
 'rolled oats': ['quinoa'],
 'ham': ['flank steak'],
 'sesame seeds': ['taco seasoning', 'chili powder', 'cumin'],
 'barbecue sauce': ['enchilada sauce'],
 'onion': ['green onion'],
 'onions': ['green onions'],
 'processed cheese food': ['monterey jack cheese'],
 'tofu': ['refried beans', 'black beans'],
 'tuna': ['shrimp'],
 'provolone cheese': ['monterey jack cheese', 'cheddar cheese'],
 'worcestershire sauce': ['enchilada sauce'],
 'oregano': ['fresh cilantro', 'salsa', 'fresh mint'],
 'apple': ['avocado'],
 'dill': ['fresh cilantro', 'salsa', 'fresh mint'],
 'poppy seeds': ['taco seasoning', 'chili powder', 'cumin'],
 'marinara sauce': ['enchilada sauce'],
 'ricotta cheese': ['monterey jack cheese', 'cheddar cheese'],
 'swiss cheese': ['monterey jack cheese', 'cheddar cheese'],
 'dried rosemary': ['taco seasoning', 'chili powder', 'cumin'],
 'cardamom': ['taco seasoning', 'chili powder', 'cumin'],
 'cottage cheese': ['monterey jack cheese', 'cheddar cheese'],
 'ginger': ['jalapeño pepper'],
 'zucchini': ['kernel corn'],
 'curry powder': ['chili powder'],
 'fennel seed': ['taco seasoning', 'chili powder', 'cumin'],
 'coconut': ['avocado'],
 'mango': ['avocado'],
 'artichoke': ['black olives'],
 'lamb': ['flank steak'],
 'green beans': ['chili beans', 'black olives', 'kernel corn'],
 'star anise': ['taco seasoning', 'chili powder', 'cumin'],
 'bean sprouts': ['chili beans', 'black olives', 'kernel corn'],
 'mustard': ['enchilada sauce'],
 'vanilla extract': ['agave'],
 'feta cheese': ['monterey jack cheese','cheddar cheese'],
 'pancetta': ['flank steak'],
 'hoisin sauce': ['enchilada sauce'],
 'basil': ['fresh cilantro', 'salsa', 'fresh mint'],
 'romano cheese': ['monterey jack cheese', 'cheddar cheese'],
 'seafood seasoning': ['taco seasoning', 'chili powder', 'cumin'],
 'shallot': ['green onion'],
 'sherry': ['avocado'],
 'caraway seed': ['taco seasoning', 'chili powder', 'cumin'],
 'pasta sauce': ['enchilada sauce'],
 'soy sauce': ['enchilada sauce'],
 'banana': ['avocado'],
 'pepper': ['jalapeño pepper'],
 'paprika': ['taco seasoning', 'chili powder', 'cumin'],
 'bay leaf': ['fresh cilantro', 'salsa', 'fresh mint'],
 'turmeric': ['taco seasoning', 'chili powder', 'cumin'],
 'cheddar cheese': ['monterey jack cheese', 'cheddar cheese'],
 'nutmeg': ['taco seasoning', 'chili powder', 'cumin'],
 'barbecue sauce': ['enchilada sauce'],
 'turkey': ['flank steak', 'chicken'],
 'parmesan cheese': ['monterey jack cheese', 'cheddar cheese'],
 'ranch dressing': ['enchilada sauce'],
 'poultry seasoning': ['taco seasoning', 'chili powder', 'cumin'],
 'mushrooms': ['chili beans', 'black olives', 'kernel corn'],
 'strawberries': ['avocado'],
 'orange': ['lime'],
 'salmon': ['shrimp'],
 'hot sauce': ['jalapeño pepper']
}


TRANSFORMS["japanese"] = {
 'garam masala': ['sesame seeds'],
 'elbow macaroni': ['udon noodles'],
 'monterey jack cheese': ['tofu'],
 'ketchup': ['teriyaki sauce'],
 'beef': ['pork'],
 'mozzarella cheese': ['tofu'],
 'saffron': ['ginger'],
 'mayonnaise': ['cream cheese'],
 'brussels sprouts': ['cucumber'],
 'thyme': ['ginger'],
 'gnocchi': ['buckwheat gnocchi'],
 'bacon': ['dashi', 'round steak', 'ham', 'beef'],
 'fresh mint': ['ginger'],
 'green chiles': ['leeks', 'ginger', 'cucumber'],
 'sage': ['ginger'],
 'veal': ['pork'],
 'italian-style salad dressing': ['teriyaki sauce', 'soy sauce'],
 'green chilies': ['ginger'],
 'round steak': ['pork'],
 'peas': ['edamame'],
 'parsley': ['ginger'],
 'butter': ['sesame oil'],
 'chicken': ['pork'],
 'quinoa': ['edamame'],
 'cannellini beans': ['edamame'],
 'rum': ['sake'],
 'kielbasa': ['smoked tofu'],
 'bay leaves': ['ginger'],
 'italian seasoning': ['soy sauce', 'teriyaki sauce'],
 'margarine': ['sesame oil'],
 'capers': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'oyster sauce': ['teriyaki sauce', 'soy sauce'],
 'black olives': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'cinnamon': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'pinto beans': ['edamame'],
 'american cheese': ['tofu'],
 'fish sauce': ['teriyaki sauce', 'soy sauce'],
 'rolled oats': ['rice', 'potato', 'tortillas'],
 'ham': ['pork'],
 'chili beans': ['smoked tofu'],
 'garlic': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'sesame seeds': ['fennel seed', 'star anise', 'cardamom'],
 'tortillas': ['rice', 'potato'],
 'barbeque sauce': ['teriyaki sauce'],
 'onion': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'salt': ['soy sauce'],
 'cumin': ['ginger'],
 'provolone cheese': ['tofu'],
 'worcestershire sauce': ['teriyaki sauce', 'soy sauce'],
 'vinegar': ['mirin', 'rice vinager'],
 'oregano': ['sesame seeds'],
 'gochujang': ['miso paste'],
 'dill': ['ginger'],
 'shortening': ['sesame oil'],
 'poppy seeds': ['sesame seeds'],
 'marinara sauce': ['teriyaki sauce', 'soy sauce'],
 'enchilada sauce': ['teriyaki sauce', 'soy sauce'],
 'ricotta cheese': ['tofu'],
 'swiss cheese': ['tofu'],
 'wine': ['sake'],
 'refried beans': ['tofu'],
 'cardamom': ['ginger'],
 'cottage cheese': ['tofu'],
 'zucchini': ['cucumber'],
 'curry powder': ['wasabi'],
 'chili sauce': ['wasabi'],
 'pumpkin puree': ['miso paste'],
 'taco seasoning': ['wasabi'],
 'black beans': ['tofu'],
 'kidney beans': ['tofu'],
 'artichoke': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'lamb': ['pork'],
 'green beans': ['edamame'],
 'cloves': ['sesame seeds'],
 'star anise': ['fennel seed'],
 'bean sprouts': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'mustard': ['teriyaki sauce', 'soy sauce'],
 'vanilla extract': ['teriyaki sauce'],
 'feta cheese': ['tofu'],
 'flank steak': ['pork'],
 'pancetta': ['pork'],
 'kale': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'lasagna noodles': ['udon noodles'],
 'hoisin sauce': ['teriyaki sauce', 'soy sauce'],
 'basil': ['ginger'],
 'chili powder': ['wasabi'],
 'romano cheese': ['tofu'],
 'kernel corn': ['edamame'],
 'corn': ['edamame'],
 'seafood seasoning': ['soy sauce'],
 'salsa': ['ginger'],
 'caraway seed': ['sesame seeds'],
 'pasta sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'pimento': ['wasabi'],
 'jalapeño pepper' : ['wasabi'],
 'pepper': ['wasabi'],
 'cajun seasoning': ['wasabi'],
 'paprika': ['ginger'],
 'bay leaf': ['ginger'],
 'turmeric': ['ginger'],
 'tomato': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'cheddar cheese': ['tofu'],
 'nutmeg': ['garlic'],
 'barbecue sauce': ['teriyaki sauce', 'soy sauce'],
 'beer': ['sake'],
 'turkey': ['pork'],
 'parmesan cheese': ['tofu'],
 'ranch dressing': ['teriyaki sauce', 'soy sauce'],
 'poultry seasoning': ['soy sauce'],
 'mushrooms': ['shitake'],
 'hot sauce': ['wasabi'],
# end of Piotr's automatically generated list
 'bell pepper': ['ginger', 'cucumber'],
}

TRANSFORMS["meatToVeg"] = {
    "generic": ["tofu", "tempeh", "seitan"],
    "chicken": ["tofu", "tempeh", "seitan"],
    "turkey": ["Tofurkey"],
    "turkey breast": ["Tofurkey"],
    "gelatin": ["pectin"],
    "bacon": ["Morningstar Farms Veggie Bacon Strips"],
    "canadian bacon": ["Morningstar Farms Veggie Bacon Strips"],
    "bacon bit": ["Bac'n Pieces (Vegan)"],
    "bacon bits": ["Bac'n Pieces (Vegan)"],
    "burger": ["Impossible Burger", "Beyond Burger", "tofu"],
    "burgers": ["Impossible Burgers", "Beyond Burgers", "tofu"],
    "hamburger": ["Impossible Burger", "Beyond Burger", "tofu"],
    "hamburgers": ["Impossible Burgers", "Beyond Burgers", "tofu"],
    "hot dog": ["Smart Dog"],
    "hot dogs": ["Smart Dogs"],
    "steak": ["portobello mushrooms", "jackfruit"],
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
    "pork": ["tofu", "tempeh", "seitan"],
    "pork tenderloin": ["tofu", "tempeh", "seitan"],
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
    "sushi": ["avocado"],
    "anchovies": ["marinated olives"]
}

TRANSFORMS["vegToMeat"] = {
    "tofu": ["chicken","beef","pork"],
    "tempeh": ["chicken","beef","pork"],
    "seitan": ["chicken","beef","pork"],
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
    "bacon": ["turkey bacon"],
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
    "mayonnaise": ["Vegenaise"],
    "vegetable oil": ["olive oil", "coconut oil"],
    "canola oil": ["olive oil", "coconut oil"],
    "vegetable broth": ["water"],
    "beef broth": ["water"],
    "chicken broth": ["water"],
    "sugar": ["honey","agave"], # Victor's suggestions
    "ketchup": ["fresh tomato sauce"],
    "salmon": ["wild salmon"],
    "chicken": ["lean turkey"]
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
    "extra virgin olive oil": ["canola oil"],
    "honey": ["white sugar"], # Victor's suggestions
    "agave": ["white sugar"],
    "tomato sauce": ["ketchup"],
    "marinara sauce": ["ketchup"],
    "marinara" : ["ketchup"],
    "beef": ["rib-eye steak"],
    "chicken": ["rib-eye steak"],
    "turkey": ["rib-eye steak"],
    "veal": ["rib-eye steak"],
    "salmon": ["rib-eye steak"],
    "tuna": ["rib-eye steak"],
    "cod": ["rib-eye steak"],
    "whitefish": ["rib-eye steak"]
}
