import select
from Utils.Pathing import get_path
from Handbook.Rules import Rules
import json

rules = Rules()

d_pb = [0,2,2,2,2,3,3,3,3,4,4,4,4,5,5,5,5,6,6,6,6]


class s_Atr:
    def __init__(self, data):
        self.Base = data["Base"]
        self.Race = data["Race"]
        self.Milestone = data["Milestone"]
    
    def Sit(self, cat, val):
        setattr(self, cat, int(val))
    
    @property
    def Val(self):
        return self.Base + self.Race + self.Milestone

    @property
    def Mod(self):
        return (self.Val - 10) // 2

    def to_dict(self):
        return {
            "Base": self.Base,
            "Race": self.Race,
            "Milestone": self.Milestone
        }

class s_Vision:
    def __init__(self, data):
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
    
    @property
    def Val(self):
        return self.Race + self.Class + self.Milestone

    def to_dict(self):
        return {
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone
        }

class s_Speed:
    def __init__(self, data):
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]

    def Sit(self, cat, val):
        setattr(self, cat, int(val))
    
    @property
    def Val(self):
        return self.Race + self.Class + self.Milestone

    def to_dict(self):
        return {
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone
        }

class s_Prof:
    def __init__(self, data):
        self.Base = data["Base"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Background = data["Background"]

    def Sit(self, cat, val):
        getattr(self, cat).append(val)

    def Clear(self, cat):
        setattr(self, cat, [])
    
    @property
    def Val(self):
        combined = self.Base + self.Class + self.Milestone + self.Background
        return [x for i, x in enumerate(combined) if x not in combined[:i]]

    def to_dict(self):
        return {
            "Base": self.Base,
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone,
            "Background": self.Background
        }

class s_Class_Skill:
    def __init__(self, db, data):
        self.Options = data["Options"]
        self.Select = data["Select"]

    def Sit_From_Class(self, val, num):
        self.Options = val
        self.Select = [""]*num

    def Sit_Select(self, idx, inp):
        # Added based on context usage in m_Class
        self.Select[idx] = inp
        
    def to_dict(self):
        return {
            "Options": self.Options,
            "Select": self.Select
        }
        
class s_Skill:
    def __init__(self, db, Atr, data):
        self.db = db
        self.Atr = Atr
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Background = data["Background"]

    def Sit(self, cat, key, val):
        getattr(self, cat)[key] = val

    def Clear(self, cat):
        setattr(self, cat, [False, False])
        
    @property
    def Val(self):
        return any((self.Race[0], self.Class[0], self.Milestone[0], self.Background[0]))

    @property
    def Mod(self):
        pb = self.db.Core.PB
        mod = getattr(self.db.Atr, self.Atr).Mod
        Exp = any((self.Race[1], self.Class[1], self.Milestone[1], self.Background[1]))

        mv = mod
        if self.Val:
            mv += pb
        if Exp:
            mv += pb
        return mv
        
    def to_dict(self):
        return {
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone,
            "Background": self.Background,
        }

# --- Main Section Classes (m_) ---


class s_Closet:
    def __init__(self, db, data):
        self.Armor = data["Armor"]
        self.Hand_1 = data["Hand_1"]
        self.Hand_2 = data["Hand_2"]

    def to_dict(self):
        return {
            "Armor": self.Armor,
            "Hand_1": self.Hand_1,
            "Hand_2": self.Hand_2,
        }

class m_Inventory:
    def __init__(self, db, data):
        self.db = db
        self.Closet = s_Closet(db, data["Closet"])
        self.Backpack = data["Backpack"]
    
    def Bazaar_Add_Item(self, cat, item):
        self.Backpack_Add_Item(item)

    def Backpack_Add_Item(self, item):
        if item not in self.Backpack: self.Backpack[item] = {}
        self.Backpack[item]["Player"] = self.Backpack[item].get("Player", 0) + 1

    def Backpack_Sub_Item(self, item):
        pack = self.Backpack[item]
        parent = "Player" if "Player" in pack else next(iter(pack))
        pack[parent] -= 1
        if pack[parent] <= 0: del pack[parent]
        if not pack: del self.Backpack[item]

    def Backpack_Clear_Item(self, item):
        del self.Backpack[item]

    def Backpack_Clear_Parent(self, parent):
        for item in list(self.Backpack.keys()):
            pack = self.Backpack[item]
            if parent in pack:
                del pack[parent]
                if not pack: del self.Backpack[item]
    
    def Closet_Clear(self, slot):
        setattr(self.Closet, slot, "")
    
    def Closet_Hand(self, slot, name, dh1, dh2):
        if slot == "Hand_1": self.Closet.Hand_1 = name
        elif slot == "Hand_2": self.Closet.Hand_2 = name

        if self.Closet.Hand_1 == name and "Two-handed" in dh1.prop:
            self.Closet.Hand_2 = "Grip"
            return
        if self.Closet.Hand_2 == "Grip":
            if self.Closet.Hand_1 != name or ("Two-handed" not in dh1.prop and "Versatile" not in dh1.prop):
                self.Closet.Hand_2 = ""
        if "Versatile" in dh1.prop and self.Closet.Hand_2 == self.Closet.Hand_1:
            self.Closet.Hand_2 = "Grip"
        if slot == "Hand_2" and "Two-handed" in dh1.prop:
            self.Closet.Hand_2 = ""

    def Closet_Armor(self, slot, name, data):
        pass 

    def to_dict(self):
        return {
            "Closet": self.Closet.to_dict(),
            "Backpack": self.Backpack,
        }

        

class m_Caster:
    def __init__(self, db, data):
        self.db = db
        self.Max_Spell_Level = data["Max_Spell_Level"]
        self.Cantrips_Available = data["Cantrips_Available"]
        self.Cantrips_Known = data["Cantrips_Known"]
        self.Spells_Available = data["Spells_Available"]
        self.Spells_Known = data["Spells_Known"]
        self.Prepared_Type = data["Prepared_Type"]
        self.Prepared_Available = data["Prepared_Available"]
        self.Spells_Prepared = data["Spells_Prepared"]
        self.Toggle = data["Toggle"]
        self.Abil = data["Abil"]
        self.Caster_List = data["Caster_List"]
        self.Book = data["Book"]
        self.Prepared = data["Prepared"]
        self.Slot = data["Slot"]
        self.DC = data["DC"]
        self.ATK = data["ATK"]
        
    def Transfer(self, parent):
        keys = ("Max_Spell_Level","Cantrips_Available","Cantrips_Known", "Spells_Available", "Spells_Known", "Prepared_Type", "Prepared_Available", "Spells_Prepared", "Abil","Caster_List","Book","Prepared","Slot","DC","ATK")
        r = parent
        self.Toggle = r.Toggle

        for k in keys: setattr(self, k, getattr(r, k) if self.Toggle else None)

    def return_current(self, mode):
        if mode == "SK":  return self.Spells_Known
        if mode == "SP":  return self.Spells_Prepared
        if mode == "CK": return self.Cantrips_Known
        return 0

    def Max_Check(self, Spell, Level, Lookup, Current, Max):
        target = self.Book[Level] if Lookup == "B" else self.Prepared[Level]
        
        if Spell in target:
            target.remove(Spell)
            return
        
        c = self.return_current(Current)
        m = {"SA": self.Spells_Available, "CA": self.Cantrips_Available, "PA": self.Prepared_Available}[Max]
        if c < m: target.append(Spell)
        
    def to_dict(self):
        return {
            "Max_Spell_Level": self.Max_Spell_Level,
            "Cantrips_Available": self.Cantrips_Available,
            "Cantrips_Known": self.Cantrips_Known,
            "Spells_Available": self.Spells_Available,
            "Spells_Known": self.Spells_Known,
            "Prepared_Type": self.Prepared_Type,
            "Prepared_Available": self.Prepared_Available,
            "Spells_Prepared": self.Spells_Prepared,
            "Toggle": self.Toggle,
            "Abil": self.Abil,
            "Caster_List": self.Caster_List,
            "Book": self.Book,
            "Prepared": self.Prepared,
            "Slot": self.Slot,
            "DC": self.DC,
            "ATK": self.ATK,
        }

class m_Core:
    def __init__(self, db, data):
        self.Level = data["Level"]
        self.Race = data["Race"]
        self.Subrace = data["Subrace"]
        self.Class = data["Class"]
        self.Subclass = data["Subclass"]
        self.Background = data["Background"]

    @property
    def PB(self):
        return d_pb[self.Level]

    def Sit_Level(self, val):
        math = max(1, min(int(self.Level + val), 20))
        self.Level = math
        
    def Sit_Gen(self, cat, val):
        setattr(self, cat, val)
    
    def Sit_Race(self, val):
        self.Race = val
        self.Subrace = ""
        
    def Sit_Class(self, val):
        self.Class = val
        self.Subclass = ""
    
    def to_dict(self):
        return {
            "Level": self.Level,
            "Race": self.Race,
            "Subrace": self.Subrace,
            "Class": self.Class,
            "Subclass": self.Subclass,
            "Background": self.Background
        }

class m_Atr:
    def __init__(self, db, data):
        self.STR = s_Atr(data["STR"])
        self.DEX = s_Atr(data["DEX"])
        self.CON = s_Atr(data["CON"])
        self.INT = s_Atr(data["INT"])
        self.WIS = s_Atr(data["WIS"])
        self.CHA = s_Atr(data["CHA"])
    
    def Sit(self, stat, cat, val):
        getattr(self, stat).Sit(cat, val)

    def View(self):
        return {
            "STR": self.STR,
            "DEX": self.DEX,
            "CON": self.CON,
            "WIS": self.WIS,
            "INT": self.INT,
            "CHA": self.CHA
        }

    def to_dict(self):
        return {
            "STR": self.STR.to_dict(),
            "DEX": self.DEX.to_dict(),
            "CON": self.CON.to_dict(),
            "INT": self.INT.to_dict(),
            "WIS": self.WIS.to_dict(),
            "CHA": self.CHA.to_dict()
        }

class m_Vision:
    def __init__(self, db, data):
        self.Dark = s_Vision(data["Dark"])
        self.Blind = s_Vision(data["Blind"])
        self.Tru = s_Vision(data["Tru"])
        self.Tremor = s_Vision(data["Tremor"])

    def Sit(self, item, cat, val):
        getattr(self, item).Sit(cat, val)
    
    def View(self):
        return {
            "Dark": self.Dark,
            "Blind": self.Blind,
            "Tru": self.Tru,
            "Tremor": self.Tremor
        }
        
    def to_dict(self):
        return {
            "Dark": self.Dark.to_dict(),
            "Blind": self.Blind.to_dict(),
            "Tru": self.Tru.to_dict(),
            "Tremor": self.Tremor.to_dict()
        }

class m_Speed:
    def __init__(self, db, data):
        self.Walk = s_Speed(data["Walk"])
        self.Fly = s_Speed(data["Fly"])
        self.Swim = s_Speed(data["Swim"])
        self.Climb = s_Speed(data["Climb"])
        self.Burrow = s_Speed(data["Burrow"])

    def Sit(self, item, cat, val):
        getattr(self, item).Sit(cat, val)

    def View(self):
        return {
            "Walk": self.Walk,
            "Fly": self.Fly,
            "Swim": self.Swim,
            "Climb": self.Climb,
            "Burrow": self.Burrow
        }
    def to_dict(self):
        return {
            "Walk": self.Walk.to_dict(),
            "Fly": self.Fly.to_dict(),
            "Swim": self.Swim.to_dict(),
            "Climb": self.Climb.to_dict(),
            "Burrow": self.Burrow.to_dict()
        }

class m_Prof:
    def __init__(self, db, data):
        self.Armor = s_Prof(data["Armor"])
        self.Weapon = s_Prof(data["Weapon"])
        self.Tool = s_Prof(data["Tool"])
        self.Lang = s_Prof(data["Lang"])

    def Sit(self, item, cat, val):
        getattr(self, item).Sit(cat, val)

    def Clear(self, item, cat):
        getattr(self, item).Clear(cat)

    def View(self):
        return {
            "Armor": self.Armor,
            "Weapon": self.Weapon,
            "Tool": self.Tool,
            "Lang": self.Lang
        }

    def to_dict(self):
        return {
            "Armor": self.Armor.to_dict(),
            "Weapon": self.Weapon.to_dict(),
            "Tool": self.Tool.to_dict(),
            "Lang": self.Lang.to_dict()
        }

class m_Skill:
    def __init__(self, db, data):
        self.Acrobatics = s_Skill(db, "DEX", data["Acrobatics"])
        self.Animal_Handling = s_Skill(db, "WIS", data["Animal Handling"])
        self.Arcana = s_Skill(db, "INT", data["Arcana"])
        self.Athletics = s_Skill(db, "STR", data["Athletics"])
        self.Deception = s_Skill(db, "CHA", data["Deception"])
        self.History = s_Skill(db, "INT", data["History"])
        self.Insight = s_Skill(db, "WIS", data["Insight"])
        self.Intimidation = s_Skill(db, "CHA", data["Intimidation"])
        self.Investigation = s_Skill(db, "INT", data["Investigation"])
        self.Medicine = s_Skill(db, "WIS", data["Medicine"])
        self.Nature = s_Skill(db, "INT", data["Nature"])
        self.Perception = s_Skill(db, "WIS", data["Perception"])
        self.Performance = s_Skill(db, "CHA", data["Performance"])
        self.Persuasion = s_Skill(db, "CHA", data["Persuasion"])
        self.Religion = s_Skill(db, "INT", data["Religion"])
        self.Sleight_Of_Hand = s_Skill(db, "DEX", data["Sleight of Hand"])
        self.Stealth = s_Skill(db, "DEX", data["Stealth"])
        self.Survival = s_Skill(db, "WIS", data["Survival"])

    def Sit(self, item, cat, key, val):
        getattr(self, item).Sit(cat, key, val)

    def Clear(self, item, cat):
        getattr(self, item).Clear(cat)

    def View(self):
        return {
            "Acrobatics": self.Acrobatics,
            "Animal Handling": self.Animal_Handling,
            "Arcana": self.Arcana,
            "Athletics": self.Athletics,
            "Deception": self.Deception,
            "History": self.History,
            "Insight": self.Insight,
            "Intimidation": self.Intimidation,
            "Investigation": self.Investigation,
            "Medicine": self.Medicine,
            "Nature": self.Nature,
            "Perception": self.Perception,
            "Performance": self.Performance,
            "Persuasion": self.Persuasion,
            "Religion": self.Religion,
            "Sleight of Hand": self.Sleight_Of_Hand,
            "Stealth": self.Stealth,
            "Survival": self.Survival
        }

    def to_dict(self):
        return {
            "Acrobatics": self.Acrobatics.to_dict(),
            "Animal Handling": self.Animal_Handling.to_dict(),
            "Arcana": self.Arcana.to_dict(),
            "Athletics": self.Athletics.to_dict(),
            "Deception": self.Deception.to_dict(),
            "History": self.History.to_dict(),
            "Insight": self.Insight.to_dict(),
            "Intimidation": self.Intimidation.to_dict(),
            "Investigation": self.Investigation.to_dict(),
            "Medicine": self.Medicine.to_dict(),
            "Nature": self.Nature.to_dict(),
            "Perception": self.Perception.to_dict(),
            "Performance": self.Performance.to_dict(),
            "Persuasion": self.Persuasion.to_dict(),
            "Religion": self.Religion.to_dict(),
            "Sleight of Hand": self.Sleight_Of_Hand.to_dict(),
            "Stealth": self.Stealth.to_dict(),
            "Survival": self.Survival.to_dict()
        }

class m_Condition:
    def __init__(self, db, data):
        self.Blinded = data["Blinded"]
        self.Charmed = data["Charmed"]
        self.Deafened = data["Deafened"]
        self.Frightened = data["Frightened"]
        self.Grappled = data["Grappled"]
        self.Incapacitated = data["Incapacitated"]
        self.Invisible = data["Invisible"]
        self.Paralyzed = data["Paralyzed"]
        self.Petrified = data["Petrified"]
        self.Poisoned = data["Poisoned"]
        self.Prone = data["Prone"]
        self.Restrained = data["Restrained"]
        self.Stunned = data["Stunned"]
        self.Unconscious = data["Unconscious"]
        self.Exhaustion = data["Exhaustion"]

    def Sit(self, item, val):
        setattr(self, item, val)

    def View(self):
        return self.to_dict()
    
    def to_dict(self):
        return {
            "Blinded": self.Blinded,
            "Charmed": self.Charmed,
            "Deafened": self.Deafened,
            "Frightened": self.Frightened,
            "Grappled": self.Grappled,
            "Incapacitated": self.Incapacitated,
            "Invisible": self.Invisible,
            "Paralyzed": self.Paralyzed,
            "Petrified": self.Petrified,
            "Poisoned": self.Poisoned,
            "Prone": self.Prone,
            "Restrained": self.Restrained,
            "Stunned": self.Stunned,
            "Unconscious": self.Unconscious,
            "Exhaustion": self.Exhaustion
        }

class m_HP:
    def __init__(self, db, data):
        self.db = db
        self.Temp = data["Temp"]
        self.Player = data["Player"]
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]
        self.Current = data["Current"]

    def Sit(self, item, val):
        setattr(self, item, int(val))

    @property
    def Max(self):
        L = self.db.Core.Level
        con = self.db.Atr.CON.Mod
        return self.Player + self.Race + self.Class + self.Milestone + L * con

    def View(self):
        return self.to_dict()

    def to_dict(self):
        return {
            "Temp": self.Temp,
            "Player": self.Player,
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone,
            "Current": self.Current
        }

