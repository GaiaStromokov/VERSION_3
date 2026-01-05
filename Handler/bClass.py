import q, re, math
from Handler.Utils.funcs import *
# ==========================================
# HANDLER CLASSES
# ==========================================

class bClass:
    def __init__(self):
        self.Mode = "Refresh"
    
    @property
    def dbm(self): return q.dbm

    @property
    def db(self): return q.dbm.db

    @property
    def C(self): return q.dbm.db.Core.Class

    @property
    def SC(self): return q.dbm.db.Core.Subclass

    def Startup(self):
        if not self.C: return
        self.Refresh_Class_Data()

    def Refresh(self):
        if not self.C: return
        self.Mode = "Refresh"
        self.Refresh_Class_Data()

    def New(self):
        if not self.C: return
        self.Mode = "New"
        self.Refresh_Class_Data()


    def Refresh_Class_Data(self):
        self.db.Clear_Class_Globals()
        if self.C not in Catalog: return
        Group = Catalog[self.C]
        Actor = Group[self.SC] if (self.SC and self.SC in Group) else Group["Base"]
        instance = Actor(self)
        instance.execute()
    


class tClass:
    def __init__(self, mgr):
        self.bClass = mgr
        self.Features = {}
        self.Feature_List = []

    @property
    def db(self): return self.bClass.db

    @property
    def dbm(self): return self.bClass.dbm

    def Refresh_Skill(self, List, Num):
        Mode = self.bClass.Mode

        if Mode == "New":
            self.db.Class.Skill.Sit_From_Class(List, Num)

        if Mode == "Refresh":
            past = self.db.Class.Skill.Select
            self.db.Class.Skill.Sit_From_Class(List, Num)
            self.db.Class.Skill.Select = (past + [""] * Num)[:Num]

        for skill in self.db.Class.Skill.Select:
            if skill:
                getattr(self.db.Skill, skill).Sit("Class", 0, True)
                
    def execute(self):
        Mode = self.bClass.Mode
        for F_Class in self.Feature_List:
            feature = F_Class(self)
            ran = feature.Run()
            if Mode == "Refresh" and ran is not False:
                feature.Refresh()
        self.db.Class.Features = self.Features


class tFeature:
    def __init__(self, mgr):
        self.tClass = mgr
        self.Name = self.__class__.__name__[8:]
        self.Tag = ""
        self.Desc = []

    @property
    def Atr(self): return q.dbm.db.Atr
    @property
    def L(self): return q.dbm.db.Core.Level

    @property
    def SC(self): return q.dbm.db.Core.Subclass

    @property
    def PB(self): return q.dbm.db.Core.PB
    
    @property
    def Class_features(self): 
        return q.dbm.db.Class.Features 
    
    @property
    def Place(self): 
        return self.tClass.Features 

    def allowed(self, req_level):
        return self.L >= req_level

    def get_past(self, key):
        if self.Name in self.Class_features:
            return self.Class_features[self.Name].get(key)
        return []

    def Set(self):
        place = self.Place.setdefault(self.Name, {})
        place["Tag"] = self.Tag
        place["Desc"] = self.Desc

    def Update(self, data):
        place = self.Place.setdefault(self.Name, {})
        place.update(data)

    def Run(self):
        pass

    def Refresh(self):
        pass


class Empty(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = []

class EMP_BAS_Empty(Empty):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = []


class Fighter(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.HD.Sit("HD", 10)
        self.db.Prof.Armor.Sit("Class", ["Light", "Medium", "Heavy", "Shield"])
        self.db.Prof.Weapon.Sit("Class", q.w.BAW)
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

class Wizard(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.HD.Sit("HD", 6)
        self.db.Prof.Weapon.Sit("Class", ["Dagger", "Dart", "sling", "Quarterstaff", "Light_Crossbow"])
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
    # lReq = 6
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
    # lReq = 14
    def Run(self):
        if not self.allowed(14): return False
        self.Tag = "Passive"
        self.Desc = ["Summoned creatures have +30 temp HP."]
        self.set()

    def Refresh(self):
        pass


Catalog = {
    "Empty": {
        "Base": Empty,
    },
    "Fighter": {
        "Base": Fighter,
        "Champion": Fighter_Champion,
        "Eldritch_Knight": Fighter_Eldritch_Knight,
        "Samuri": Fighter_Samuri
    },
    "Wizard": {
        "Base": Wizard,
        "Abjuration": Wizard_Abjuration,
        "Conjuration": Wizard_Conjuration
    }
}