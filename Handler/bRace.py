import q, re, math
from Handler.Utils.funcs import *


class bRace:
    def __init__(self):
        self.Mode = "Refresh"
    
    @property
    def dbm(self): return q.dbm

    @property
    def db(self): return q.dbm.db

    @property
    def R(self): return q.dbm.db.Core.Race

    @property
    def SR(self): return q.dbm.db.Core.Subrace

    def Startup(self):
        if not self.R: return
        self.Refresh_Race_Data()

    def Refresh(self):
        if not self.R: return
        self.Mode = "Refresh"
        self.Refresh_Race_Data()

    def New(self):
        if not self.R: return
        self.Mode = "New"
        self.Refresh_Race_Data()


    def Refresh_Race_Data(self):
        self.db.Clear_Race_Globals()
        if self.R not in Catalog: return
        Group = Catalog[self.R]
        Actor = Group[self.SR] if (self.SR and self.SR in Group) else Group["Base"]
        instance = Actor(self)
        instance.execute()
    


class tRace:
    def __init__(self, mgr):
        self.bRace = mgr
        self.Features = {}
        self.Feature_List = []

    @property
    def db(self): return self.bRace.db

    @property
    def dbm(self): return self.bRace.dbm

    def Refresh_Skill(self, List, Num):
        Mode = self.bRace.Mode

        if Mode == "New":
            self.db.Race.Skill.Sit_From_Race(List, Num)

        if Mode == "Refresh":
            past = self.db.Race.Skill.Select
            self.db.Race.Skill.Sit_From_Race(List, Num)
            self.db.Race.Skill.Select = (past + [""] * Num)[:Num]

        for skill in self.db.Race.Skill.Select:
            if skill:
                getattr(self.db.Skill, skill).Sit("Race", 0, True)
                
    def execute(self):
        Mode = self.bRace.Mode
        for F_Race in self.Feature_List:
            feature = F_Race(self)
            ran = feature.Run()
            if Mode == "Refresh" and ran is not False:
                feature.Refresh()
        self.db.Race.Features = self.Features


class tFeature:
    def __init__(self, mgr):
        self.tRace = mgr
        self.Name = self.__class__.__name__[8:]
        self.Tag = ""
        self.Desc = []

    @property
    def Atr(self):
        return q.dbm.db.Atr
    
    @property
    def Parent(self): return self.tRace
    @property
    def L(self): return q.dbm.db.Core.Level

    @property
    def SR(self): return q.dbm.db.Core.Subrace

    @property
    def PB(self): return q.dbm.db.Core.PB

    @property
    def Atr(self): return q.dbm.db.Atr
    
    @property
    def Race_features(self): 
        return q.dbm.db.Race.Features 
    
    @property
    def Place(self): 
        return self.tRace.Features 

    def allowed(self, req_level):
        return self.L >= req_level

    def get_past(self, key):
        if self.Name in self.Race_features:
            return self.Race_features[self.Name].get(key)
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


