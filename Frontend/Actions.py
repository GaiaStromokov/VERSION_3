from Utils.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing


class pat_Actions:
    def __init__(self):
        pass
    
    @property
    def Hands(self): 
        d = q.dbm.db.Inventory.Closet
        d1 = q.itm.get(d.Hand_1)
        d2 = q.itm.get(d.Hand_2)
        return [d1, d2]

    def Refresh(self):
        self.Weapon()

    def Weapon(self):
        for j in Rules.l.Weapon_Atr:
            delete_item(Tag.block.actions.cell(j,0), children_only=True)
            delete_item(Tag.block.actions.cell(j,1), children_only=True)

        hands = self.Hands
        
        for idx, hand in enumerate(hands):
            print(idx, hand)
            if idx == 1:
                if hand.base_name == "Grip": continue

            Roll = hand.Roll
            if idx == 0 and "Versatile" in hand.prop and hands[1].base_name == "Grip":
                Roll = hand.vRoll

            if "Weapon" in hand.cat: self.actions_weapon(hand, idx, Roll)


    def actions_weapon(self, cdata, idx, Roll):
        with group(parent=Tag.block.actions.cell("Name", idx)):add_text(cdata.id)
        with group(parent=Tag.block.actions.cell("Range", idx)): add_text(cdata.Range)
        with group(parent=Tag.block.actions.cell("Hit", idx)):
            with group(horizontal=True):
                add_text(f"{cdata.Hit:+}")

        with group(parent=Tag.block.actions.cell("Damage", idx)):
            with group(horizontal=True):
                add_text(f"{Roll} {cdata.Dam:+}")


        with group(parent=Tag.block.actions.cell("Type", idx)):
            add_text(cdata.dType, tag=Tag.block.actions.text("Type", idx))
            # idel(Tag.block.actions.tooltip("Type", idx))
            # with tooltip(Tag.block.actions.text("Type", idx), tag=Tag.block.actions.tooltip("Type", idx)):
            #     if cdata.dType:
            #         add_text(get.dict_weapon_dtype_description[cdata.dType])

        with group(parent=Tag.block.actions.cell("Notes", idx)):
            with group(horizontal=True):
                for prop in cdata.prop:
                    t_text = Tag.block.actions.text("wprop", prop, idx)
                    t_tooltip = Tag.block.actions.tooltip("wprop", prop, idx)
                    # if prop == "Special": sc = get.dict_weapon_prop["Special"]["SC"]; desc = get.dict_weapon_prop["Special"][cdata.Name]
                    # else: sc = get.dict_weapon_prop[prop]["SC"]; desc = get.dict_weapon_prop[prop]["Desc"]
                    add_text(prop, tag=t_text)
                    idel(t_tooltip)
                    with tooltip(t_text, tag=t_tooltip):
                        add_text(prop, color=Coler.Header.G)
                        # add_text(desc, wrap=240)

                        

    # def actions_shield(self, cdata, idx):
    #     with group(parent=tag.wactions.cell("Name", idx)):add_text(cdata.Name)
    #     with group(parent=tag.wactions.cell("Range", idx)): add_text("")
    #     with group(parent=tag.wactions.cell("Hit", idx)): add_text("")
    #     with group(parent=tag.wactions.cell("Damage", idx)): add_text(f"AC: {cdata.AC}")
    #     with group(parent=tag.wactions.cell("Type", idx)): add_text("")
    #     with group(parent=tag.wactions.cell("Notes", idx)): add_text("")

