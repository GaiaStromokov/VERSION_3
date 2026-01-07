from Utils.UI.f_Utility import *
import q
Tag = q.Tag


class Current:
    def __init__(self):
        pass

    @property
    def itm(self):
        return q.itm
    
    @property
    def Closet(self):
        return q.dbm.db.Inventory.Closet

    @property
    def Hand_1(self):
        return self.itm.get(self.Closet.Hand_1)

    @property
    def Hand_2(self):
        return self.itm.get(self.Closet.Hand_2)

    @property
    def Armor(self):
        return self.itm.get(self.Closet.Armor)

class pat_Closet:
    def __init__(self):
        self.Current = Current()

    @property
    def itm(self): return q.itm

    @property
    def db(self): return q.dbm.db

    @property
    def Backpack(self): return set(q.dbm.db.Inventory.Backpack.keys())

    @property
    def Closet(self): return q.dbm.db.Inventory.Closet
    
    def Refresh(self):
        owned = self.Backpack

        for slot, cat in [("Armor", "Primary"), ("Hand_1", "Main"), ("Hand_2", "Off")]:
            opts = sorted(owned.intersection(self.itm.map_cat.get(cat, set())))
            configure_item(Tag.closet.select(slot), items=opts, default_value=getattr(self.Closet, slot))