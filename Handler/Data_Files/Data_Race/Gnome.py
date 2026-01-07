import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

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

Gnome_Catalog = {
    "Base": Gnome,
    "Forest": Gnome_Forest,
    "Rock": Gnome_Rock
}