class Empty(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = []



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
        
#----------------------
class Dwarf(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 25)
        self.db.Vision.Dark.Sit("Race", 60)
        self.db.Prof.Lang.Sit("Race", ["Common", "Dwarvish"])
        self.db.Prof.Weapon.Sit("Race", ["Battleaxe", "Handaxe", "Light_Hammer", "Warhammer"])
        self.Feature_List = [DWF_BAS_Dwarven_Resilience, DWF_BAS_Stonecunning]


class Dwarf_Hill(Dwarf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([DWF_HIL_Dwarven_Toughness])


class Dwarf_Mountain(Dwarf):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Prof.Armor.Sit("Race", ["Light", "Medium"])
        self.Feature_List.extend([])


class DWF_BAS_Dwarven_Resilience(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Advantage on Poison saves, Resistance to Poison damage."]
        self.Set()


class DWF_BAS_Stonecunning(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"Add {self.PB} to History checks on stonework."]
        self.Set()


class DWF_HIL_Dwarven_Toughness(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "HP"
        self.Desc = [f"HP Max increases by {self.L}."]
        self.Set()
        self.Update({"HP": "LEVEL"})

#--------------------------------------------------------------------------------
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
        self.Tag = "Use"
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

class Gnome(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 25)
        self.db.Vision.Dark.Sit("Race", 60)
        self.db.Prof.Lang.Sit("Race", ["Common", "Gnomish"])
        self.Feature_List = [GNM_BAS_Gnome_Cunning]

class Gnome_Forest(Gnome):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([GNM_FOR_Natural_Illusionist, GNM_FOR_Speak_with_Small_Beasts])


class Gnome_Rock(Gnome):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Prof.Tool.Sit("Race", ["Tinker"])
        self.Feature_List.extend([GNM_ROK_Artificers_Lore, GNM_ROK_Tinker])

class GNM_BAS_Gnome_Cunning(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["You have advantage on all Intelligence, Wisdom, and Charisma saves against magic."]
        self.Set()

    
class GNM_FOR_Natural_Illusionist(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Spell"
        self.Desc = ["Gain Magic"]
        self.Set()
        self.Spells = {"Minor Illusion": "Will"}
        self.Update({"Spells": self.Spells})

class GNM_FOR_Speak_with_Small_Beasts(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Communicate simple ideas with Small beasts."]
        self.Set()


class GNM_ROK_Artificers_Lore(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = [f"Add {2*self.PB} to History checks on magic/tech items."]
        self.Set()

class GNM_ROK_Tinker(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Tinker"
        self.Desc = ["Construct Tiny clockwork device (1hr, 10gp, AC 5, 1hp). Lasts 24h. Max 3."]
        self.Set()

        self.max_choices = 1
        self.Select = [""] * self.max_choices
        self.Options = ["Clockwork Toy", "Fire Starter", "Music Box"]

        self.Multi_Desc = {
            "Clockwork Toy": "Moves 5ft random direction, makes noise.",
            "Fire Starter": "Action to produce miniature flame.",
            "Music Box": "Plays single song.",
        }

        self.Update({"Select": self.Select, "Options": self.Options, "Multi_Desc": self.Multi_Desc})

    def Refresh(self):
        past_sel = self.get_past("Select") or []
        self.Select = (past_sel + [""] * self.max_choices)[:self.max_choices]
        self.Update({"Select": self.Select})

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


class Human(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Prof.Lang.Sit("Race", ["Common"])
        self.Feature_List = []




class Tiefling(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Vision.Dark.Sit("Race", 60)
        self.db.Prof.Lang.Sit("Race", ["Common", "Infernal"])
        self.Feature_List = [TIF_BAS_Hellish_Resistance]


class Tiefling_Asmodeus(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_ASM_Infernal_Legacy])


class Tiefling_Baalzebul(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_BAL_Legacy_of_Maladomini])


class Tiefling_Dispater(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_DIS_Legacy_of_Dis])


class Tiefling_Fierna(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_FIE_Legacy_of_Phlegethos])


class Tiefling_Glasya(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_GLA_Legacy_of_Malbolge])


class Tiefling_Levistus(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_LEV_Legacy_of_Stygia])


class Tiefling_Mammon(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_MAM_Legacy_of_Minauros])


class Tiefling_Mephistopheles(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_MEP_Legacy_of_Cania])


class Tiefling_Zariel(Tiefling):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List.extend([TIF_ZAR_Legacy_of_Avernus])


class TIF_BAS_Hellish_Resistance(tFeature):
    def Run(self):
        if not self.allowed(1): return False
        self.Tag = "Passive"
        self.Desc = ["Resistance to Fire damage."]
        self.Set()


class TIF_Spell_Legacy(tFeature):
    Given = {}

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


class TIF_ASM_Infernal_Legacy(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Hellish Rebuke": [3, 1], "Darkness": [5, 1]}
class TIF_BAL_Legacy_of_Maladomini(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Ray of Sickness": [3, 1], "Crown of Madness": [5, 1]}
class TIF_DIS_Legacy_of_Dis(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Disguise Self": [3, 1], "Detect Thoughts": [5, 1]}
class TIF_FIE_Legacy_of_Phlegethos(TIF_Spell_Legacy):
    Given = {"Friends": [1, "Will"], "Charm Person": [3, 1], "Suggestion": [5, 1]}
class TIF_GLA_Legacy_of_Malbolge(TIF_Spell_Legacy):
    Given = {"Minor Illusion": [1, "Will"], "Disguise Self": [3, 1], "Invisibility": [5, 1]}
class TIF_LEV_Legacy_of_Stygia(TIF_Spell_Legacy):
    Given = {"Ray of Frost": [1, "Will"], "Armor of Agathys": [3, 1], "Darkness": [5, 1]}
class TIF_MAM_Legacy_of_Minauros(TIF_Spell_Legacy):
    Given = {"Mage Hand": [1, "Will"], "Tenser's Floating Disk": [3, 1], "Arcane Lock": [5, 1]}
class TIF_MEP_Legacy_of_Cania(TIF_Spell_Legacy):
    Given = {"Mage Hand": [1, "Will"], "Burning Hands": [3, 1], "Flame Blade": [5, 1]}
class TIF_ZAR_Legacy_of_Avernus(TIF_Spell_Legacy):
    Given = {"Thaumaturgy": [1, "Will"], "Searing Smite": [3, 1], "Branding Smite": [5, 1]}


Catalog = {
    "Empty": {
        "Base": Empty
    },
    "Dragonborn": {
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
    },
    "Dwarf": {
        "Base": Dwarf,
        "Hill": Dwarf_Hill,
        "Mountain": Dwarf_Mountain
    },
    "Elf": {
        "Base": Elf,
        "Drow": Elf_Drow,
        "High": Elf_High,
        "Shadar_Kai": Elf_Shadar_Kai,
        "Wood": Elf_Wood
    },
    "Gnome": {
        "Base": Gnome,
        "Forest": Gnome_Forest,
        "Rock": Gnome_Rock
    },
    "Half_Orc": {
        "Base": Half_Orc
    },
    "Halfling": {
        "Base": Halfling,
        "Lightfoot": Halfling_Lightfoot,
        "Stout": Halfling_Stout
    },
    "Harengon": {
        "Base": Harengon
    },
    "Human": {
        "Base": Human
    },
    "Tiefling": {
        "Base": Tiefling,
        "Asmodeus": Tiefling_Asmodeus,
        "Baalzebul": Tiefling_Baalzebul,
        "Dispater": Tiefling_Dispater,
        "Fierna": Tiefling_Fierna,
        "Glasya": Tiefling_Glasya,
        "Levistus": Tiefling_Levistus,
        "Mammon": Tiefling_Mammon,
        "Mephistopheles": Tiefling_Mephistopheles,
        "Zariel": Tiefling_Zariel
    }
}