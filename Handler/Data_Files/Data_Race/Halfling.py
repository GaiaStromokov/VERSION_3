import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Halfling(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 25)
        self.db.Prof.Lang.Sit("Race", ["Common", "Halfling"])
        self.Feature_List = [HLF_BAS_Lucky, HLF_BAS_Brave, HLF_BAS_Halfling_Nimbleness]

class Halfling_Lightfoot(Halfling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([HLF_LIG_Naturally_Stealthy])

class Halfling_Stout(Halfling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([HLF_STO_Stout_Resilience])

class HLF_BAS_Lucky(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Reroll 1s on a roll. Must use new roll."]
        self.Set()

class HLF_BAS_Brave(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on saves vs Frightened."]
        self.Set()

class HLF_BAS_Halfling_Nimbleness(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Move through space of creatures larger than you."]
        self.Set()

class HLF_LIG_Naturally_Stealthy(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Hide when obscured by creature one size larger."]
        self.Set()

class HLF_STO_Stout_Resilience(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on Poison saves, Resistance to Poison damage."]
        self.Set()

Halfling_Catalog = {
    "Base": Halfling,
    "Lightfoot": Halfling_Lightfoot,
    "Stout": Halfling_Stout
}