class m_HD:
    def __init__(self, db, data):
        self.db = db
        self.Val = data["Val"]
        self.Current = data["Current"]

    def Sit(self, item, val):
        setattr(self, item, int(val))

    @property
    def Max(self):
        return self.db.Core.Level

    def View(self):
        return self.to_dict()
        
    def to_dict(self):
        return {
            "Val": self.Val,
            "Current": self.Current,
            "Max": self.Max,
        }

class m_Race:
    def __init__(self, db, data):
        self.Features = data["Features"]

    def Sit_Spell(self, item, index , inp):
        self.Features[item]["Spells"][index][0] = inp
        
    def to_dict(self):
        return {"Features": self.Features}

class m_Class:
    def __init__(self, db, data):
        self.db = db
        self.Features = data["Features"]
        self.Skill = s_Class_Skill(db, data["Skill"])
    
    def Skill_Select(self, idx, inp): 
        self.Skill.Sit_Select(idx, inp)
        
    def Skill_Clear(self): 
        length = len(self.Skill.Select)
        self.Skill.Select = [""]*length

    def Familiar_Update(self, key, num):
        ward_data = self.Features[key]["HP"]
        new_hp = ward_data["Current"] + num
        ward_data["Current"] = max(0, min(new_hp, ward_data["Max"]))


    def to_dict(self):
        return {
            "Features": self.Features,
            "Skill": self.Skill.to_dict()
        }

