import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Harengon(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Skill.Perception.Sit("Race", 0, True)
        self.db.Prof.Lang.Sit("Race", ["Common"])
        self.Feature_List = [HRG_BAS_Hare_Trigger, HRG_BAS_Lucky_Footwork, HRG_BAS_Rabbit_Hop]

class HRG_BAS_Hare_Trigger(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"Add {self.PB} to Initiative."]
        self.Set()

class HRG_BAS_Lucky_Footwork(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"(Reaction) On failed DEX save, add {self.PB}."]
        self.Set()

class HRG_BAS_Rabbit_Hop(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Use"
        self.Desc = [f"(Bonus) Jump {self.PB * 5} ft, no Opportunity Attacks."]
        self.Set()

        self.max_uses = self.PB
        self.Use = [False] * self.max_uses
        self.Recharge = ["Long"]
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        self.max_uses = self.PB
        past_use = self.get_past("Use") or []
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

Harengon_Catalog = {
    "Base": Harengon
}