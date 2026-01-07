from Utils.UI.f_Utility import *
import q

Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing

t_table = Tag.backpack.table()
class pat_Backpack():
    def __init__(self):
        self.slot_map = {"Main": "M", "Off": "O", "Armor": "A"}
    
    @property
    def itm(self): return q.itm

    @property
    def db(self): return q.dbm.db
        
    @property
    def Backpack(self): return q.dbm.db.Inventory.Backpack
    
    def Refresh(self):
        self.fill_backpack()
        self.populate_backpack()
        
    def fill_backpack(self):
        backpack = self.Backpack
        count = len(backpack)
        
        existing_rows = 0
        while does_item_exist(Tag.backpack.row(existing_rows)):
            existing_rows += 1

        for idx in range(existing_rows, count):
            with table_row(parent=t_table, tag=Tag.backpack.row(idx)):
                add_table_cell(tag=Tag.backpack.cell("name", idx))
                add_table_cell(tag=Tag.backpack.cell("slot", idx))
                add_table_cell(tag=Tag.backpack.cell("qty", idx))
                add_table_cell(tag=Tag.backpack.cell("weight", idx))
                add_table_cell(tag=Tag.backpack.cell("cost", idx))

        for idx in range(count, existing_rows):
            delete_item(Tag.backpack.row(idx))

    def populate_backpack(self):
        backpack = self.Backpack
        
        for idx, id in enumerate(backpack):
            cdata = self.itm.get(id)

            qty = backpack[id]
            
            weight = cdata.Weight * qty
            cost = cdata.Cost * qty
            
            slots = [self.slot_map[c] for c in cdata.cat if c in self.slot_map]
            slot_str = ", ".join(sorted(slots))
            
            icl(Tag.backpack.cell("name", idx))
            icl(Tag.backpack.cell("slot", idx))
            icl(Tag.backpack.cell("qty", idx))
            icl(Tag.backpack.cell("weight", idx))
            icl(Tag.backpack.cell("cost", idx))
            
            add_text(id, parent=Tag.backpack.cell("name", idx))
            
            idel(Tag.backpack.tooltip(idx))
            with tooltip(Tag.backpack.cell("name", idx), tag=Tag.backpack.tooltip(idx)):
                item_detail_handler(id)
                
            add_text(slot_str, parent=Tag.backpack.cell("slot", idx))
            
            with group(horizontal=True, parent=Tag.backpack.cell("qty", idx)):
                add_text(qty, tag=Tag.backpack.text(id, idx))
                add_button(label="<", user_data=[id], callback=q.cbh.Backpack_Sub_Item, small=True)
                add_button(label=">", user_data=[id], callback=q.cbh.Backpack_Add_Item, small=True)
                add_button(label="X", user_data=[id], callback=q.cbh.Backpack_Clear_Item, small=True)

            add_text(f"{weight:.2f}", parent=Tag.backpack.cell("weight", idx))
            add_text(f"{cost:.2f}", parent=Tag.backpack.cell("cost", idx))