class s_Background_Feature:
    def __init__(self, data):
        self.Name = data["Name"]
        self.Desc = data["Desc"]
    
    def Sit(self, name, desc):
        self.Name = name
        self.Desc = desc

    def Clear(self):
        self.Name = ""
        self.Desc = ""
    def to_dict(self):
        return {
            "Name": self.Name,
            "Desc": self.Desc
        }

class s_Background_Selects:
    def __init__(self, data):
        self.Select = data["Select"]
        self.Options = data["Options"]

    def Sit(self, select, options):
        self.Select = select
        self.Options = options
    
    def Clear(self):
        self.Select = ""
        self.Options = []

    def to_dict(self):
        return {
            "Select": self.Select,
            "Options": self.Options
        }


class m_Background:
    def __init__(self, db, data):
        self.db = db
        self.Features = s_Background_Feature(data["Features"])
        self.Tool  = s_Background_Selects(data["Tool"])
        self.Lang = s_Background_Selects(data["Lang"])
        
    def Sit_Features(self, Name, Desc): self.Features.Sit(Name, Desc)
    def Sit_Tool(self, Select, options): self.Tool.Sit(Select, options)
    def Sit_Lang(self, Select, options): self.Lang.Sit(Select, options)


    def Clear(self):
        self.Features.Clear()
        self.Tool.Clear()
        self.Lang.Clear()
    def Clear_Tool(self): self.Tool.Clear()
    def Clear_Lang(self): self.Lang.Clear()
    def to_dict(self):
        return {
            "Features": self.Features.to_dict(),
            "Tool": self.Tool.to_dict(),
            "Lang": self.Lang.to_dict()
        }

