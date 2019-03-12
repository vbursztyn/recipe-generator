import nltk
from keywords.cooking_verbs import COOKING_VERBS
from keywords.units import UNITS
from keywords.tools import COOKING_TOOLS
import copy
import re


def intervals_overlap(interval1, interval2):
    """Assumes each interval is already sorted. This function also assumes
    half-open intervals, so if interval1[1] == interval2[0] that does NOT count
    as overlapping."""
    if interval1[0] <= interval2[0]:
        return interval2[0] < interval1[1]
    return interval1[0] < interval2[1]

def unitnumstr2float(unitnumstr):
    pieces = unitnumstr.split(' ')
    total = 0
    for piece in pieces:
        if re.match(r'^\d+([.]\d+)?$', piece):
            total += float(piece)
        elif re.match(r'^\d+/\d+$', piece):
            subpieces = piece.partition('/')
            total += float(subpieces[0]) / float(subpieces[2])
        else:
            return float('NaN')
    return total

def expand_str_placeholders(string, placeholders_dict, max_depth=None):
    if max_depth == 0:
        return string

    tokens = string.split(' ')
    for i in range(len(tokens)):
        if tokens[i] in placeholders_dict:
            tokens[i] = expand_str_placeholders(str(placeholders_dict[tokens[i]]), placeholders_dict, max_depth=(max_depth-1 if max_depth else None))

    return ' '.join(tokens)

def print_steps(steps):
    i = 1
    for step in steps:
        tokens = step._processed_text.split(' ')
        for j in range(len(tokens)):
            match = re.match(r'^__([^_]+)_\d+__$', tokens[j])
            if match:
                fullstr = expand_str_placeholders(tokens[j], step.placeholders)
                if match.group(1) == 'ingredient':
                    fullstr = '[' + fullstr + ']'
                elif match.group(1) == 'cookverb':
                    fullstr = '<' + fullstr + '>'
                tokens[j] = fullstr
        print('Step {}: {}'.format(i, ' '.join(tokens)))
        i += 1

def make_step(action, ingredients, until=None, fortime=None):
    step = RecipeStep()
    action_placid = step.new_placeholder_id(base_name='cookverb')
    step.placeholders[action_placid] = Placeholder(action)
    ingredient_exs = []
    for ingr in ingredients:
        ingr_ex = {
            'ingredient': ingr,
            'placeholder': step.new_placeholder_id(base_name='ingredient'),
        }
        ingredient_exs.append(ingr_ex)
        step.placeholders[ingr_ex['placeholder']] = Placeholder(ingr.name, meta=ingr_ex)

    ingrlist = ' , '.join([x['placeholder'] for x in ingredient_exs[:-1]])
    if len(ingredient_exs) > 1:
        ingrlist += ' and '
    ingrlist += ingredient_exs[-1]['placeholder']

    step._processed_text = action_placid + ' ' + ingrlist

    if until:
        # Assuming "until" is a string representing a stop condition
        until_placid = step.new_placeholder_id(base_name='until')
        step.placeholders[until_placid] = Placeholder('until ' + until)
        step._processed_text += ' ' + until_placid

    if fortime:
        # Assuming "fortime" is a string representing an amount of time
        fortime_placid = step.new_placeholder_id(base_name='fortime')
        step.placeholders[fortime_placid] = Placeholder('for ' + fortime)
        step._processed_text += ' ' + fortime_placid

    step._processed_text += ' ' + '.'
    return step

def modify_steps(steps, ingr_subs):
    for step in steps:
        step.sub_ingredients(ingr_subs)

def add_ingredents_alongside(steps, reference_ingr, new_ingrs):
    i = 0
    while i < len(steps):
        if any(ingr['placeholder'] in steps[i]._processed_text and ingr['ingredient'].statement == reference_ingr.statement for ingr in steps[i].ingredients):
            new_step = RecipeStep()
            action_placid = new_step.new_placeholder_id(base_name='cookverb')
            new_step.placeholders[action_placid] = Placeholder('add')
            ingredient_exs = []
            for ingr in new_ingrs:
                ingr_ex = {
                    'ingredient': ingr,
                    'placeholder': new_step.new_placeholder_id(base_name='ingredient'),
                }
                ingredient_exs.append(ingr_ex)
                new_step.placeholders[ingr_ex['placeholder']] = Placeholder(ingr.name, meta=ingr_ex)

            ingrlist = ' , '.join([x['placeholder'] for x in ingredient_exs[:-1]])
            if len(ingredient_exs) > 1:
                ingrlist += ' and '
            ingrlist += ingredient_exs[-1]['placeholder']

            new_step._processed_text = 'Now would be a good time to {} the {}'.format(action_placid, ingrlist)
            steps.insert(i+1, new_step)
            i += 1
        i += 1


