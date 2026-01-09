import q, re, math
from Handler.Utils.funcs import *
from Handler.bClass import tClass, tFeature

class Monk(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.HD.Sit("HD", 8)
        self.db.Prof.Weapon.Sit("Class", q.itm.Search([0], ["Simple", "Weapon"]) + ["Shortsword"])
        self.Refresh_Skill(["Acrobatics", "Athletics", "History", "Insight", "Religion", "Stealth"], 2)

        self.Feature_List = [
            MNK_BAS_Unarmored_Defense,
            MNK_BAS_Martial_Arts,
            MNK_BAS_Ki,
            MNK_BAS_Unarmored_Movement,
            MNK_BAS_Deflect_Missiles,
            MNK_BAS_Slow_Fall,
            MNK_BAS_Extra_Attack,
            MNK_BAS_Stunning_Strike,
            MNK_BAS_Ki_Empowered_Strikes,
            MNK_BAS_Evasion,
            MNK_BAS_Stillness_Of_Mind,
            MNK_BAS_Diamond_Soul,
            MNK_BAS_Timeless_Body,
            MNK_BAS_Empty_Body,
            MNK_BAS_Perfect_Self
        ]

class Monk_Open_Hand(Monk):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([
            MNK_OPN_Open_Hand_Technique,
            MNK_OPN_Wholeness_Of_Body,
            MNK_OPN_Tranquility,
            MNK_OPN_Quivering_Palm
        ])

class MNK_BAS_Unarmored_Defense(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"While not wearing armor or shield, AC = {10 + self.Atr.DEX.Mod + self.Atr.WIS.Mod}."]
        self.Set()

class MNK_BAS_Martial_Arts(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        dice = ["", "1d4", "1d4", "1d4", "1d4", "1d6", "1d6", "1d6", "1d6", "1d6", "1d6", "1d8", "1d8", "1d8", "1d8", "1d8", "1d8", "1d10", "1d10", "1d10", "1d10"]
        self.Desc = [
            "Use DEX instead of STR for Monk weapons/Unarmed.",
            f"Martial Arts Die: {dice[self.L]}",
            "Bonus Action Unarmed Strike after Attack action."
        ]
        self.Set()

class MNK_BAS_Ki(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Resource"
        self.Recharge = ["Short", "Long"]
        self.Points = [self.L, self.L]
        self.Actions = {
            "Flurry_of_Blows": {
                "Cost": 1, 
                "Desc": "Immediately after Attack action, make two unarmed strikes as bonus action."
            },
            "Patient_Defense": {
                "Cost": 1, 
                "Desc": "Dodge action as bonus action."
            },
            "Step_of_the_Wind": {
                "Cost": 1, 
                "Desc": "Disengage or Dash as bonus action, jump distance doubled."
            }
        }
        self.Set()
        self.Update({"Points": self.Points, "Actions": self.Actions, "Recharge": self.Recharge})

    def Refresh(self):
        past = self.get_past("Points")
        current = self.L if len(past) < 2 else past[1]
        self.Points = [self.L, current]


class MNK_BAS_Unarmored_Movement(tFeature):
    def Run(self):
        if not self.allowed(2): return False
        self.Tag = "Passive"
        bonus = [0,10,10,10,10,15,15,15,15,20,20,20,20,25,25,25,25,30,30,30,30][self.L]
        self.Desc = [f"Speed increased by {bonus} ft while unarmored."]
        if self.L >= 9:
            self.Desc.append("You can move along vertical surfaces and liquids.")
        self.Set()

class MNK_BAS_Deflect_Missiles(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        amt = self.Atr.DEX.Mod + self.L
        self.Desc = [f"Reaction: Reduce ranged damage by 1d10 + {amt}. If 0, spend 1 Ki to throw it back."]
        self.Set()

class MNK_BAS_Slow_Fall(tFeature):
    def Run(self):
        if not self.allowed(4): return False
        self.Tag = "Passive"
        amount = self.L * 5
        self.Desc = [f"Reaction: Reduce falling damage by {amount}."]
        self.Set()

class MNK_BAS_Extra_Attack(tFeature):
    def Run(self):
        if not self.allowed(5): return False
        self.Tag = "Passive"
        self.Desc = ["Attack twice when taking the Attack action."]
        self.Set()

class MNK_BAS_Stunning_Strike(tFeature):
    def Run(self):
        if not self.allowed(5): return False
        self.Tag = "Resource_Use"
        self.Actions = {
            "Stunning_Strike": {
                "Cost": 1,
                "Desc": "On melee weapon hit, target Stunned until end of next turn if they fail CON save."
            }
        }
        self.Set()
        self.Update({"Actions": self.Actions})

class MNK_BAS_Ki_Empowered_Strikes(tFeature):
    def Run(self):
        if not self.allowed(6): return False
        self.Tag = "Passive"
        self.Desc = ["Unarmed strikes count as magical for overcoming resistances."]
        self.Set()

class MNK_BAS_Evasion(tFeature):
    def Run(self):
        if not self.allowed(7): return False
        self.Tag = "Passive"
        self.Desc = ["DEX Saves: Take no damage on success, half on fail."]
        self.Set()

class MNK_BAS_Stillness_Of_Mind(tFeature):
    def Run(self):
        if not self.allowed(7): return False
        self.Tag = "Passive"
        self.Desc = ["Action: End one effect causing Charmed or Frightened."]
        self.Set()

class MNK_BAS_Diamond_Soul(tFeature):
    def Run(self):
        if not self.allowed(14): return False
        self.Tag = "Resource_Use"
        self.Desc = ["Proficiency in all Saving Throws."]
        self.Actions = {
            "Diamond_Soul_Reroll": {
                "Cost": 1,
                "Desc": "Reroll a failed saving throw."
            }
        }
        self.Set()
        self.Update({"Actions": self.Actions})

class MNK_BAS_Timeless_Body(tFeature):
    def Run(self):
        if not self.allowed(15): return False
        self.Tag = "Passive"
        self.Desc = ["You suffer no frailty of old age, can't be aged magically, and need no food or water."]
        self.Set()

class MNK_BAS_Empty_Body(tFeature):
    def Run(self):
        if not self.allowed(18): return False
        self.Tag = "Resource_Use"
        self.Actions = {
            "Invisibility": {
                "Cost": 4,
                "Desc": "Invisible and Resist all damage (except Force) for 1 min."
            },
            "Astral_Projection": {
                "Cost": 8,
                "Desc": "Cast Astral Projection (Self only)."
            }
        }
        self.Set()
        self.Update({"Actions": self.Actions})

class MNK_BAS_Perfect_Self(tFeature):
    def Run(self):
        if not self.allowed(20): return False
        self.Tag = "Passive"
        self.Desc = ["Start of combat: If Ki is 0, regain 4 Ki."]
        self.Set()

class MNK_OPN_Open_Hand_Technique(tFeature):
    def Run(self):
        if not self.allowed(3): return False
        self.Tag = "Passive"
        self.Desc = ["Flurry of Blows Augment: Knock Prone (DEX), Push 15ft (STR), or No Reactions."]
        self.Set()

class MNK_OPN_Wholeness_Of_Body(tFeature):
    def Run(self):
        if not self.allowed(6): return False
        self.Tag = "Use"
        heal = self.L * 3
        self.Desc = [f"Action: Regain {heal} HP."]
        self.Recharge = ["Long"]
        self.max_uses = 1
        self.Use = [False] * self.max_uses
        self.Set()
        self.Update({"Use": self.Use, "Recharge": self.Recharge})

    def Refresh(self):
        past_use = self.get_past("Use")
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class MNK_OPN_Tranquility(tFeature):
    def Run(self):
        if not self.allowed(11): return False
        self.Tag = "Passive"
        self.Desc = [f"Start of day: Gain Sanctuary effect (DC {8 + self.Atr.WIS.Mod + self.PB}). Ends if you attack or cast harmful spell."]
        self.Set()

class MNK_OPN_Quivering_Palm(tFeature):
    def Run(self):
        if not self.allowed(17): return False
        self.Tag = "Resource_Use"
        
        self.Actions = {
            "Quivering_Palm": {
                "Cost": 3,
                "Desc": f"Action to end vibrations. DC {8 + self.Atr.WIS.Mod + self.PB} CON Save: 0 HP on fail, 10d10 Necrotic on success."
            }
        }
        self.Set()
        self.Update({"Actions": self.Actions})

Monk_Catalog = {
    "Base": Monk,
    "Open_Hand": Monk_Open_Hand
}