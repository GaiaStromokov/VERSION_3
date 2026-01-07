import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Dragonborn(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Prof.Lang.Sit("Race", ["Common", "Draconic"])
        self.Feature_List = []

class Dragonborn_Black(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Black"
        self.Type = "Acid"
        self.Shape = "Line"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Blue(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Blue"
        self.Type = "Lightning"
        self.Shape = "Line"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Brass(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Brass"
        self.Type = "Fire"
        self.Shape = "Line"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Bronze(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Bronze"
        self.Type = "Lightning"
        self.Shape = "Line"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Copper(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Copper"
        self.Type = "Acid"
        self.Shape = "Line"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Gold(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Gold"
        self.Type = "Fire"
        self.Shape = "Cone"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Green(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Green"
        self.Type = "Poison"
        self.Shape = "Cone"
        self.Save = "CON"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Red(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Red"
        self.Type = "Fire"
        self.Shape = "Cone"
        self.Save = "DEX"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_Silver(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "Silver"
        self.Type = "Cold"
        self.Shape = "Cone"
        self.Save = "CON"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class Dragonborn_White(Dragonborn):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Color = "White"
        self.Type = "Cold"
        self.Shape = "Cone"
        self.Save = "CON"
        self.Feature_List.extend([DRA_BAS_Breath_Weapon, DRA_BAS_Draconic_Resistance])

class DRA_BAS_Breath_Weapon(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        r = self.Parent
        self.max_uses = [0,1,1,1,1,2,2,2,2,2,3,3,3,3,3,4,4,4,4,4,4][self.L]
        self.Damage = [0,2,2,2,2,3,3,3,3,3,4,4,4,4,4,5,5,5,5,5,5][self.L]
        self.Tag = "Use"
        self.Desc = [f"(Action) 30ft {r.Shape}, DC {10 + getattr(self.Atr, r.Save).Mod + self.PB} {r.Save} save. Fail: {self.Damage}d6 {r.Type} dmg. Success: Half."]
        self.Set()
        self.Use = [False] * self.max_uses
        self.Recharge = ["Short", "Long"]
        self.Update({"Use": self.Use, "Recharge": self.Recharge})
        
    def Refresh(self):
        past_use = self.get_past("Use")
        self.Use = (past_use + [False] * self.max_uses)[:self.max_uses]
        self.Update({"Use": self.Use})

class DRA_BAS_Draconic_Resistance(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        r = self.Parent
        self.Tag = "Passive"
        self.Desc = [f"You have resistance to {r.Type} damage."]
        self.Set()

Dragonborn_Catalog = {
    "Base": Dragonborn,
    "Black": Dragonborn_Black,
    "Blue": Dragonborn_Blue,
    "Brass": Dragonborn_Brass,
    "Bronze": Dragonborn_Bronze,
    "Copper": Dragonborn_Copper,
    "Gold": Dragonborn_Gold,
    "Green": Dragonborn_Green,
    "Red": Dragonborn_Red,
    "Silver": Dragonborn_Silver,
    "White": Dragonborn_White
}