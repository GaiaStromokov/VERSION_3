import q
from Manager.Database import Database
from colorist import green, red
import inspect
import re
from Handler.Utils.Importer import bRace, bClass, bCaster 
from Frontend.Utils.Importer import pat_Sheet, pat_Race, pat_Class, pat_Caster, pat_Bazaar, pat_Closet, pat_Backpack, pat_Logger, pat_Actions

def register_callback(key):
    def wrapper(func):
        func._callback_key = key
        return func
    return wrapper

class Populate:
    def __init__(self, parent):
        self.dbm = parent
        self.S = pat_Sheet()
        self.R = pat_Race()
        self.C = pat_Class()
        self.Cas = pat_Caster()
        self.Bazaar = pat_Bazaar()
        self.Closet = pat_Closet()
        self.Backpack = pat_Backpack()
        self.Logger = pat_Logger()

        self._refresh_map = {
            "Sheet": self.S.All,
            "Race": self.R.Refresh,
            "Class": self.C.Refresh,
            "Caster": self.Cas.Refresh,
            "Condition": self.S.Condition,
            "Cast": self.Cas.Cast_Spell,
            "HP": self.S.Health,
            "Skill": self.S.Skill,
            "Bazaar": self.Bazaar.Refresh,
            "Closet": self.Closet.Refresh,
            "Backpack": self.Backpack.Refresh,
        }

    @property
    def db(self):
        return self.parent.db

    def update(self, *scopes):
        for scope in scopes:
            if method := self._refresh_map.get(scope):
                method()

    def fat(self):
        self.update("Sheet", "Race", "Class", "Caster", "Bazaar", "Closet", "Backpack")

    def Startup(self):
        self.fat()

    def Level(self):
        self.fat()

    def Race(self):
        self.update("Sheet", "Race")

    def Class(self):
        self.update("Sheet", "Class", "Caster")

    def Class_Skill(self):
        self.update("Sheet", "Class", "Caster", "Skill")
    
    def Caster(self):
        self.update("Caster")
    
    def Condition(self):
        self.update("Condition")

    def Caster_Cast(self):
        self.update("Cast")

    def Sheet(self):
        self.update("Sheet")
    
    def Inventory(self):
        self.update("Bazaar", "Closet", "Backpack")

class cb_Base:
    def __init__(self, parent):
        self.dbm = parent
        self.db = parent.db
        self.pat = parent.populate
        
        
        for name, func in inspect.getmembers(self, inspect.ismethod):
            if key := getattr(func, "_callback_key", None):
                self.dbm.Input_map[key] = func
                

    def atr_check(self, stat):
            lookup = self.db.Caster
            if lookup.Toggle and lookup.Abil == stat:
                self.dbm.Caster.Refresh() 
                self.pat.Caster()

class cb_Health(cb_Base):
    @register_callback("mod_HP")
    def mod_HP(self, sender, inp, udata):
        num = udata[0]
        self.db.HP.Sit("Current", num)
        self.pat.update("HP")

    @register_callback("mod_Temp")
    def mod_Temp(self, sender, inp, udata):
        num = udata[0]
        self.db.HP.Sit("Temp", num)
        self.pat.update("HP")

    @register_callback("mod_Base_HP")
    def mod_Base_HP(self, sender, inp, udata):
        self.db.HP.Sit("Player", inp)
        self.pat.update("HP")

class cb_Closet(cb_Base):
    @register_callback("Closet")
    def Closet_Dispatch(self, sender, inp, udata):
        pass
    
    def Clear(self):
        pass

    def Modify(self):
        pass

class cb_Rest(cb_Base):
    @register_callback("Rest")
    def Rest_Dispatch(self, sender, inp, udata):
        if inp == "Short": self.Short()
        elif inp == "Long": self.Long()
        self.pat.Sheet()

    def Short(self):
        pass

    def Long(self):
        pass

class cb_Condition(cb_Base):
    @register_callback("Condition")
    def Modify(self, sender, inp, udata):
        key = udata[0]
        self.db.Condition[key].Sit(inp)
        self.pat.Condition()

