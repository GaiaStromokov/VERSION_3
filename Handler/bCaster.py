
import q
from Handler.Utils.funcs import *

class bCaster:
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
        self.Refresh_Caster_Data()

    def Refresh(self):
        if not self.C: return
        self.Mode = "Refresh"
        self.Refresh_Caster_Data()

    def New(self):
        if not self.C: return
        self.Mode = "New"
        self.Refresh_Caster_Data()

    def Refresh_Caster_Data(self):
        from Handler.Cataloges.Caster_Catalog import Caster_Catalog

        Group = Caster_Catalog.get(self.C, Caster_Catalog["Empty"])
        Actor = Group.get(self.SC, Group.get("Base", Caster_Catalog["Empty"]["Base"]))

        instance = Actor(self)
        instance.execute()


class tCaster:
    def __init__(self, mgr):
        self.bCaster = mgr
        self.Mode = mgr.Mode
        self.Max_Spell_Level = None
        self.Cantrips_Available = None
        self.Spells_Available = None
        self.Cantrips_Known = None
        self.Spells_Known = None
        self.Prepared_Type = None
        self.Prepared_Available = None
        self.Spells_Prepared = None
        self.Toggle = None
        self.Abil = None
        self.Caster_List = None
        self.Book = [[] for _ in range(10)]
        self.Prepared = [[] for _ in range(10)]
        self.Slot = None
        self.DC = None
        self.ATK = None

    @property
    def empty_past(self):
        return [[] for _ in range(10)]

    @property
    def dbm(self): return q.dbm

    @property
    def db(self): return q.dbm.db

    @property
    def Atr_Mod(self):
        if self.Abil in q.Rules.l.Atr: return getattr(q.dbm.db.Atr, self.Abil).Mod
        return 0

    @property
    def L(self): return q.dbm.db.Core.Level

    @property
    def PB(self): return q.dbm.db.Core.PB

    @property
    def C(self): return q.dbm.db.Core.Class

    @property
    def Past_Slots(self):
        if self.db.Caster.Slot: return self.db.Caster.Slot
        return self.empty_past

    def execute(self):
        self.Run()

        if not self.Toggle:
            self.db.Caster.Transfer(self)
            return

        if self.Mode == "Refresh":
            self.Refresh_Caster_Data()

        self.Calculate()
        self.db.Caster.Transfer(self)

    def Calculate(self):
        if not self.Toggle: return
        mod = self.Atr_Mod
        calc = self.PB + mod
        self.DC  = 8 + calc
        self.ATK = f"{calc:+}"

        self.Prepared[0] = list(dict.fromkeys(self.Book[0]))

        if self.Prepared_Type == "None":
            self.Prepared_Available = 99999
            for i in range(1, 10):
                self.Prepared[i] = list(dict.fromkeys(self.Book[i]))

        if self.Prepared_Type == "Full":
            self.Prepared_Available = max(1, self.L + mod)
            for i in range(1, 10):
                self.Prepared[i] = [s for s in self.Prepared[i] if s in self.Book[i]]

        self.Cantrips_Known = len(self.Book[0])
        self.Spells_Known = sum(len(x) for x in self.Book[1:])
        self.Spells_Prepared = sum(len(self.Prepared[level]) for level in range(1, len(self.Prepared)))

    def Refresh_Caster_Data(self):
        past_data = self.db.Caster
        past_book = past_data.Book if past_data.Book else self.empty_past
        past_prepared = past_data.Prepared if past_data.Prepared else self.empty_past
        past_slot = past_data.Slot if past_data.Slot else self.empty_past

        Slot = self.empty_past
        for i in range(10):
            p_s = past_slot[i] if i < len(past_slot) else []
            s_s = self.Slot[i] if (self.Slot and i < len(self.Slot)) else []
            Slot[i] = (p_s + s_s)[:len(s_s)]
        self.Slot = Slot

        for i in range(10):
            current_set = set(self.Book[i])
            p_b = past_book[i] if i < len(past_book) else []
            for spell in p_b:
                if spell not in current_set:
                    self.Book[i].append(spell)

        for i in range(10):
            self.Prepared[i] = past_prepared[i] if i < len(past_prepared) else []

    def Run(self):
        pass
