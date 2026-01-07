import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Human(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.db.Speed.Walk.Sit("Race", 30)
        self.db.Prof.Lang.Sit("Race", ["Common"])
        self.Feature_List = []

Human_Catalog = {
    "Base": Human
}