class cb_Core(cb_Base):
    @register_callback("mod_Level")
    def Level(self, sender, inp, udata):
        data = udata[0]
        self.db.Core.Sit_Level(data)
        if not self.dbm.Validate.Class: self.db.Core.Sit_Gen("Subclass", "")
        self.dbm.Race.Refresh()
        self.dbm.Class.Refresh()
        self.dbm.Caster.Refresh()
        self.pat.Level()

    @register_callback("mod_Race")
    def mod_Race(self, sender, inp, udata):
        if inp == self.db.Core.Race:
            return
        else:
            self.db.Core.Sit_Race(inp)
            self.dbm.Race.New()
            self.dbm.Caster.New()
            self.pat.Race()


    @register_callback("mod_Subrace")
    def mod_Subrace(self, sender, inp, udata):
        self.db.Core.Sit_Gen("Subrace", inp)
        self.dbm.Race.New()
        self.pat.Race()
        


    @register_callback("mod_Class")
    def mod_Class(self, sender, inp, udata):
        if inp == self.db.Core.Class:
            return
        else:
            self.db.Core.Sit_Class(inp)
            self.dbm.Class.New()
            self.dbm.Caster.New()
            self.pat.Class()

    @register_callback("mod_Subclass")
    def mod_Subclass(self, sender, inp, udata):
        self.db.Core.Sit_Gen("Subclass", inp)
        self.dbm.Class.New()
        self.dbm.Caster.New()
        self.pat.Class()

    @register_callback("mod_Background")
    def mod_Background(self, sender, inp, udata):
        self.db.Core.Sit_Gen("Background", inp)
        self.pat.Sheet()

class cb_Class(cb_Base):
    @register_callback("Class_F_Select")
    def Feature_Select(self, sender, inp, udata):
        key, index = udata
        self.db.Class.Features[key]["Select"][index] = inp
        self.dbm.Class.Refresh()
        self.pat.Class()

    @register_callback("Class_F_Use")
    def Feature_Use(self, sender, inp, udata):
        key, index = udata
        self.db.Class.Features[key]["Use"][index] = inp
        self.dbm.Class.Refresh()
        self.pat.Class()

    @register_callback("Class_S_Select")
    def Class_Select(self, sender, inp, udata):
        index = udata[0]
        self.db.Class.Skill.Select[index] = inp
        self.dbm.Class.Refresh()
        self.pat.Class_Skill()

    @register_callback("Class_S_Clear")
    def Skill_Clear(self, sender, inp, udata):
        self.db.Class.Skill_Clear()
        self.dbm.Class.Refresh()
        self.pat.Class_Skill()


    @register_callback("Familiar_Update")
    def Arcane_Ward(self, sender, inp, udata):
        key, num = udata
        self.db.Class.Familiar_Update(key, num)
        self.dbm.Class.Refresh()
        self.pat.Class()


class cb_Race(cb_Base):
    @register_callback("Race_Spell_Toggle")
    def Spell_Toggle(self, sender, inp, udata):
        item, index = udata
        self.db.Race.Sit_Spell(item, index, inp)
        self.pat.Race()
        
    @register_callback("Race_F_Select")
    def Feature_Select(self, sender, inp, udata):
        key, index = udata
        self.db.Race.Features[key]["Select"][index] = inp
        self.dbm.Race.Refresh()
        self.pat.Race()


    @register_callback("Race_F_Use")
    def Feature_Use(self, sender, inp, udata):
        key, index = udata
        self.db.Race.Sit_Use(key, index, inp)
        self.pat.Race()

    @register_callback("Race Asi")
    def mod_Asi(self, sender, inp, udata):
        stat = udata[0]
        self.db.Atr[stat].Sit("Race", inp)
        self.atr_check(stat)
        self.pat.Race()

class cb_Atr(cb_Base):
    @register_callback("Base_Atr")
    def Base(self, sender, inp, udata):
        stat = udata[0]
        getattr(self.db.Atr, stat).Sit("Base", inp)
        self.atr_check(stat)
        self.pat.Level()
        
class cb_Caster(cb_Base):    
    @register_callback("Spell_Cast")
    def Cast(self, sender, inp, udata):
        level = udata[0]
        slots = self.db.Caster.Slot[int(level)]
        for i in range(len(slots)):
            if not slots[i]:
                slots[i] = True
                break
        self.dbm.Caster.Refresh()
        self.pat.Caster()
    
    @register_callback("Spell_Learn")
    def Learn(self, sender, inp, udata):
        spell, level, spell_type = udata
        c, m = ("CK", "CA") if spell_type == "Cantrip" else ("SK", "SA")
        self.db.Caster.Max_Check(spell, level, "B", c, m)
        self.dbm.Caster.Refresh()
        self.pat.Caster()

    @register_callback("Spell_Prepare")
    def Prepare(self, sender, inp, udata):
        spell, level = udata
        self.db.Caster.Max_Check(spell, level, "P", "SP", "PA")
        self.dbm.Caster.Refresh()
        self.pat.Caster()


