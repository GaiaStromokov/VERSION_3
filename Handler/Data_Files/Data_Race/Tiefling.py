import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Tiefling(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Vision.Dark.Sit("Race", 60)
        self.db.Prof.Lang.Sit("Race", ["Common", "Infernal"])
        self.Feature_List = [TIF_BAS_Hellish_Resistance]

class Tiefling_Asmodeus(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_ASM_Infernal_Legacy])

class Tiefling_Baalzebul(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_BAL_Legacy_of_Maladomini])

class Tiefling_Dispater(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_DIS_Legacy_of_Dis])

class Tiefling_Fierna(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_FIE_Legacy_of_Phlegethos])

class Tiefling_Glasya(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_GLA_Legacy_of_Malbolge])

class Tiefling_Levistus(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_LEV_Legacy_of_Stygia])

class Tiefling_Mammon(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_MAM_Legacy_of_Minauros])

class Tiefling_Mephistopheles(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_MEP_Legacy_of_Cania])

class Tiefling_Zariel(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_ZAR_Legacy_of_Avernus])

class TIF_BAS_Hellish_Resistance(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Resistance to Fire damage."]
        self.Set()

class TIF_Spell_Legacy(tFeature):
    Given = {}

    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Spell"
        self.Desc = ["Gain Magic"]
        self.Set()

        self.Spells = {}
        for spell, (req, uses) in self.Given.items():
            if req <= self.L:
                self.Spells[spell] = "Will" if uses == "Will" else [False] * uses

        self.Recharge = ["Long"]
        self.Update({"Spells": self.Spells, "Recharge": self.Recharge})

    def Refresh(self):
        past = (self.Race_features.get(self.Name, {}) or {}).get("Spells") or {}

        self.Spells = {}
        for spell, (req, uses) in self.Given.items():
            if req <= self.L:
                self.Spells[spell] = past.get(spell, "Will" if uses == "Will" else [False] * uses)
        self.Update({"Spells": self.Spells})

class TIF_ASM_Infernal_Legacy(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Hellish Rebuke": [3, 1], "Darkness": [5, 1]}
class TIF_BAL_Legacy_of_Maladomini(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Ray of Sickness": [3, 1], "Crown of Madness": [5, 1]}
class TIF_DIS_Legacy_of_Dis(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Disguise Self": [3, 1], "Detect Thoughts": [5, 1]}
class TIF_FIE_Legacy_of_Phlegethos(TIF_Spell_Legacy):
    Given = {"Friends": [1, "Will"], "Charm Person": [3, 1], "Suggestion": [5, 1]}
class TIF_GLA_Legacy_of_Malbolge(TIF_Spell_Legacy):
    Given = {"Minor Illusion": [1, "Will"], "Disguise Self": [3, 1], "Invisibility": [5, 1]}
class TIF_LEV_Legacy_of_Stygia(TIF_Spell_Legacy):
    Given = {"Ray of Frost": [1, "Will"], "Armor of Agathys": [3, 1], "Darkness": [5, 1]}
class TIF_MAM_Legacy_of_Minauros(TIF_Spell_Legacy):
    Given = {"Mage Hand": [1, "Will"], "Tenser's Floating Disk": [3, 1], "Arcane Lock": [5, 1]}
class TIF_MEP_Legacy_of_Cania(TIF_Spell_Legacy):
    Given = {"Mage Hand": [1, "Will"], "Burning Hands": [3, 1], "Flame Blade": [5, 1]}
class TIF_ZAR_Legacy_of_Avernus(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Searing Smite": [3, 1], "Branding Smite": [5, 1]}

Tiefling_Catalog = {
    "Base": Tiefling,
    "Asmodeus": Tiefling_Asmodeus,
    "Baalzebul": Tiefling_Baalzebul,
    "Dispater": Tiefling_Dispater,
    "Fierna": Tiefling_Fierna,
    "Glasya": Tiefling_Glasya,
    "Levistus": Tiefling_Levistus,
    "Mammon": Tiefling_Mammon,
    "Mephistopheles": Tiefling_Mephistopheles,
    "Zariel": Tiefling_Zariel
}