import q, re, math
from Handler.Utils.funcs import *
from Handler.bClass import tClass, tFeature

class Wizard(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.HD.Sit("HD", 6)
        self.db.Prof.Weapon.Sit("Class", ["Dagger", "Dart", "Sling", "Quarterstaff", "Light_Crossbow"])
        self.Refresh_Skill(["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"], 2)
        self.Feature_List = [WIZ_BAS_Spellcasting, WIZ_BAS_Arcane_Recovery, WIZ_BAS_Spell_Mastery, WIZ_BAS_Signature_Spell]

class Wizard_Abjuration(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = [WIZ_ABJ_Abjuration_Savant, WIZ_ABJ_Arcane_Ward, WIZ_ABJ_Projected_Ward, WIZ_ABJ_Improved_Abjuration, WIZ_ABJ_Spell_Resistance]

class Wizard_Conjuration(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = [WIZ_CNJ_Conjuration_Savant, WIZ_CNJ_Minor_Conjuration, WIZ_CNJ_Benign_Transportation, WIZ_CNJ_Focused_Conjuration, WIZ_CNJ_Durable_Summons, ]

class WIZ_BAS_Spellcasting(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["You gots them magic hands."]
        self.Set()

class WIZ_BAS_Arcane_Recovery(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Use"
        recover_num = math.ceil(self.L / 2)
        self.Desc = [f"(Short Rest) Recover spell slots with combined level of {recover_num}. Recover only up to 5th level spells"]
        self.Recharge = ["Long"]
        self.max_uses = 1
        self.Use = [False]*self.max_uses

        self.Set()
        self.Update({"Use": self.Use, "Recharge": self.Recharge})
    
    def Refresh(self):
        past_use = self.get_past("Use")
        if past_use is None: past_use = []
        self.Use = (past_use + [False]*self.max_uses)[:self.max_uses]

class WIZ_BAS_Spell_Mastery(tFeature):
    def Run(self):
        if not self.allowed(18): return False

        self.Tag = "Spell_Mastery" 
        self.Desc = ["Cast chosen 1st and 2nd level spells at will."]
        self.Set()

        self.max_choices = 2
        self.Select = [""] * self.max_choices

        Spell_List_1 = [""] + q.fTome(Level=1, Caster="Wizard")
        Spell_List_2 = [""] + q.fTome(Level=2, Caster="Wizard")
        self.Options = [Spell_List_1, Spell_List_2]

        self.Update({"Options": self.Options, "Select": self.Select})

    def Refresh(self):
        past_sel = self.get_past("Select")
        if past_sel is None: past_sel = []
        self.Select = (past_sel + [""] * self.max_choices)[:self.max_choices]
        self.Update({"Select": self.Select})

        
class WIZ_BAS_Signature_Spell(tFeature):
    def Run(self):
        if not self.allowed(20): return False
        
        self.Tag = "Signature_Spell"
        self.Desc = ["Two 3rd level spells, always prepared, cast once each without slot."]
        self.Set()

        self.max_choices = 2
        self.Select = [""] * self.max_choices

        self.max_uses = 2
        self.Use = [False]*self.max_uses
        Spell_List = [""] + q.fTome(Level = 3, Caster = "Wizard")
        self.Options = [Spell_List, Spell_List]
        self.Recharge = ["Short"]
        self.Update({
            "Options": self.Options,
            "Select": self.Select,
            "Use": self.Use,
            "Recharge": self.Recharge
        })
    
    def Refresh(self):
        past_sel = self.get_past("Select")
        if past_sel is None: past_sel = []
        self.Select = (past_sel + [""] * self.max_choices)[:self.max_choices]

        past_use = self.get_past("Use")
        if past_use is None: past_use = []
        self.Use = (past_use + [False]*self.max_uses)[:self.max_uses]

        self.Update({
            "Select": self.Select,
            "Use": self.Use
        })


class WIZ_ABJ_Abjuration_Savant(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Passive"
        self.Desc = ["Cost/time to copy Abjuration spells halved."]
        self.Set()
    
    def Refresh(self):
        pass

class WIZ_ABJ_Arcane_Ward(tFeature):
    def Run(self):
        if not self.allowed(2): return False

        int_mod = self.Atr.INT.Mod
        max_hp = (self.L * 2) + int_mod
        
        self.Tag = "Familiar"
        self.Desc = [f"Ward has HP equal to {max_hp}"]
        self.Set()
        
        self.HP = {"Max": max_hp, "Current": max_hp}
        self.max_uses = 1
        self.Use = [False]*self.max_uses
        self.Recharge = ["Long"]
        self.Update({"HP": self.HP, "Use": self.Use, "Recharge": self.Recharge})
        
    def Refresh(self):
        past_use = self.get_past("Use")
        if past_use is None: past_use = []
        self.Use = (past_use + [False]*self.max_uses)[:self.max_uses]
        
        
        current_hp = self.Class_features[self.Name].get("HP")["Current"]
        
        self.HP["Current"] = current_hp
        self.Update({"HP": self.HP, "Use": self.Use})
        
            
    
class WIZ_ABJ_Projected_Ward(tFeature):
    def Run(self):
        if not self.allowed(6): return False
        self.Tag = "Passive"
        self.Desc = ["(Reaction) Arcane Ward absorbs damage for creature within 30ft."]
        self.Set()
        
    def Refresh(self):
            pass

class WIZ_ABJ_Improved_Abjuration(tFeature):
    def Run(self):
        if not self.allowed(10): return False
        self.Tag = "Passive"
        self.Desc = [f"Add {self.PB} to Abjuration spell checks."]
        self.Set()
        
    def Refresh(self):
        pass

class WIZ_ABJ_Spell_Resistance(tFeature):
    def Run(self):
        if not self.allowed(14): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on spell saves, resistance to spell damage."]
        self.Set()
        
    def Refresh(self):
            pass

class WIZ_CNJ_Conjuration_Savant(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Passive"
        self.Desc = ["Cost/time to copy Conjuration spells halved."]
        self.Set()
        
    def Refresh(self):
            pass

class WIZ_CNJ_Minor_Conjuration(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Passive"
        self.Desc = ["(Action) Conjure non-magical item (3ft, 10lb)."]
        self.Set()
    
    def Refresh(self):
            pass

class WIZ_CNJ_Benign_Transportation(tFeature):
    def Run(self):
        if not self.allowed(6): return False
        self.Tag = "Use"
        self.Desc = ["(Action) Teleport 30ft or swap places. Refreshes on casting 1st+ Conjuration spell."]
        self.Set()
        self.max_uses = 1
        self.Use = [False]*self.max_uses
        self.Recharge = ["Long"]
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        past_use = self.get_past("Use")
        if past_use is None: past_use = []
        self.Use = (past_use + [False]*self.max_uses)[:self.max_uses]
        
        self.Update({"Use": self.Use})

    
class WIZ_CNJ_Focused_Conjuration(tFeature):
    def Run(self):
        if not self.allowed(10): return False
        self.Tag = "Passive"
        self.Desc = ["Damage does not break concentration on Conjuration spells."]
        self.set()

    def Refresh(self):
            pass


class WIZ_CNJ_Durable_Summons(tFeature):

    def Run(self):
        if not self.allowed(14): return False
        self.Tag = "Passive"
        self.Desc = ["Summoned creatures have +30 temp HP."]
        self.set()

    def Refresh(self):
        pass

Wizard_Catalog = {
    "Base": Wizard,
    "Abjuration": Wizard_Abjuration,
    "Conjuration": Wizard_Conjuration
}