class Placeholder:
    def __init__(self, string, meta=None):
        self.string = string
        self.meta = meta

    def __str__(self):
        return self.string


class RecipeStep:
    def __init__(self):
        self.raw_step = ""
        self.raw_tokens = []
        self.ingredients = []

        self._placeholder_counter = 0
        self.placeholders = dict()

        self._processed_text = ''

    def new_placeholder_id(self, base_name='placeholder'):
        self._placeholder_counter += 1
        return ('__' + base_name + '_' + str(self._placeholder_counter) + '__')

    def _sub_ingredient(self, old_ingr_ex, new_ingr):
        new_ingr_ex = {
            'ingredient': new_ingr,
            'placeholder': self.new_placeholder_id(base_name='ingredient'),
        }
        new_plac = Placeholder(new_ingr.name, meta=new_ingr_ex)
        self.placeholders[new_ingr_ex['placeholder']] = new_plac
        tokens = self._processed_text.split(' ')
        for i, tok in enumerate(tokens):
            if tok == old_ingr_ex['placeholder']:
                tokens[i] = new_ingr_ex['placeholder']
                if 0 < i and re.match(r'^__unit_\d+__$', tokens[i-1]) and tokens[i-1] in self.placeholders:
                    self.placeholders[tokens[i-1]] = new_ingr.get_pretty_quantity_str() + ' ' + new_ingr.unit
                elif 1 < i and re.match(r'^__unit_\d+__$', tokens[i-2]) and tokens[i-2] in self.placeholders:
                    self.placeholders[tokens[i-2]] = new_ingr.get_pretty_quantity_str() + ' ' + new_ingr.unit
        self._processed_text = ' '.join(tokens)

    def sub_ingredients(self, ingr_subs):
        """Note: ingr_subs should be a dict like [old_ingr1_statement: new_ingr1,
        ...]. This method substitutes by checking if an old_ingr_statement
        matches that of an existing ingredient in a step."""

        for i in range(len(self.ingredients)):
            ingr1 = self.ingredients[i]
            if ingr1['ingredient'].statement in ingr_subs:
                self._sub_ingredient(ingr1, ingr_subs[ingr1['ingredient'].statement])

    def get_needed_tools(self):
        tools = []
        for plac in self.placeholders.keys():
            if re.match(r'^__cooktool_\d+__$', plac):
                tools.append(expand_str_placeholders(str(self.placeholders[plac]), self.placeholders))
        return tools


