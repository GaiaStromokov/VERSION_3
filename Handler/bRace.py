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
        from Handler.Cataloges.Race_Catalog import Race_Catalog
        self.db.Clear_Race_Globals()
        if self.R not in Race_Catalog: return
        Group = Race_Catalog[self.R]
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