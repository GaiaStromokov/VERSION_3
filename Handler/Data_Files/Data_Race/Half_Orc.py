import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Half_Orc(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Vision.Dark.Sit("Race", 60)
        self.db.Skill.Intimidation.Sit("Race", 0, True)
        self.db.Prof.Lang.Sit("Race", ["Common", "Orc"])
        self.Feature_List = [HOR_BAS_Relentless_Endurance, HOR_BAS_Savage_Attacks]

class HOR_BAS_Relentless_Endurance(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Use"
        self.Desc = ["Drop to 1HP instead of 0HP once per Long Rest."]
        self.Set()

        self.max_uses = 1
        self.Use = [False] * self.max_uses
        self.Recharge = ["Long"]
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        past_use = self.get_past("Use") or []
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class HOR_BAS_Savage_Attacks(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Crit with melee weapon adds one extra damage die."]
        self.Set()

Half_Orc_Catalog = {
    "Base": Half_Orc
}   