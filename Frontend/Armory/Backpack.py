from Utils.UI.f_Utility import *
import q

Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing


t_table = Tag.backpack.table()
class pat_Backpack():
    def __init__(self):
        pass
    
    @property
    def w(self): return q.w

    @property
    def db(self): return q.dbm.db

        
    @property
    def Backpack(self): return q.dbm.db.Inventory.Backpack
    
    
    def Refresh(self):
        self.fill_backpack()
        self.populate_backpack()
        
    def fill_backpack(self):
        backpack = self.Backpack
        item_count = len(backpack)
        
        existing_rows = 0
        while does_item_exist(Tag.backpack.row(existing_rows)):
            existing_rows += 1

        for idx in range(existing_rows, item_count):
            with table_row(parent=t_table, tag=Tag.backpack.row(idx)):
                add_table_cell(tag=Tag.backpack.cell("name", idx))
                add_table_cell(tag=Tag.backpack.cell("slot", idx))
                add_table_cell(tag=Tag.backpack.cell("qty", idx))
                add_table_cell(tag=Tag.backpack.cell("weight", idx))
                add_table_cell(tag=Tag.backpack.cell("cost", idx))

        for idx in range(item_count, existing_rows):
            delete_item(Tag.backpack.row(idx))

    def populate_backpack(self):
        
        backpack = self.Backpack
        
        for idx, item in enumerate(backpack):
            print(idx, item)
            cdata = q.w.get(item)
            qty = backpack[item][1]
            weight = 0
            cost = 0
            
            icl(Tag.backpack.cell("name", idx))
            icl(Tag.backpack.cell("slot", idx))
            icl(Tag.backpack.cell("qty", idx))
            icl(Tag.backpack.cell("weight", idx))
            icl(Tag.backpack.cell("cost", idx))
            
            # Populate cells
            add_text(item.replace("_", " "), parent=Tag.backpack.cell("name", idx))
            
            idel(Tag.backpack.tooltip(idx))
            with tooltip(Tag.backpack.cell("name", idx), tag=Tag.backpack.tooltip(idx)):
                item_detail_handler(item)
                
            add_text(cdata.Slot, parent=Tag.backpack.cell("slot", idx))
            
            with group(horizontal=True, parent=Tag.backpack.cell("qty", idx)):
                add_text(qty, tag=Tag.backpack.text(item, idx))
                add_button(label="<", callback=q.cbh, user_data=["Backpack_Mod_Item", item, -1], small=True)
                add_button(label=">", callback=q.cbh, user_data=["Backpack_Mod_Item", item, 1], small=True)
                add_button(label="X", callback=q.cbh, user_data=["Backpack_Clear_Item", item], small=True)

            add_text(weight, parent=Tag.backpack.cell("weight", idx))
            add_text(cost, parent=Tag.backpack.cell("cost", idx))