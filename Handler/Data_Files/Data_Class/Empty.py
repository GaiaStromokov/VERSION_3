from Handler.bClass import tClass

class Empty(tClass):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = []

class EMP_BAS_Empty(Empty):
    def __init__(self, mgr):
        super().__init__(mgr)
        self.Feature_List = []

Empty_Catalog = {
    "Base": Empty,
}