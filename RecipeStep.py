import nltk
from keywords.cooking_verbs import COOKING_VERBS
from keywords.units import UNITS
import copy

class RecipeStep:
    def __init__(self):
        self.raw_step = ""
        self.tokens = []
        self.action = ""
        self.action_position = (-1, -1)
        self.ingredients = []

def intervals_overlap(interval1, interval2):
    """Assumes each interval is already sorted. This function also assumes
    half-open intervals, so if interval1[1] == interval2[0] that does NOT count
    as overlapping."""
    if interval1[0] <= interval2[0]:
        return interval2[0] < interval1[1]
    return interval1[0] < interval2[1]

class RecipeDirectionsParser:
    def __init__(self, raw_directions, ingredients):
        self.raw_directions = raw_directions
        self.ingredients = ingredients
        self.steps = []
        self.placeholders = dict()

        self.raw_steps = self._split_steps(raw_directions)
        for step in self.raw_steps:
            self.steps.append(self.direction_to_recipe_step(step))

    def get_steps(self):
        return self.steps

    def _parse_cooking_action(self, direction_tokens):
        # Take the first word that could be a valid step
        # TODO: Right now we'll miss compounds like "roll out"; needs fixing
        for i in range(len(direction_tokens)):
            if direction_tokens[i] in COOKING_VERBS:
                return direction_tokens[i], (i, i+1)
        return None, (-1, -1)

    def _disambiguate_overlapping_ingredients(self, direction_tokens, ingr_extras):
        # TODO: Nesting is not deep enough here. Needs more levels of indentation
        for i, ingr1 in enumerate(ingr_extras):
            for j, ingr2 in enumerate(ingr_extras[(i+1):]):
                for interval1 in ingr1['positions']:
                    for interval2 in ingr2['positions']:
                        if intervals_overlap(interval1, interval2):
                            intervalsize1 = interval1[1] - interval1[0]
                            intervalsize2 = interval2[1] - interval2[0]
                            if intervalsize1 < intervalsize2:
                                ingr1['positions'].remove(interval1)
                            elif intervalsize2 < intervalsize1:
                                ingr2['positions'].remove(interval2)
                            else:
                                # TODO: Check for a size keyword in front of the
                                # ingredient and choose intelligently. Currently we
                                # just default to removing ingr2
                                ingr2['positions'].remove(interval2)

    def _parse_step_ingredients(self, direction_tokens):
        ingr_extras = []
        for ingr in self.ingredients:
            namelist = ingr.name.lower().split(' ')
            ingr_extras.append({
                'ingredient': ingr,
                'positions': [],
                'namelist': tuple(namelist),
                'nameset': set(namelist)
            })

        all_ingr_positions = []

        for ingr in ingr_extras:
            start = -1
            namelist_start = -1
            for i in range(len(direction_tokens)):
                token = direction_tokens[i]
                if namelist_start >= 0:
                    namelist_offset = namelist_start + i - start
                    if namelist_offset >= len(ingr['namelist']) or token != ingr['namelist'][namelist_offset]:
                        ingr['positions'].append((start, i))
                        start = -1
                        namelist_start = -1
                elif token in ingr['namelist']:
                    namelist_start = ingr['namelist'].index(token)
                    start = i

            if start >= 0:
                ingr['positions'].append((start, len(direction_tokens)))

            # Delete no longer needed fields
            del ingr['namelist']
            del ingr['nameset']


        self._disambiguate_overlapping_ingredients(direction_tokens, ingr_extras)

        return ingr_extras

    def _sub_units2placeholders(self, raw_direction):
        # TODO: Implement this method
        return raw_direction

    def direction_to_recipe_step(self, direction):
        direction = direction.lower()
        step = RecipeStep()
        step.tokens = nltk.word_tokenize(direction.lower())
        step.raw_step = direction
        step.action, step.action_position = self._parse_cooking_action(step.tokens)
        step.ingredients = self._parse_step_ingredients(step.tokens)
        return step

    def _split_steps(self, directions):
        # TODO: Eventually need to handle splitting compound sentences like "Chop
        # celery and mix with lettuce."
        if isinstance(directions, list):
            all_steps = []
            for substep in directions:
                all_steps.extend(self._split_steps(substep))
            return all_steps
        return nltk.sent_tokenize(directions)

def modify_steps(steps, ingr_subs):
    """Note: ingr_subs should be a list of pairs like [(old_ingr1, new_ingr1),
    ...]. This method substitutes by checking if the "statement" field of an
    old_ingr matches that of an existing ingredient in a step."""

    new_steps = copy.deepcopy(steps)

    sub_positions = []

    for step_num, step in enumerate(new_steps):
        for i in range(len(step.ingredients)):
            ingr1 = step.ingredients[i]
            for old_ingr2, new_ingr2 in ingr_subs:
                if ingr1['ingredient'].statement == old_ingr2.statement:
                    step.ingredients[i]['ingredient'] = new_ingr2
                    for j, pos in enumerate(step.ingredients[i]['positions']):
                        sub_positions.append((pos, step_num, i, j, new_ingr2))
                    break
    sub_positions = sorted(sub_positions, key=lambda x: x[0], reverse=True)
    for sub in sub_positions:
        pos = sub[0]
        step_num = sub[1]
        ingr_num = sub[2]
        pos_num = sub[3]
        ingr = sub[4]
        new_steps[step_num].tokens[pos[0]:pos[1]] = ingr.name.split(' ')
        new_steps[step_num].ingredients[ingr_num]['positions'][pos_num] = (pos[0], pos[0]+len(ingr.name.split(' ')))
    return new_steps

def print_steps(steps):
    i = 1
    for step in steps:
        tokens = copy.deepcopy(step.tokens)
        for ingr in step.ingredients:
            for pos in ingr['positions']:
                tokens[pos[0]] = '[' + tokens[pos[0]]
                tokens[pos[1]-1] = tokens[pos[1]-1] + ']'
        if step.action is not None:
            tokens[step.action_position[0]] = '<' + tokens[step.action_position[0]]
            tokens[step.action_position[1]-1] = tokens[step.action_position[1]-1] + '>'
        print('Step {}: {}'.format(i, ' '.join(tokens)))
        i += 1