class RecipeDirectionsParser:
    def __init__(self, raw_directions, ingredients):
        self.raw_directions = raw_directions
        self.ingredients = ingredients
        self.steps = []

        self._HEATLEVEL_REGEX = r'\b(over|on) (low|medium|high) heat'
        self._COOKING_VERB_REGEX = r'\b(' + r'|'.join([re.escape(verb) for verb in COOKING_VERBS]) + r')\b'
        self._UNIT_NUMBER_REGEX = r'\b((\d+ )?\d+([/.]\d+)?)\b'
        self._UNIT_NAME_REGEX = r'\b(' + r'|'.join([re.escape(unit) for unit in UNITS]) + r')\b'
        self._UNIT_REGEX = r'\b__unitnumber_\d+__ ' + self._UNIT_NAME_REGEX
        self._TEMPERATURE_REGEX = r'\b__unitnumber_\d+__ degrees [fc]\b'
        self._TIME_REGEX = r'\b(__unitnumber_\d+__ to )?__unitnumber_\d+__ (minutes?|hours?)\b'
        self._FOR_TIME_REGEX = r'\bfor (\w+ )?__time_\d+__'
        self._UNTIL_REGEX = r'\buntil \w+( \w+)* [,.]'
        self._COOKING_TOOL_REGEX = r'\b(' + r'|'.join([re.escape(tool) for tool in COOKING_TOOLS]) + r')\b'
        self._COOKING_TOOL_INTEXT_REGEX = r'(with|using|in) an? (?P<to_sub>((small|medium|large) )?' + self._COOKING_TOOL_REGEX + r')'

        self.raw_steps = self._split_steps(raw_directions)
        for step in self.raw_steps:
            self.steps.append(self.direction_to_recipe_step(step))

    def get_steps(self):
        return self.steps

    def _disambiguate_overlapping_ingredients(self, step, direction_tokens, ingr_extras):
        # When a word could correspond to any of multiple ingredients,
        # disambiguate by checking the length of the match and whether the
        # amount is specified inline

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
                            elif 0 < interval1[0] and re.match(r'^__unit_\d+__$', direction_tokens[interval1[0]-1]):
                                # In theory we should check the unit in
                                # addition to the value (e.g., cups are bigger
                                # than tablespoons). In practice, using just
                                # the number seems to work pretty well and is
                                # much easier to implement
                                expanded_plac = str(step.placeholders[direction_tokens[interval1[0]-1]])
                                number_str = re.search(r'^__unitnumber_\d+__\b', expanded_plac)
                                if number_str:
                                    number = unitnumstr2float(str(step.placeholders[expanded_plac[number_str.start():number_str.end()]]))
                                    ingr1_quant = ingr1['ingredient'].quantity if ingr1['ingredient'].convertibleQuantity else float('nan')
                                    ingr2_quant = ingr2['ingredient'].quantity if ingr2['ingredient'].convertibleQuantity else float('nan')
                                    if abs(number - ingr1_quant) >= abs(number - ingr2_quant):
                                        ingr1['positions'].remove(interval1)
                                        return
                                # When all else fails
                                ingr2['positions'].remove(interval2)
                            else:
                                # When all else fails
                                ingr2['positions'].remove(interval2)

    def _strsub_regex2placeholders(self, step, sub_regex, base_name='regex'):
        """This function modifies step._processed_text"""

        new_str = ''
        last_ind = 0
        for match in re.finditer(sub_regex, step._processed_text):
            start, end = match.start(), match.end()
            if 'to_sub' in match.groupdict():
                start, end = match.start('to_sub'), match.end('to_sub')
            new_str += step._processed_text[last_ind:start]
            newplac = step.new_placeholder_id(base_name=base_name)
            step.placeholders[newplac] = Placeholder(step._processed_text[start:end])
            new_str += newplac
            last_ind = end
        new_str += step._processed_text[last_ind:]
        step._processed_text = new_str

    def _parse_step_ingredients(self, step):
        direction_tokens = step._processed_text.split(' ')
        ingr_extras = []
        for ingr in self.ingredients:
            namelist = nltk.word_tokenize(ingr.name.lower())
            if 'and' in namelist:
                namelist.remove('and')
            ingr_extras.append({
                'ingredient': ingr,
                'placeholder': step.new_placeholder_id(base_name='ingredient'),
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


        self._disambiguate_overlapping_ingredients(step, direction_tokens, ingr_extras)

        sub_positions = []
        for ingr in ingr_extras:
            for pos in ingr['positions']:
                sub_positions.append((pos, ingr))
            del ingr['positions']
        sub_positions = sorted(sub_positions, key=lambda x: x[0], reverse=True)
        for sub in sub_positions:
            pos = sub[0]
            ingr = sub[1]
            step.placeholders[ingr['placeholder']] = Placeholder(' '.join(direction_tokens[pos[0]:pos[1]]), meta=ingr)
            direction_tokens[pos[0]:pos[1]] = [ingr['placeholder']]

        step._processed_text = ' '.join(direction_tokens)

        step.ingredients = ingr_extras

    def direction_to_recipe_step(self, direction):
        direction = direction.lower()
        step = RecipeStep()
        step.raw_step = direction
        step.raw_tokens = nltk.word_tokenize(direction.lower())

        step._processed_text = ' '.join(step.raw_tokens)
        self._strsub_regex2placeholders(step, self._HEATLEVEL_REGEX, base_name='heatlevel')
        self._strsub_regex2placeholders(step, self._COOKING_VERB_REGEX, base_name='cookverb')
        self._strsub_regex2placeholders(step, self._UNIT_NUMBER_REGEX, base_name='unitnumber')
        self._strsub_regex2placeholders(step, self._UNIT_REGEX, base_name='unit')
        self._strsub_regex2placeholders(step, self._TEMPERATURE_REGEX, base_name='temperature')
        self._strsub_regex2placeholders(step, self._TIME_REGEX, base_name='time')
        self._strsub_regex2placeholders(step, self._FOR_TIME_REGEX, base_name='fortime')
        self._parse_step_ingredients(step)
        self._strsub_regex2placeholders(step, self._UNTIL_REGEX, base_name='until')
        self._strsub_regex2placeholders(step, self._COOKING_TOOL_INTEXT_REGEX, base_name='cooktool')
        return step

    def _split_steps(self, directions):
        if isinstance(directions, list):
            all_steps = []
            for substep in directions:
                all_steps.extend(self._split_steps(substep))
            return all_steps
        return nltk.sent_tokenize(directions)

