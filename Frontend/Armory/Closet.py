from dearpygui.dearpygui import configure_item
import q

Tag = q.Tag

class Current:
    def __init__(self):
        pass

    @property
    def w(self):
        return q.w
    
    @property
    def Closet(self):
        return q.dbm.db.Inventory.Closet

    @property
    def Hand_1(self):
        return self.w.get(self.Closet.Hand_1)

    @property
    def Hand_2(self):
        return self.w.get(self.Closet.Hand_2)

    @property
    def Armor(self):
        return self.w.get(self.Closet.Armor)

class pat_Closet:
    def __init__(self):
        self.Current = Current()

    @property
    def w(self): return q.w

    @property
    def db(self): return q.dbm.db

    @property
    def Backpack(self): return q.dbm.db.Inventory.Backpack

    @property
    def Closet(self): return q.dbm.db.Inventory.Closet
    
    def Refresh(self):
        backpack = self.Backpack

        opts = [k for k, v in backpack.items() if v[0] == "Armor"]
        opts.sort()
        configure_item(Tag.closet.select("Armor"), items=opts, default_value=self.Closet.Armor)

        opts = [k for k, v in backpack.items() if v[0] == "Weapon"]
        opts.sort()
        configure_item(Tag.closet.select("Hand_1"), items=opts, default_value=self.Closet.Hand_1)

        opts = [k for k, v in backpack.items() if v[0] in ["Weapon", "Shield"]]
        opts.sort()
            
        configure_item(Tag.closet.select("Hand_2"), items=opts, default_value=self.Closet.Hand_2)