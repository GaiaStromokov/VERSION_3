import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Elf(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Vision.Dark.Sit("Race", 60)
        
        self.db.Skill.Perception.Sit("Race", 0, True)
        self.db.Prof.Lang.Sit("Race", ["Common", "Elvish"])
        self.Feature_List = [ELF_BAS_Fey_Ancestry, ELF_BAS_Trance]

class Elf_High(Elf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Prof.Weapon.Sit("Race", ["Longsword", "Shortsword", "Shortbow", "Longbow"])
        # self.db.Prof.Lang.Sit("Race", ["Extra"])
        self.Feature_List.extend([ELF_HIG_Cantrip])

class Elf_Wood(Elf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 35)
        self.db.Prof.Weapon.Sit("Race", ["Longsword", "Shortsword", "Shortbow", "Longbow"])
        self.Feature_List.extend([ELF_WOD_Mask_of_the_Wild])

class Elf_Drow(Elf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Vision.Dark.Sit("Race", 120)
        self.db.Prof.Weapon.Sit("Race", ["Rapier", "Shortsword", "Hand_Crossbow"])
        self.Feature_List.extend([ELF_DRK_Sunlight_Sensitivity, ELF_DRK_Drow_Magic])

class Elf_Shadar_Kai(Elf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([ELF_SHA_Necrotic_Resistance, ELF_SHA_Blessing_of_the_Raven_Queen])
        
class ELF_BAS_Fey_Ancestry(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on saves vs being charmed; magic can't put you to sleep."]
        self.Set()

class ELF_BAS_Trance(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Meditate 4 hours instead of sleeping; gain benefits of a long rest."]
        self.Set()

class ELF_HIG_Cantrip(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "High_Cantrip"
        self.Desc = ["Gain a Cantrip"]
        self.Set()

        self.max_choices = 1
        self.Select = [""]*self.max_choices
        self.Options = [""] + q.fTome(Level=0, Caster="Wizard")
        self.Update({"Select": self.Select, "Options": self.Options})

    def Refresh(self):
        past_sel = self.get_past("Select") or []
        self.Select = (past_sel + [""] * self.max_choices)[:self.max_choices]
        self.Update({"Select": self.Select})

class ELF_WOD_Mask_of_the_Wild(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Can attempt to hide when lightly obscured by natural phenomena."]
        self.Set()

class ELF_DRK_Sunlight_Sensitivity(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Disadvantage on attacks and Perception checks relying on sight in sunlight."]
        self.Set()

class ELF_DRK_Drow_Magic(tFeature):
    Given = {
        "Dancing Lights": [1, "Will"],
        "Faerie Fire": [3, 1],
        "Darkness": [5, 1],
    }

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

class ELF_SHA_Necrotic_Resistance(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Resistance to Necrotic damage."]
        self.Set()

class ELF_SHA_Blessing_of_the_Raven_Queen(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Use"
        
        if self.L >= 3:
            self.Desc = ["(Bonus) Teleport 30ft. Gain Resistance to all dmg until start of next turn."]
        else:
            self.Desc = ["(Bonus) Teleport 30ft."]
            
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

Elf_Catalog = {
    "Base": Elf,
    "Drow": Elf_Drow,
    "High": Elf_High,
    "Shadar_Kai": Elf_Shadar_Kai,
    "Wood": Elf_Wood
}