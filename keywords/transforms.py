TRANSFORMS = {}

transformer = []

# THESE FIRST TWO ARE LISTS USED BY INGREDIENT TRANSFORMER WHEN DECIDING WHAT TO DOUBLE OR HALVE FOR toHealthy/toUnhealthy
# Please add whatever makes sense...
TRANSFORMS["unhealthyIngredients"] = ["salt", "sugar", "brown sugar", "molasses", "cream"]
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
 'vanilla extract': ['taco seasoning', 'chili powder', 'cumin'],
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
# beginning of Piotr's automatically generated list
'garam masala': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'elbow macaroni': ['spaghetti', 'lasagna noodles', 'gnocchi'],
 'monterey jack cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'ketchup': ['teriyaki sauce', 'soy sauce'],
 'beef': ['dashi', 'round steak', 'ham'],
 'mozzarella cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'saffron': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'mayonnaise': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'cabbage': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'brussels sprouts': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'scallops': ['dashi', 'round steak', 'ham', 'beef'],
 'thyme': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'gnocchi': ['spaghetti', 'lasagna noodles'],
 'bacon': ['dashi', 'round steak', 'ham', 'beef'],
 'fresh mint': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'avocado': ['raisins', 'coconut', 'orange', 'lemon'],
 'green chiles': ['leeks', 'ginger', 'cucumber'],
 'sage': ['cilantro', 'basil'],
 'veal': ['dashi', 'round steak', 'ham', 'beef'],
 'italian-style salad dressing': ['teriyaki sauce',
  'soy sauce',
  'ketchup',
  'vinegar'],
 'green chilies': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'round steak': ['dashi'],
 'yellow squash': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'peas': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'parsley': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'shrimp': ['dashi', 'round steak', 'ham', 'beef'],
 'butter': ['oil'],
 'white bread': ['rice', 'potato', 'tortillas', 'rolled oats'],
 'chicken': ['dashi', 'round steak', 'ham', 'beef'],
 'quinoa': ['rice', 'potato', 'tortillas', 'rolled oats'],
 'cannellini beans': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'pear': ['raisins', 'coconut', 'orange', 'lemon'],
 'rum': ['sake', 'wine'],
 'kielbasa': ['dashi', 'round steak', 'ham', 'beef'],
 'bay leaves': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'italian seasoning': ['fennel seed',
  'star anise',
  'cardamom',
  'sesame seeds'],
 'margarine': ['oil', 'butter', 'shortening'],
 'dried cranberries': ['raisins', 'coconut', 'orange', 'lemon'],
 'cauliflower': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'capers': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'oyster sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'black olives': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'carrot': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'cinnamon': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'pinto beans': ['tofu', 'kidney beans', 'black beans', 'refried beans'],
 'fresh chives': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'broccoli': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'pork': ['dashi', 'round steak', 'ham', 'beef'],
 'american cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'fish sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'rolled oats': ['rice', 'potato', 'tortillas'],
 'ham': ['dashi', 'round steak'],
 'chili beans': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'garlic': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'sesame seeds': ['fennel seed', 'star anise', 'cardamom'],
 'tortillas': ['rice', 'potato'],
 'barbeque sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'onion': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'salt': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'tuna': ['dashi', 'round steak', 'ham', 'beef'],
 'cumin': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'provolone cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'worcestershire sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'vinegar': ['teriyaki sauce', 'soy sauce', 'ketchup'],
 'oregano': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'gochujang': ['miso paste', 'pumpkin puree'],
 'apple': ['raisins', 'coconut', 'orange', 'lemon'],
 'dill': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'shortening': ['oil', 'butter'],
 'poppy seeds': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'marinara sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'enchilada sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'ricotta cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'swiss cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'wine': ['sake'],
 'dried rosemary': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'refried beans': ['tofu', 'kidney beans', 'black beans'],
 'cardamom': ['fennel seed', 'star anise'],
 'lettuce': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'cottage cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'ginger': ['leeks'],
 'zucchini': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'celery': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'curry powder': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'chili sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'pumpkin puree': ['miso paste'],
 'taco seasoning': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'coconut': ['raisins'],
 'mango': ['raisins', 'coconut', 'orange', 'lemon'],
 'black beans': ['tofu', 'kidney beans'],
 'kidney beans': ['tofu'],
 'artichoke': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'lemon': ['raisins', 'coconut', 'orange'],
 'lamb': ['dashi', 'round steak', 'ham', 'beef'],
 'green beans': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'cloves': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'liquid smoke': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'star anise': ['fennel seed'],
 'bean sprouts': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'mustard': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'vanilla extract': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'feta cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese',
  'romano cheese'],
 'flank steak': ['dashi', 'round steak', 'ham', 'beef'],
 'pancetta': ['dashi', 'round steak', 'ham', 'beef'],
 'kale': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'lasagna noodles': ['spaghetti'],
 'hoisin sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'basil': ['cilantro'],
 'chili powder': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'romano cheese': ['processed cheese food',
  'parmesan cheese',
  'cheddar cheese'],
 'kernel corn': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'seafood seasoning': ['fennel seed',
  'star anise',
  'cardamom',
  'sesame seeds'],
 'shallot': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'sherry': ['raisins', 'coconut', 'orange', 'lemon'],
 'salsa': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'caraway seed': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'pasta sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'soy sauce': ['teriyaki sauce'],
 'pimento': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'banana': ['raisins', 'coconut', 'orange', 'lemon'],
 'potato': ['rice'],
 'spinach': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'pepper': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'cajun seasoning': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'paprika': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'bay leaf': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'turmeric': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'tomato': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'cheddar cheese': ['processed cheese food', 'parmesan cheese'],
 'nutmeg': ['fennel seed', 'star anise', 'cardamom', 'sesame seeds'],
 'barbecue sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'beer': ['sake', 'wine', 'rum'],
 'lime': ['raisins', 'coconut', 'orange', 'lemon'],
 'turkey': ['dashi', 'round steak', 'ham', 'beef'],
 'parmesan cheese': ['processed cheese food'],
 'ranch dressing': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'poultry seasoning': ['fennel seed',
  'star anise',
  'cardamom',
  'sesame seeds'],
 'mushrooms': ['leeks', 'ginger', 'cucumber', 'green chiles'],
 'strawberries': ['raisins', 'coconut', 'orange', 'lemon'],
 'orange': ['raisins', 'coconut'],
 'almon': ['dashi', 'round steak', 'ham', 'beef'],
 'hot sauce': ['teriyaki sauce', 'soy sauce', 'ketchup', 'vinegar'],
 'cucumber': ['leeks', 'ginger'],
# end of Piotr's automatically generated list
 'bell pepper': ['leeks', 'ginger', 'cucumber', 'green chiles'],
}

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
