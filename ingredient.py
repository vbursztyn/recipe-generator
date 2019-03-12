from copy import copy, deepcopy
import re

from keywords.units import UNITS
from keywords.prep import PREPSTEPS

class Ingredient(object):
    def __init__(self, statement, guru):
        self.statement = statement
        self.altered = False # changed during recipe/ingredient transformation
        self.addedByTransform = False # changed during recipe/ingredient transformation
        self.guru = guru  # if guru != None else Guru()
        self.name = None
        self.baseType = None
        self.quantity = None
        self.quantityModifier = None
        self.knownHealthyModifiers = ["lean", "extra-lean", "extra lean", "lowfat", "low-fat", "low fat", "low-calorie", "low calorie", "diet"]
        self.healthyModifier = None
        self.knownSizeModifiers = ["large", "medium", "med", "small", "good-sized", "whole", "half", "halves"]
        self.sizeModifier = None
        self.knownFlavorModifiers = ["sweet", "hot", "tangy", "smoky", "spiced"]
        self.flavorModifier = None
        self.knownTypeModifiers = ["dry", "dried", "ground", "crushed", "flaked", "frozen", "fresh"]
        self.typeModifier = None
        self.convertibleQuantity = False
        self.unit = None
        self.prepSteps = []
        self.role = None
        self.parse()
        self.assignRole()

    def __repr__(self):
        output = "-----"
        output += "\nSTATEMENT: " + self.statement
        output += "\nNAME: " + str(self.name)
        output += "\nBASETYPE: " + str(self.baseType)
        output += "\nQUANTITY: " + str(self.quantity)
        output += "\nQUANTITY MODIFIER: " + str(self.quantityModifier)
        output += "\nHEALTHY MODIFIER: " + str(self.healthyModifier)
        output += "\nSIZE MODIFIER: " + str(self.sizeModifier)
        output += "\nTYPE MODIFIER: " + str(self.typeModifier)
        output += "\nFLAVOR MODIFIER: " + str(self.flavorModifier)
        output += "\nUNIT: " + str(self.unit)
        output += "\nPREP STEPS: " + str(self.prepSteps)
        output += "\nROLE: " + str(self.role)
        output += "\n"
        return output

    def __str__(self):
        # SORTA NLG IT UP!
        output = ""
        if self.quantity: output += str(self.quantity)
        if self.unit: output += " " + self.unit
        if self.sizeModifier: output += " " + self.sizeModifier
        if self.flavorModifier: output += " " + self.flavorModifier
        if self.healthyModifier: output += " " + self.healthyModifier
        if self.typeModifier: output += " " + self.typeModifier
        prepSteps = copy(self.prepSteps)
        if "ground" in prepSteps:
            output += " ground"
            prepSteps.remove("ground")
        if self.name: output += " " + self.name
        if prepSteps and len(prepSteps) == 1:
            output += ", " + prepSteps[0]
        elif prepSteps and len(prepSteps) > 1:
            for i, step in enumerate(prepSteps):
                if (i + 1) == len(prepSteps):
                    output += " and "
                output += " " + step
        if self.quantityModifier:
            output += " (" + self.quantityModifier + ")"
        return output

    def __mul__(self, x):
        if isinstance(x, (int, float)) and self.convertibleQuantity:
            newIngredient = deepcopy(self)
            newIngredient.quantity = self.quantity * x
            return newIngredient
        return self

    __rmul__ = __mul__

    def parse(self):
        workingStatement = self.statement

        # clean up the statement...
        workingStatement = workingStatement.replace(",", "")
        # etc...

        # PREP INSTRUCTIONS
        # TODO: move to Guru for pre-compiling
        rgx = "(?:"+"|".join(PREPSTEPS)+")"
        prepCheck = re.findall(rgx, workingStatement)
        if prepCheck:
            # we"re dealing with one-to-many here...
            for i, prepStep in enumerate(prepCheck):
                workingStatement = workingStatement.replace(prepStep, "")
            if len(prepCheck) > 1 and i == len(prepCheck)-1:
                # check for orphaned ands/ors
                # cheating a bit by looking for double spaces...if this works, it avoid
                # regex permutations...
                hunter = "  (?:and|or) ?"
                matched = re.search(hunter, workingStatement)
                if matched:
                    workingStatement = re.sub(hunter, "", workingStatement)
            else:
                workingStatement = workingStatement.replace("  ", " ").strip()
                self.prepSteps.append(prepStep.strip())

        # ROLE ASSESSMENT
        # TODO: make this smarter and derive role like "protein" or "starch"
        # FOR NOW: just look for "garnish with" or "for garnish"
        garnishCheck = re.search("(?:for)? ?(?:garnish) ?(?:with)?", workingStatement)
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

        # now make quantity a proper number/decimal
        try:
            self.quantity = float(self.quantity)
            self.convertibleQuantity = True
        except:
            self.convertibleQuantity = False

        if not self.convertibleQuantity:
            # keep trying!
            try:
                if len(self.quantity.split("/")) > 1:
                    # it's a fraction...split it apart
                    # first...is there a whole number, too?
                    spaceChunks = self.quantity.split(" ")
                    if len(spaceChunks) == 1:
                        # just a fraction
                        fractChunks = self.quantity.split("/")
                        self.quantity = int(fractChunks[0]) / int(fractChunks[1])
                        self.convertibleQuantity = True
                    elif len(spaceChunks) == 2:
                        firstPart = int(spaceChunks[0])
                        fractChunks = self.quantity.split("/")
                        secondPart = int(fractChunks[0]) / int(fractChunks[1])
                        self.quantity = firstPart + secondPart
                        self.convertibleQuantity = True
            except:
                # we still have a quantity
                # but we can't change it downstream
                pass

        # IS THERE A QUANTITY MODIFIER?
        modifierSnippets = ["or to taste","or more to taste","or more as needed to taste","or as needed to taste","as needed to taste","to taste","or more as needed","or more","or as needed","as needed"]
        modifierCheck = re.search("(?:"+"|".join(modifierSnippets)+")", workingStatement)
        if modifierCheck:
            self.quantityModifier = modifierCheck.group().strip()
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
            specialUnit = re.match("^\(\d*[ .]?\d*(?:\/?\d*)?[\s\S]*\) ?(?:can|bottle|jar|package|square|jigger|link)?s?", workingStatement)
            if specialUnit and specialUnit.group():
                self.unit = specialUnit.group().replace("(","").replace(")","").strip()
                workingStatement = workingStatement[len(specialUnit.group()):].strip()
                if "of " in workingStatement and workingStatement.lower().index("of ") == 0:
                    workingStatement = workingStatement[3:]

        # SOME FINAL CLEANUP
        workingStatement = workingStatement.replace(" -", "").strip()

        # is there a healthy, size or flavor modifier in here?
        for hm in self.knownHealthyModifiers:
            if hm in workingStatement:
                self.healthyModifier = hm
                workingStatement = workingStatement.replace(hm, "").replace("  ", " ").strip()

        # is there a size modifier on here?
        for sm in self.knownSizeModifiers:
            if sm in workingStatement:
                self.sizeModifier = sm
                workingStatement = workingStatement.replace(sm, "").replace("  ", " ").strip()

        # is there a flavor modifier on here?
        for fm in self.knownFlavorModifiers:
            if fm in workingStatement:
                self.flavorModifier = fm
                workingStatement = workingStatement.replace(fm, "").replace("  ", " ").strip()

        # is there a type modifier on here?
        for tm in self.knownTypeModifiers:
            if tm in workingStatement:
                self.typeModifier = tm
                workingStatement = workingStatement.replace(tm, "").replace("  ", " ").strip()

        # if there's a hanging "bulk" in there, it's pretty likely to be implied by this point...
        if workingStatement.find("bulk") == 0:
            workingStatement = workingStatement[4:].strip()

        # GET THE BASE TYPE
        # ask the guru for help, so we"re not constantly loading external data per ingredient
        # by now our workingStatement *should* just be the ingredient itself
        self.baseType = self.guru.getIngredientBaseType(workingStatement)

        #CLEAN UP
        #anything that's contained in a parantheses is most likely to specific and can interfere with parsing
        # so we remove it

        def remove_parantheses(s : str):
            left_par_index = s.find("(")
            right_par_index = s.find(")")
            if left_par_index == -1 or right_par_index == -1:
                return s
            else:
                if left_par_index > 0 and s[left_par_index-1] == ' ':
                    return remove_parantheses(s[:left_par_index-1] + s[right_par_index+1:])
                else:
                    return remove_parantheses(s[:left_par_index] + s[right_par_index+1:])

        workingStatement = remove_parantheses(workingStatement)

        # same for anything following a " - "
        def remove_after_dash(s : str):
            if " - " in s:
                s = s[0:s.find(" - ")]
            return s

        workingStatement = remove_after_dash(workingStatement)

        # and save the name...
        self.name = workingStatement

    def assignRole(self):
        # check if this was assigned during parsing
        if self.role == "garnish": return True
        # if not, leverage the Guru to assign it
        pass
