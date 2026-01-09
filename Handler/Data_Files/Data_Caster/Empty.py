from Handler.bCaster import tCaster

class Empty(tCaster):
    def __init__(self, mgr):
        super().__init__(mgr)

    def Run(self):
        self.Toggle = False

Empty_Catalog = {
    "Base": Empty,
}
