import nltk

class RecipeStep:
    def __init__(self):
        self.raw_step = ""
        self.action = ""
        self.action_position = (-1, -1)
        self.ingredients = []

# TODO: Hard-coded cooking actions for now. May want to read these from
# a separate file or try to parse based on context without knowing
# cooking-specific verbs.
cooking_verbs = {'add', 'adjust', 'arrange', 'bake', 'baste', 'beat', 'blend',
    'boil', 'braise', 'break', 'bread', 'broil', 'brown', 'brush', 'build',
    'burn', 'bury', 'carve', 'check', 'chill', 'chop', 'clarify', 'close',
    'cook', 'cool', 'correct', 'combine', 'cover', 'crack', 'crumple',
    'curdle', 'cut', 'debone', 'dice', 'discard', 'drain', 'dress', 'fillet',
    'flour', 'fold', 'freeze', 'fry', 'garnish', 'glaze', 'grate', 'grind',
    'grill', 'gut', 'heat', 'knead', 'lower', 'macerate', 'marinate', 'mash',
    'melt', 'mince', 'mix', 'open', 'parboil', 'pat', 'peel', 'pickle',
    'place', 'poach', 'pour', 'prepare', 'pull', 'put', 'preheat', 'reduce',
    'refrigerate', 'remove', 'rinse', 'roast', 'roll out', 'roll up', 'rub',
    'sauté', 'scoop', 'scorch', 'scramble', 'season', 'serve', 'set', 'simmer',
    'slice', 'slow', 'cook', 'soak', 'sour', 'spread', 'sprinkle', 'squeeze',
    'steam', 'steep', 'stir', 'strain', 'sweeten', 'thaw', 'thicken', 'toast',
    'warm', 'wash', 'water down', 'whip', 'whisk', 'wipe'}
# Possible conflicts; let's leave these out for now and parse via context clues later
#cooking_verbs = ['try', 'taste', 'sugar', 'spice', 'skim', 'salt', 'batter', 'spoon']

def parse_cooking_action(direction_tokens):
    # Take the first word that could be a valid step
    # TODO: Right now we'll miss compounds like "roll out"; needs fixing
    for i in range(len(direction_tokens)):
        if direction_tokens[i] in cooking_verbs:
            return direction_tokens[i], (i, i+1)
    return None, (-1, -1)

def parse_step_ingredients(direction_tokens, ingredients):
    ingr_extras = []
    for ingr in ingredients:
        namelist = ingr.name.lower().split(' ')
        if 'and' in namelist:
            namelist.remove('and') # Ugly hack
        ingr_extras.append({
            'ingredient': ingr,
            'namelist': tuple(namelist),
            'nameset': set(namelist)
        })

    for ingr in ingr_extras:
        positions = []
        start = -1
        namelist_start = -1
        for i in range(len(direction_tokens)):
            token = direction_tokens[i]
            if namelist_start >= 0:
                namelist_offset = namelist_start + i - start
                if namelist_offset >= len(ingr['namelist']) or token != ingr['namelist'][namelist_offset]:
                    positions.append((start, i))
                    start = -1
                    namelist_start = -1
            elif token in ingr['namelist']:
                namelist_start = ingr['namelist'].index(token)
                start = i

        if start >= 0:
            positions.append((start, len(direction_tokens)))

        ingr['positions'] = positions

        # Delete no longer needed fields
        del ingr['namelist']
        del ingr['nameset']

    return ingr_extras


def direction_to_recipe_step(direction, ingredients):
    tokens = nltk.word_tokenize(direction.lower())
    step = RecipeStep()
    step.raw_step = direction
    step.action, step.action_position = parse_cooking_action(tokens)
    step.ingredients = parse_step_ingredients(tokens, ingredients)
    return step

def split_steps(directions):
    # TODO: Eventually need to handle splitting compound sentences like "Chop
    # celery and mix with lettuce."
    if isinstance(directions, list):
        all_steps = []
        for substep in directions:
            all_steps.extend(split_steps(substep))
        return all_steps
    return nltk.sent_tokenize(directions)

def directions_to_recipe_steps(directions, ingredients):
    return [direction_to_recipe_step(d, ingredients) for d in split_steps(directions)]

def print_steps(steps):
    i = 1
    for step in steps:
        tokens = nltk.word_tokenize(step.raw_step.lower())
        insertion_list = []
        for ingr in step.ingredients:
            for pos in ingr['positions']:
                insertion_list.append((pos[0], '['))
                insertion_list.append((pos[1], ']'))
        if step.action is not None:
            insertion_list.append((step.action_position[0], '<'))
            insertion_list.append((step.action_position[1], '>'))
        insertion_list = sorted(insertion_list, reverse=True)
        for item in insertion_list:
            tokens.insert(item[0], item[1])
        print('Step {}: {}'.format(i, ' '.join(tokens)))
        i += 1

