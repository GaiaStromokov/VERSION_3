import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Dwarf(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 25)
        self.db.Vision.Dark.Sit("Race", 60)
        self.db.Prof.Lang.Sit("Race", ["Common", "Dwarvish"])
        self.db.Prof.Weapon.Sit("Race", ["Battleaxe", "Handaxe", "Light_Hammer", "Warhammer"])
        self.Feature_List = [DWF_BAS_Dwarven_Resilience, DWF_BAS_Stonecunning]

class Dwarf_Hill(Dwarf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([DWF_HIL_Dwarven_Toughness])

class Dwarf_Mountain(Dwarf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Prof.Armor.Sit("Race", ["Light", "Medium"])
        self.Feature_List.extend([])

class DWF_BAS_Dwarven_Resilience(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on Poison saves, Resistance to Poison damage."]
        self.Set()

class DWF_BAS_Stonecunning(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"Add {self.PB} to History checks on stonework."]
        self.Set()

class DWF_HIL_Dwarven_Toughness(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "HP"
        self.Desc = [f"HP Max increases by {self.L}."]
        self.Set()
        self.Update({"HP": "LEVEL"})

Dwarf_Catalog = {
    "Base": Dwarf,
    "Hill": Dwarf_Hill,
    "Mountain": Dwarf_Mountain
}