import re

from guru import Guru
from keywords.units import UNITS
from keywords.prep import PREPSTEPS

class Ingredient(object):
    def __init__(self, statement, guru = None):
        self.statement = statement
        self.guru = guru if guru != None else Guru()
        self.name = None
        self.baseType = None
        self.quantity = None
        self.quantity_modifier = None
        self.unit = None
        self.prepSteps = []
        self.role = None
        self.parse()

    def parse(self):
        workingStatement = self.statement

        # clean up the statement...
        workingStatement = workingStatement.replace(",", "")
        # etc...

        # PREP INSTRUCTIONS
        # TODO: move to Guru for pre-compiling
        rgx = "(?:"+"|".join(PREPSTEPS)+")"
        prepCheck = re.findall(rgx, workingStatement)
        if self.statement == "3 (28 ounce) cans whole peeled tomatoes, crushed": breakpoint()
        if prepCheck:
            # we're dealing with one-to-many here...
            for prepStep in prepCheck:
                workingStatement = workingStatement.replace(prepStep, "").replace("  ", " ").strip()
                self.prepSteps.append(prepStep.strip())

        # ROLE ASSESSMENT
        # TODO: make this smarter and derive role like "protein" or "starch"
        # FOR NOW: just look for "garnish with" or "for garnish"
        garnishCheck = re.search('(?:for)? ?(?:garnish) ?(?:with)?', workingStatement)
        if garnishCheck:
            workingStatement = workingStatement.replace(garnishCheck.group(), "").replace("  ", " ").strip()
            self.role = "garnish"

        # SUSS OUT THE QUANTITY
        quantityCheck = re.match("^\d*[ .]?\d*(?:\/?\d*)?", workingStatement)
        if quantityCheck:
            self.quantity = quantityCheck.group().strip()
            workingStatement = workingStatement[(len(self.quantity)):].strip()
        elif workingStatement.split(" ")[0].lower() == "a":
            # TODO: handle stuff like "a half" and "a quarter"
            self.quantity = "1"
            workingStatement = workingStatement[2:].strip()

        # IS THERE A QUANTITY MODIFIER?
        modifierCheck = re.search('(?:or)? ?(?:to taste)', workingStatement)
        if modifierCheck:
            self.quantity_modifier = modifierCheck.group().strip()
            workingStatement = workingStatement.replace(modifierCheck.group(), "").replace("  ", " ").strip()

        # GET THE UNIT
        # unigrams and bigrams (if applicable)
        chunks = workingStatement.split(" ")
        terms = [chunks[0].lower()]
        if len(chunks) > 2:
            terms.append(chunks[0].lower() + " " + chunks[1].lower())
        for term in terms:
            if term in UNITS:
                # TODO: explore handling periods in abbreviations -- possibly with regex?
                self.unit = term
                workingStatement = workingStatement.replace(term, "", 1).strip()
        if not self.unit:
            # look for leading parentheses/patterns like "(4 ounce)"
            # TODO: maybe build this out to be more flexible (and move to Guru for precompiling)
            specialUnit = re.match("^\(\d*[ .]?\d*(?:\/?\d*)? \w*\) ?(?:can|bottle|jar|package)?s?", workingStatement)
            if specialUnit and specialUnit.group():
                self.unit = specialUnit.group().replace("(","").replace(")","").strip()
                workingStatement = workingStatement[len(specialUnit.group()):].strip()
                if "of " in workingStatement and workingStatement.lower().index("of ") == 0:
                    workingStatement = workingStatment[3:]

        # GET THE BASE TYPE
        # ask the guru for help, so we're not constantly loading external data per ingredient
        # by now our workingStatement *should* just be the ingredient itself
        self.baseType = self.guru.get_ingredient_base_type(workingStatement)

        # and save the name...
        self.name = workingStatement

    def express_components(self):
        # debugging helper
        print("-----")
        print("STATEMENT: " + self.statement)
        print("NAME: " + str(self.name))
        print("BASETYPE: " + str(self.baseType))
        print("QUANTITY: " + str(self.quantity))
        print("UNIT: " + str(self.unit))
        print("PREP STEPS: " + str(self.prepSteps))
        print("ROLE: " + str(self.role))