class m_Initiative:
    def __init__(self, db, data):
        self.db = db
        self.Race = data["Race"]
        self.Class = data["Class"]
        self.Milestone = data["Milestone"]

    def Sit(self, cat, val):
        setattr(self, cat, int(val))

    @property
    def Val(self):
        return self.Race + self.Class + self.Milestone

    def View(self):
        return self.to_dict()
        
    def to_dict(self):
        return {
            "Race": self.Race,
            "Class": self.Class,
            "Milestone": self.Milestone
        }

# --- Database ---

class Database:
    def __init__(self):
        with open(get_path("Dist", "db.json"), "r") as f:
            sheet = json.load(f)

        self.Core = m_Core(self, sheet["Core"])
        self.Atr = m_Atr(self, sheet["Atr"])
        self.Initiative = m_Initiative(self, sheet["Initiative"])
        self.Vision = m_Vision(self, sheet["Vision"])
        self.Speed = m_Speed(self, sheet["Speed"])
        self.Prof = m_Prof(self, sheet["Prof"])
        self.Skill = m_Skill(self, sheet["Skill"])
        self.Condition = m_Condition(self, sheet["Condition"])
        self.HP = m_HP(self, sheet["HP"])
        self.HD = m_HD(self, sheet["HD"])
        self.Race = m_Race(self, sheet["Race"])
        self.Class = m_Class(self, sheet["Class"])
        self.Caster = m_Caster(self, sheet["Caster"])
        self.Background = m_Background(self, sheet["Background"])
        self.Inventory = m_Inventory(self, sheet["Inventory"])

    def Clear_Background_Globals(self):
        for item in ("Armor", "Weapon", "Tool", "Lang"):
            self.Prof.Clear(item, "Background")

        for name in vars(self.Skill).keys():
            self.Skill.Clear(name, "Background")
        
        self.Background.Clear()
            

    def Clear_Class_Globals(self):
        for item in ("Dark", "Blind", "Tru", "Tremor"):
            self.Vision.Sit(item, "Class", 0)

        for item in ("Walk", "Fly", "Swim", "Climb", "Burrow"):
            self.Speed.Sit(item, "Class", 0)

        self.Initiative.Sit("Class", 0)
        self.HP.Sit("Class", 0)

        for item in ("Armor", "Weapon", "Tool", "Lang"):
            self.Prof.Clear(item, "Class")

        for name in vars(self.Skill).keys():
            self.Skill.Clear(name, "Class")


    def Clear_Race_Globals(self):
        for item in ("Dark", "Blind", "Tru", "Tremor"):
            self.Vision.Sit(item, "Race", 0)

        for item in ("Walk", "Fly", "Swim", "Climb", "Burrow"):
            self.Speed.Sit(item, "Race", 0)

        self.Initiative.Sit("Race", 0)
        self.HP.Sit("Race", 0)

        for item in ("Armor", "Weapon", "Tool", "Lang"):
            self.Prof.Clear(item, "Race")

        for name in vars(self.Skill).keys():
            self.Skill.Clear(name, "Race")

    @property
    def Save_out(self):
        sheet = {
            "Core": self.Core.to_dict(),
            "Atr": self.Atr.to_dict(),
            "Vision": self.Vision.to_dict(),
            "Speed": self.Speed.to_dict(),
            "Initiative": self.Initiative.to_dict(),
            "HP": self.HP.to_dict(),
            "HD": self.HD.to_dict(),
            "Prof": self.Prof.to_dict(),
            "Skill": self.Skill.to_dict(),
            "Race": self.Race.to_dict(),
            "Class": self.Class.to_dict(),
            "Background": self.Background.to_dict(),
            "Caster": self.Caster.to_dict(),
            "Condition": self.Condition.to_dict(),
            "Inventory": self.Inventory.to_dict()
        }
        
        with open(get_path("Dist", "db.json"), "w") as f:
            json.dump(sheet, f, indent=4)