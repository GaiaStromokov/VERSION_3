import q, re, math
from Handler.Utils.funcs import *
from Handler.bClass import tClass, tFeature

class Fighter(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.HD.Sit("HD", 10)
        self.db.Prof.Armor.Sit("Class", ["Light", "Medium", "Heavy", "Shield"])
        self.db.Prof.Weapon.Sit("Class", q.itm.Search([0], ["Weapon"]))
        self.Refresh_Skill(["Arcana", "History", "Insight", "Investigation", "Medicine", "Religion"], 2)
        self.Feature_List = [FGT_BAS_Second_Wind, FGT_BAS_Action_Surge, FGT_BAS_Fighting_Style, FGT_BAS_Extra_Attack, FGT_BAS_Indomitable]

class Fighter_Champion(Fighter):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([
            FGT_CHP_Improved_Critical,
            FGT_CHP_Remarkable_Athlete,
            FGT_CHP_Survivor
        ])

class Fighter_Eldritch_Knight(Fighter):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([
            FGT_ELK_Weapon_Bond,
            FGT_ELK_War_Magic,
            FGT_ELK_Eldritch_Strike,
            FGT_ELK_Arcane_Charge
        ])

class Fighter_Samuri(Fighter):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([
            FGT_SAM_Bonus_Proficiency,
            FGT_SAM_Fighting_Spirit,
            FGT_SAM_Elegant_Courtier,
            FGT_SAM_Tireless_Spirit,
            FGT_SAM_Rapid_Strike,
            FGT_SAM_Strength_Before_Death
        ])
        
class FGT_BAS_Second_Wind(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.max_uses = 1
        self.Tag = "Use"
        self.Desc = [f"(Bonus Action) Regain 1d10 + {self.L} HP."]
        self.Recharge = ["Short", "Long"]
        self.Use = [False] * self.max_uses
        
        self.Set()
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        past_use = self.get_past("Use")
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class FGT_BAS_Action_Surge(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Use"
        self.Desc = ["(Free) Take one additional action on your turn."]
        self.Recharge = ["Short", "Long"]
        
        self.max_uses = [0,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2][self.L]
        self.Use = [False] * self.max_uses
        
        self.Set()
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        past_use = self.get_past("Use")
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class Fighting_Style:
    def __init__(self, mgr):
        self.mgr = mgr

    @property
    def PB(self): return self.mgr.PB

    @property
    def STR(self): return self.mgr.Atr.STR.Mod

    @property
    def Style_List(self):
        return list(self.Styles.keys())
        
    @property
    def Styles(self):
        return {
            "Archery": "You gain a +2 bonus to attack rolls you make with ranged weapons.",
            "Defense": "While you are wearing armor, you gain a +1 bonus to AC.",
            "Dueling": "When you are wielding a melee weapon in one hand and no other weapons, you gain a +2 bonus to damage rolls with that weapon.",
            "Great Weapon Fighting": "When you roll a 1 or 2 on a damage die for an attack you make with a melee weapon that you are wielding with two hands, you can reroll the die and must use the new roll. The weapon must have the two-handed or versatile property for you to gain this benefit.",
            "Protection": "When a creature you can see attacks a target other than you that is within 5 feet of you, you can use your reaction to impose disadvantage on the attack roll. You must be wielding a shield.",
            "Two Weapon Fighting": "When you engage in two-weapon fighting, you can add your ability modifier to the damage of the second attack.",
            "Blind Fighting": "You have blindsight with a range of 10 feet. Within that range, you can effectively see anything that isn't behind total cover.",
            "Interception": f"When a creature you can see hits a target, other than you, within 5 feet of you with an attack, you can use your reaction to reduce the damage the target takes by 1d10 + {self.PB}. You must be wielding a shield or a simple or martial weapon to use this reaction.",
            "Thrown Weapon Fighting": "You can draw a weapon that has the thrown property as part of the attack you make with the weapon. In addition, when you hit with a ranged attack using a thrown weapon, you gain a +2 bonus to the damage roll.",
            "Unarmed Fighting": f"Your unarmed strikes can deal bludgeoning damage equal to 1d6 + {self.STR}. If you aren't wielding any weapons or a shield when you make the attack roll, the d6 becomes a d8. At the start of each of your turns, you can deal 1d4 bludgeoning damage to one creature grappled by you."
        }

    def Style_Desc(self, keys):
        output = keys.copy()
        for v, item in enumerate(keys):
            output[v] = self.Styles.get(item, "")
        return output

class FGT_BAS_Fighting_Style(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Select"
        self.Choices = 1
        if self.SC == "Champion" and self.L >= 10: self.Choices = 2
        self.Desc = [""] * self.Choices
        self.Set()
        
        self.Select = [""] * self.Choices
        self.Update({
            "Select": self.Select,
            "Options": Fighting_Style(self).Style_List
        })

    def Refresh(self):
        past_sel = self.get_past("Select")
        if past_sel is None: past_sel = []
        self.Select = (past_sel + [""] * self.Choices)[:self.Choices]

        Handler = Fighting_Style(self)
        self.Desc = Handler.Style_Desc(self.Select)
        
        self.Update({"Select": self.Select, "Desc": self.Desc})


class FGT_BAS_Extra_Attack(tFeature):
    def Run(self):
        if not self.allowed(5): return False
        self.Tag = "Passive"
        
        self.Ammount = [0,0,0,0,0,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,4][self.L]
        self.Desc = [f"You can attack {self.Ammount} times whenever you take the Attack action."]
        
        self.Set()


class FGT_BAS_Indomitable(tFeature):
    def Run(self):
        if not self.allowed(9): return False
        self.Tag = "Use"
        self.Desc = ["On Failed Save, reroll and use the new roll."]
        self.Recharge = "Long"
        
        self.max_uses = [0,0,0,0,0,0,0,0,0,1,1,1,1,2,2,2,2,3,3,3,3][self.L]
        self.Use = [False] * self.max_uses
        
        self.Set()
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        past_use = self.get_past("Use")
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class FGT_CHP_Improved_Critical(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["Weapon attacks crit on 19-20"]
        
        if self.L >= 15:
            self.Name = "Superior Critical"
            self.Desc = ["Weapon attacks crit on 18-20"]
            
        self.Set()

class FGT_CHP_Remarkable_Athlete(tFeature):
    def Run(self):
        if not self.allowed(7): return False
        self.Tag = "Passive"
        
        STR = self.Atr.STR.Mod
        self.Desc = [f"Add {self.PB} to non-proficient STR/DEX/CON checks.", "Running long jump increases by {STR} ft"]
        self.Set()

class FGT_CHP_Survivor(tFeature):
    def Run(self):
        if not self.allowed(18): return False
        self.Tag = "Passive"
        CON = self.Atr.CON.Mod + 5
        self.Desc = [f"At start of turn, if at half HP or more, regain {CON} HP"]
        self.Set()

class FGT_ELK_Weapon_Bond(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["Bond with up to two weapons, Cannot be disarmed, Summon as Bonus Action."]
        self.Set()

class FGT_ELK_War_Magic(tFeature):
    def Run(self):
        if not self.allowed(7): return False
        self.Tag = "Passive"
        self.Desc = ["Action Cantrip -> Bonus Action Weapon Attack"]
        
        if self.L >= 18:
            self.Name = "Improved War Magic"
            self.Desc = ["Action Spell -> Bonus Action Weapon Attack"]
            
        self.Set()

class FGT_ELK_Eldritch_Strike(tFeature):
    def Run(self):
        if not self.allowed(10): return False
        self.Tag = "Passive"
        self.Desc = ["Hit enemy -> Disadvantage on next save against your spell."]
        self.Set()

class FGT_ELK_Arcane_Charge(tFeature):
    def Run(self):
        if not self.allowed(15): return False
        self.Tag = "Passive"
        self.Desc = ["Action Surge -> Teleport 30ft."]
        self.Set()


class FGT_SAM_Bonus_Proficiency(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["TBA"]
        self.Set()

class FGT_SAM_Fighting_Spirit(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["TBA"]
        self.Set()

class FGT_SAM_Elegant_Courtier(tFeature):
    def Run(self):
        if not self.allowed(7): return False
        self.Tag = "Passive"
        self.Desc = ["TBA"]
        self.Set()

class FGT_SAM_Tireless_Spirit(tFeature):
    def Run(self):
        if not self.allowed(10): return False
        self.Tag = "Passive"
        self.Desc = ["TBA"]
        self.Set()

class FGT_SAM_Rapid_Strike(tFeature):
    def Run(self):
        if not self.allowed(15): return False
        self.Tag = "Passive"
        self.Desc = ["TBA"]
        self.Set()

class FGT_SAM_Strength_Before_Death(tFeature):
    def Run(self):
        if not self.allowed(18): return False
        self.Tag = "Passive"
        self.Desc = ["TBA"]
        self.Set()

Fighter_Catalog = {
    "Base": Fighter,
    "Champion": Fighter_Champion,
    "Eldritch_Knight": Fighter_Eldritch_Knight,
    "Samuri": Fighter_Samuri
}