class cb_Inventory(cb_Base):
    @register_callback("Bazaar_Add_Item")
    def Bazaar_Add_Item(self, sender, inp, udata):
        cat, item = udata
        self.db.Inventory.Bazaar_Add_Item(cat, item)
        self.pat.Inventory()

    @register_callback("Backpack_Add_Item")
    def Backpack_Add_Item(self, sender, inp, udata):
        item = udata[0]
        self.db.Inventory.Backpack_Add_Item(item)
        self.pat.Inventory()

    @register_callback("Backpack_Sub_Item")
    def Backpack_Sub_Item(self, sender, inp, udata):
        item = udata[0]
        self.db.Inventory.Backpack_Add_Item(item)
        self.pat.Inventory()

    @register_callback("Backpack_Clear_Item")
    def Backpack_Clear_Item(self, sender, inp, udata):
        item = udata[0]
        self.db.Inventory.Backpack_Clear_Item(item)
        self.pat.Inventory()

    @register_callback("Closet_Mod")
    def Closet_Mod(self, sender, inp, udata):
        slot = udata[0]
        wdata = q.itm.get(inp)
        if slot == "Hand_1" or slot == "Hand_2": 
            dh1 = q.itm.get(self.db.Inventory.Closet.Hand_1)
            dh2 = q.itm.get(self.db.Inventory.Closet.Hand_2)
            self.db.Inventory.Closet_Hand(slot, inp, dh1, dh2)
        if slot == "Armor": self.db.Inventory.Closet_(slot, inp, wdata)
        # self.db.Inventory.Backpack_Clear_Item(item)
        # self.pat.Inventory()

    @register_callback("Closet_Clear")
    def Closet_Clear(self, sender, inp, udata):
        slot = udata[0]
        self.db.Inventory.Closet_Clear(slot)
        self.pat.Inventory()

        
class Validate:
    def __init__(self, parent):
        self.dbm = parent
        self.Vis = parent.Vis
    
    @property
    def Class(self):
        Class, Level = self.dbm.Vis.v_Class
        class_exception_map = {1: ["Cleric", "Warlock"], 2: ["Wizard"]}
        return Level >= 3 or Class in class_exception_map.get(Level, [])

class Vis:
    def __init__(self, parent):
        self.parent = parent
        self.db = parent.db
    
    @property
    def ad_Race(self):
        data = self.db.Core
        return data.Level, data.PB, data.Race, data.Subrace

    @property
    def ad_Class(self):
        data = self.db.Core
        return data.Level, data.PB, data.Class, data.Subclass

    @property
    def v_Class(self):
        data = self.db.Core
        return data.Class, data.Level

    @property
    def upd_Sheet(self):
        data = self.db.Core
        return (
            data.Level, 
            data.PB, 
            data.Race, 
            data.Subrace, 
            data.Class, 
            data.Subclass, 
            data.Background
        )

class Callback_Manager:
    def __init__(self, dbm):
        self.dbm = dbm

    def __getattr__(self, key):
        def _cb(sender, app_data, user_data):
            self.dbm.sit(key, sender, app_data, user_data)
        return _cb



class DBM:
    def __init__(self):
        self.db = Database()
        self.populate = Populate(self)
        self.Vis = Vis(self)
        self.Validate = Validate(self)
        
        self.Input_map = {}
        
        self.cb_closet = cb_Closet(self)
        self.cb_rest = cb_Rest(self)
        self.cb_health = cb_Health(self)
        self.cb_core = cb_Core(self)
        self.cb_condition = cb_Condition(self)
        self.cb_race = cb_Race(self)
        self.cb_class = cb_Class(self)
        self.cb_caster = cb_Caster(self)
        self.cb_atr = cb_Atr(self)
        self.cb_inventory = cb_Inventory(self)

        self.Race = bRace()
        self.Class = bClass()
        self.Caster = bCaster()

        self.cbh = Callback_Manager(self)

    @property
    def Save_out(self):
        self.db.Save_out
    
    @property
    def Startup(self):
        self.Race.Startup()
        self.Class.Startup()
        self.Caster.Startup()
        self.populate.Startup()

    def sit(self, key, sender, data, params):
        func = self.Input_map.get(key)
        if not callable(func):
            red(f"[DBM] Unknown/uncallable key: {key}")
            return
        self.populate.Logger.Log(f"Sit: key-{key}, sender-{sender}, data-{data}, params-{params}")
        func(sender, data, params)