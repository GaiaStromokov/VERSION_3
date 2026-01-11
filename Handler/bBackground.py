import q
from Handler.Utils.funcs import *

class bBackground:
    def __init__(self):
        self.Mode = "Refresh"

    @property
    def dbm(self): return q.dbm

    @property
    def db(self): return q.dbm.db

    @property
    def BG(self): return q.dbm.db.Core.Background

    def Startup(self):
        if not self.BG: return
        self.Refresh_Background_Data()

    def Refresh(self):
        if not self.BG: return
        self.Mode = "Refresh"
        self.Refresh_Background_Data()

    def New(self):
        if not self.BG: return
        self.Mode = "New"
        self.Refresh_Background_Data()

    def Refresh_Background_Data(self):
        from Handler.Cataloges.Background_Catalog import Background_Catalog
        self.db.Clear_Background_Globals()
        if self.BG not in Background_Catalog: return
        Actor = Background_Catalog[self.BG]
        instance = Actor(self)
        instance.Run()

class tBackground:
    def __init__(self, mgr):
        self.bBackground = mgr

    @property
    def db(self): return q.dbm.db

    def Skill(self, items):
        for name in items:
            self.db.Skill.Sit(name, "Background", 0, True)

    def Tool(self, items):
        for name in items:
            self.db.Prof.Tool.Sit("Background", name)

    def Lang(self, items):
        for name in items:
            self.db.Prof.Lang.Sit("Background", name)

    def Tool_Select(self, items, qty):
        Mode = self.bBackground.Mode
        
        if Mode == "New":
            self.db.Background.Sit_Tool([""] * qty, items)
        
        if Mode == "Refresh":
            past = self.db.Background.Tool.Select
            Selects = (past + [""] * qty)[:qty]
            self.db.Background.Sit_Tool(Selects, items)
            
            for tool in Selects:
                if tool:
                    self.db.Prof.Tool.Sit("Background", tool)

    def Lang_Select(self, items, qty):
        Mode = self.bBackground.Mode
        
        if Mode == "New":
            self.db.Background.Sit_Lang([""] * qty, items)
        
        if Mode == "Refresh":
            past = self.db.Background.Lang.Select
            Selects = (past + [""] * qty)[:qty]
            self.db.Background.Sit_Lang(Selects, items)
            
            for lang in Selects:
                if lang:
                    self.db.Prof.Lang.Sit("Background", lang)

    def Features(self, data):
        self.db.Background.Sit_Features(data["Name"], data["Desc"])

    def Run(self):
        pass