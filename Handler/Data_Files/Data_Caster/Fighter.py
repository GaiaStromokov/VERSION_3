from Handler.bCaster import tCaster

class Fighter_Eldritch_Knight(tCaster):
    def __init__(self, mgr):
        super().__init__(mgr)

    def Run(self):
        self.Abil = "INT"
        self.Caster_List = "Wizard"
        self.Prepared_Type = "None"

        self.Max_Spell_Level = [0,0,0,1,1,1,1,2,2,2,2,2,2,3,3,3,3,3,3,4,4][self.L]
        self.Cantrips_Available  = [0,0,0,2,2,2,2,2,2,2,3,3,3,3,3,3,3,3,3,3,3][self.L]
        self.Spells_Available  = [0,0,0,3,4,4,4,5,6,6,7,8,8,9,10,10,11,11,12,13,13][self.L]

        self.Slot_List = [
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,0,0,0,0,0,0,0,0,0],
            [0,2,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,3,0,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,2,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,0,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,2,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,0,0,0,0,0,0],
            [0,4,3,3,1,0,0,0,0,0],
            [0,4,3,3,1,0,0,0,0,0]
        ][self.L]

        self.Slot = [[False] * n for n in self.Slot_List]
        self.Toggle = True

Fighter_Catalog = {
    "Eldritch_Knight": Fighter_Eldritch_Knight,
}
