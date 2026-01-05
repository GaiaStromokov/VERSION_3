from Utils.UI.f_Utility import *
import q

Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing

dict_struct = {
    "Weapon": [["Simple", "Melee"], ["Simple", "Ranged"], ["Martial", "Melee"], ["Martial", "Ranged"]],
    "Armor": ["Light", "Medium", "Heavy", "Shield"]
}

class pat_Bazaar:
    def __init__(self):
        pass

    @property
    def w(self):
        return q.w
    def create_bazaar_button(self, item, category_type, parent):
        button_tag = Tag.bazaar.button(item.id)
        tooltip_tag = Tag.bazaar.tooltip(item.id)
        add_button(label=item.base_name, width=sz.Item.w, user_data=[category_type, item.id], callback=q.cbh.Bazaar_Add_Item, tag=button_tag, parent=parent)
        with tooltip(button_tag, tag=tooltip_tag):
            item_detail_handler(item.id)

    def get_items_for_category(self, rank, slot, category_data):
        if isinstance(category_data, list):
            items = self.w.search(Tier=rank, Slot=slot, Cat=category_data)
            label = f"{category_data[0]} {category_data[1]}"
        else:
            items = self.w.search(Tier=rank, Slot=slot, Cat=category_data)
            label = category_data

        items.sort(key=lambda x: x.id)
        return label, items

    def rebuild_category(self, Type, Category, Rarity, t_Parent):
        icl(t_Parent)

        with group(parent=t_Parent):
            for cData in Category:
                label, items = self.get_items_for_category(Rarity, Type, cData)
                if not items:
                    continue

                add_separator(label=label)
                for i in range(0, len(items), 4):
                    with group(horizontal=True):
                        h_group = last_item() 
                        chunk = items[i:i+4]
                        for item in chunk: self.create_bazaar_button(item, Type, parent=h_group)

    def Refresh(self):
        for Type, Category in dict_struct.items():
            for rarity in range(5):
                Rank = Rules.g_Item_Rarity(rarity) 
                t_Parent = Tag.bazaar.window(Type, Rank)
                if does_item_exist(t_Parent): self.rebuild_category(Type, Category, rarity, t_Parent)