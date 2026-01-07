from Utils.UI.f_Utility import *
import q

Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing
dict_struct = {
    "Weapon": [["Weapon", "Simple", "Melee"], ["Weapon", "Simple", "Ranged"], ["Weapon", "Martial", "Melee"], ["Weapon", "Martial", "Ranged"]],
    "Armor": [["Armor", "Light"], ["Armor", "Medium"], ["Armor", "Heavy"], ["Armor", "Shield"]]
}

struct_list = {
    "Weapon": ["Simple Melee", "Simple Ranged", "Martial Melee", "Martial Ranged"],
    "Armor": ["Light", "Medium", "Heavy", "Shield"]
}

class pat_Bazaar:
    def __init__(self):
        pass



    def create_bazaar_button(self, iid, parent, rank):
        label = iid.rsplit('_', 1)[0] if rank > 0 else iid
        
        button_tag = Tag.bazaar.button(iid)
        tooltip_tag = Tag.bazaar.tooltip(iid)
        
        add_button(label=label, width=sz.Item.w, user_data=[iid], callback=q.cbh.Bazaar_Add_Item, tag=button_tag, parent=parent)
        with tooltip(button_tag, tag=tooltip_tag):
            item_detail_handler(iid)

    def get_items_for_category(self, rank, cat_list):
        items = q.itm.Search([rank], cat_list)
        items.sort()
        return items

    def rebuild_category(self, categories, labels, Rarity, t_Parent):
        icl(t_Parent)

        with group(parent=t_Parent):
            for cat_list, label in zip(categories, labels):
                items = self.get_items_for_category(Rarity, cat_list)
                
                if not items:
                    continue

                add_separator(label=label)
                for i in range(0, len(items), 4):
                    with group(horizontal=True):
                        h_group = last_item() 
                        chunk = items[i:i+4]
                        for iid in chunk: 
                            self.create_bazaar_button(iid, h_group, Rarity)

    def Refresh(self):
        for Type in dict_struct.keys():
            cats = dict_struct[Type]
            labels = struct_list[Type]

            for rarity in [0,1,2,3]:
                Rank = Rules.g_Item_Rarity(rarity) 
                t_Parent = Tag.bazaar.window(Type, Rank)
                
                if does_item_exist(t_Parent): 
                    self.rebuild_category(cats, labels, rarity, t_Parent)