import q, re, math
from Handler.Utils.funcs import *
from Handler.bClass import tClass, tFeature

class Barbarian(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.HD.Sit("HD", 12)
        self.db.Prof.Armor.Sit("Class", ["Light", "Medium", "Shield"])
        self.db.Prof.Weapon.Sit("Class", q.itm.Search([0], ["Weapon"]))
        self.Refresh_Skill(["Animal Handling", "Athletics", "Intimidation", "Nature", "Perception", "Survival"], 2)
        self.Feature_List = [
            BRB_BAS_Rage, 
            BRB_BAS_Unarmored_Defense, 
            BRB_BAS_Reckless_Attack, 
            BRB_BAS_Danger_Sense, 
            BRB_BAS_Extra_Attack, 
            BRB_BAS_Fast_Movement,
            BRB_BAS_Feral_Instinct,
            BRB_BAS_Brutal_Critical,
            BRB_BAS_Relentless_Rage
        ]

class Barbarian_Berserker(Barbarian):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([
            BRB_BER_Frenzy,
            BRB_BER_Mindless_Rage,
            BRB_BER_Intimidating_Presence,
            BRB_BER_Retaliation
        ])

class Barbarian_Totem_Warrior(Barbarian):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([
            BRB_TOT_Spirit_Seeker,
            BRB_TOT_Totem_Spirit,
            BRB_TOT_Aspect_of_the_Beast,
            BRB_TOT_Spirit_Walker,
            BRB_TOT_Totemic_Attunement
        ])

class BRB_BAS_Rage(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Recharge = ["Long"]
        
        dmg_bonus = [0,2,2,2,2,2,2,2,2,3,3,3,3,3,3,3,4,4,4,4,4][self.L]
        self.Desc = [
            "(Bonus Action) Enter Rage for 1 minute.",
            "Advantage on STR checks and saves.",
            f"+{dmg_bonus} damage on STR melee attacks.",
            "Resistance to Bludgeoning, Piercing, Slashing."
        ]
        
        update_data = {"Recharge": self.Recharge}

        if self.L == 20:
            self.Tag = "Toggle"
            self.Desc[0] = "(Bonus Action) Enter Rage (Unlimited)."
            self.Toggle = [False]
            update_data["Toggle"] = self.Toggle
        else:
            self.Tag = "Use"
            self.max_uses = [0,2,2,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6][self.L]
            self.Use = [False] * self.max_uses
            update_data["Use"] = self.Use
        
        if self.L >= 15: self.Desc.append("Persistent Rage: Rage only ends early if you fall unconscious or choose to end it.")
        elif self.L >= 11: self.Desc.append("Relentless Rage: DC 10 CON save to drop to 1 HP instead of 0 while raging.")

        self.Set()
        self.Update(update_data)

    def Refresh(self):
        if self.L == 20: return
        self.max_uses = [0,2,2,3,3,3,4,4,4,4,4,4,5,5,5,5,5,6,6,6][self.L]
        past_use = self.get_past("Use")
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class BRB_BAS_Unarmored_Defense(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"While not wearing armor, AC = {10 + self.Atr.DEX.Mod + self.Atr.CON.Mod}. You can use a shield."]
        self.Set()

class BRB_BAS_Reckless_Attack(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Passive"
        self.Desc = ["(Start of Turn) Gain Advantage on STR melee attacks, but attacks against you have Advantage until next turn."]
        self.Set()

class BRB_BAS_Danger_Sense(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on DEX saves against effects you can see."]
        self.Set()

class BRB_BAS_Extra_Attack(tFeature):
    def Run(self):
        if not self.allowed(5): return False
        self.Tag = "Passive"
        self.Desc = ["You can attack twice whenever you take the Attack action."]
        self.Set()

class BRB_BAS_Fast_Movement(tFeature):
    def Run(self):
        if not self.allowed(5): return False
        self.Tag = "Passive"
        self.Desc = ["Speed increases by 10 feet while not wearing heavy armor."]
        self.Set()

class BRB_BAS_Feral_Instinct(tFeature):
    def Run(self):
        if not self.allowed(7): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on Initiative rolls. Can act in surprise round if you Rage first."]
        self.Set()

class BRB_BAS_Brutal_Critical(tFeature):
    def Run(self):
        if not self.allowed(9): return False
        self.Tag = "Passive"
        dice = [0,1,1,1,1,1,1,1,1,1,1,1,1,2,2,2,2,3,3,3,3][self.L]
        self.Desc = [f"Roll {dice} additional weapon damage die on a critical hit."]
        self.Set()

class BRB_BAS_Relentless_Rage(tFeature):
    def Run(self):
        if not self.allowed(11): return False
        self.Tag = "Passive"
        self.Desc = ["While Raging, if you drop to 0 HP, DC 10 CON save to drop to 1 HP instead. DC increases by 5 each use per rest."]
        self.Set()

class BRB_BER_Frenzy(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["When Raging, you can go into a Frenzy. Make a melee attack as a Bonus Action. Gain 1 level of exhaustion when Rage ends."]
        self.Set()

class BRB_BER_Mindless_Rage(tFeature):
    def Run(self):
        if not self.allowed(6): return False
        self.Tag = "Passive"
        self.Desc = ["While Raging, you cannot be charmed or frightened. Suspends existing effects."]
        self.Set()

class BRB_BER_Intimidating_Presence(tFeature):
    def Run(self):
        if not self.allowed(10): return False
        self.Tag = "Use"
        self.Desc = ["(Action) Frighten one creature within 30 ft (WIS Save vs 8 + PB + CHA)."]
        self.Set()

class BRB_BER_Retaliation(tFeature):
    def Run(self):
        if not self.allowed(14): return False
        self.Tag = "Passive"
        self.Desc = ["(Reaction) When you take damage from a creature within 5 ft, you can make a melee weapon attack against them."]
        self.Set()

class BRB_TOT_Spirit_Seeker(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["You can cast Beast Sense and Speak with Animals as rituals."]
        self.Set()

class Totem_Spirit_Handler:
    def __init__(self, mgr):
        self.mgr = mgr
    
    @property
    def List(self):
        return ["Bear", "Eagle", "Elk", "Tiger", "Wolf"]

    @property
    def Spirits(self):
        return {
            "Bear": "While raging, resistance to all damage except psychic.",
            "Eagle": "While raging and unarmored, Dash as Bonus Action and opportunity attacks against you have disadvantage.",
            "Elk": "While raging and unarmored, walking speed increases by 15 feet.",
            "Tiger": "While raging, add 10 feet to long jump distance and 3 feet to high jump distance.",
            "Wolf": "While raging, friends have advantage on melee attacks against hostiles within 5 ft of you."
        }
    
    def Get_Desc(self, key):
        return self.Spirits.get(key, "")

class BRB_TOT_Totem_Spirit(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Select"
        self.Choices = 1
        self.Set()
        
        self.Select = [""] * self.Choices
        self.Update({
            "Select": self.Select,
            "Options": Totem_Spirit_Handler(self).List
        })

    def Refresh(self):
        past_sel = self.get_past("Select")
        if past_sel is None: past_sel = []
        self.Select = (past_sel + [""] * self.Choices)[:self.Choices]
        
        Handler = Totem_Spirit_Handler(self)
        self.Desc = [Handler.Get_Desc(self.Select[0])]
        
        self.Update({"Select": self.Select, "Desc": self.Desc})

class BRB_TOT_Aspect_of_the_Beast(tFeature):
    def Run(self):
        if not self.allowed(6): return False
        self.Tag = "Select"
        self.Choices = 1
        self.Set()
        
        self.Select = [""] * self.Choices
        self.Update({
            "Select": self.Select,
            "Options": ["Bear", "Eagle", "Elk", "Tiger", "Wolf"]
        })

    def Refresh(self):
        past_sel = self.get_past("Select")
        if past_sel is None: past_sel = []
        self.Select = (past_sel + [""] * self.Choices)[:self.Choices]
        
        desc_map = {
            "Bear": "Carrying capacity is doubled, advantage on push/pull/lift/break.",
            "Eagle": "Can see up to 1 mile clearly. Dim light is not Disadvantage.",
            "Elk": "Travel pace is doubled for you and up to 10 companions.",
            "Tiger": "Gain proficiency in two skills: Athletics, Acrobatics, Stealth, or Survival.",
            "Wolf": "You can track while traveling at a fast pace. Move stealthily at normal pace."
        }
        
        self.Desc = [desc_map.get(self.Select[0], "")]
        self.Update({"Select": self.Select, "Desc": self.Desc})

class BRB_TOT_Spirit_Walker(tFeature):
    def Run(self):
        if not self.allowed(10): return False
        self.Tag = "Passive"
        self.Desc = ["You can cast Commune with Nature as a ritual."]
        self.Set()

class BRB_TOT_Totemic_Attunement(tFeature):
    def Run(self):
        if not self.allowed(14): return False
        self.Tag = "Select"
        self.Choices = 1
        self.Set()
        
        self.Select = [""] * self.Choices
        self.Update({
            "Select": self.Select,
            "Options": ["Bear", "Eagle", "Elk", "Tiger", "Wolf"]
        })

    def Refresh(self):
        past_sel = self.get_past("Select")
        if past_sel is None: past_sel = []
        self.Select = (past_sel + [""] * self.Choices)[:self.Choices]
        
        desc_map = {
            "Bear": "While raging, hostiles within 5ft have Disadvantage on attacks against targets other than you.",
            "Eagle": "While raging, you have a flying speed equal to current walking speed. You fall if you end turn in air.",
            "Elk": "While raging, use Bonus Action to move through large or smaller creature's space. Prone DC 8+STR+PB.",
            "Tiger": "While raging, if you move 20ft straight toward target, Bonus Action melee attack.",
            "Wolf": "While raging, use Bonus Action to knock Large or smaller creature prone when you hit with melee weapon."
        }
        
        self.Desc = [desc_map.get(self.Select[0], "")]
        self.Update({"Select": self.Select, "Desc": self.Desc})

Barbarian_Catalog = {
    "Base": Barbarian,
    "Berserker": Barbarian_Berserker,
    "Totem_Warrior": Barbarian_Totem_Warrior
}