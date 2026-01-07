import q, re, math
from Handler.Utils.funcs import *
from Handler.bRace import tRace, tFeature

class Empty(tRace):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = []

Empty_Catalog = {
    "Base": Empty
}