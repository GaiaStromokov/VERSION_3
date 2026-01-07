import q, re, math
from Handler.Utils.funcs import *

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
        from Handler.Cataloges.Class_Catalog import Class_Catalog
        self.db.Clear_Class_Globals()
        if self.C not in Class_Catalog: return
        Group = Class_Catalog[self.C]
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