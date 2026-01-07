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
        return [d.Hand_1, d.Hand_2]
    def Refresh(self):
        self.Weapon()

    def Weapon(self):
        for j in Rules.l.Weapon_Atr:
            delete_item(Tag.block.actions.cell(j,0), children_only=True)
            delete_item(Tag.block.actions.cell(j,1), children_only=True)

        hands = self.Hands

        for idx, hand in enumerate(hands):
            print(idx, hand)

        #     versatile = get.weapon_versatile()

        #     if idx == 1 and (hands[0] in q.w.search(Prop="Two-handed") or versatile):
        #         continue

        #     cdata = get.weapon_action_handler(hand)
            
            # if cdata.Category == "Shield":
            #     self.actions_shield(cdata, idx)
            # else:
            #     self.actions_weapon(cdata, idx)

    # def actions_shield(self, cdata, idx):
    #     with group(parent=tag.wactions.cell("Name", idx)):add_text(cdata.Name)
    #     with group(parent=tag.wactions.cell("Range", idx)): add_text("")
    #     with group(parent=tag.wactions.cell("Hit", idx)): add_text("")
    #     with group(parent=tag.wactions.cell("Damage", idx)): add_text(f"AC: {cdata.AC}")
    #     with group(parent=tag.wactions.cell("Type", idx)): add_text("")
    #     with group(parent=tag.wactions.cell("Notes", idx)): add_text("")

    # def actions_weapon(self, cdata, idx):
    #     with group(parent=tag.wactions.cell("Name", idx)):add_text(cdata.Name)
    #     with group(parent=tag.wactions.cell("Range", idx)): add_text(cdata.Range)
    #     with group(parent=tag.wactions.cell("Hit", idx)):
    #         with group(horizontal=True):
    #             add_text(cdata.hSign)
    #             add_text(cdata.hNum, color=cdata.hColor)

    #     with group(parent=tag.wactions.cell("Damage", idx)):
    #         with group(horizontal=True):
    #             add_text(cdata.dDice)
    #             add_text(cdata.dSign)
    #             add_text(cdata.dNum, color=cdata.dColor)

    #     with group(parent=tag.wactions.cell("Type", idx)):
    #         add_text(cdata.dType, tag=tag.wactions.text("Type", idx))
    #         item_delete(tag.wactions.tooltip("Type", idx))
    #         with tooltip(tag.wactions.text("Type", idx), tag=tag.wactions.tooltip("Type", idx)):
    #             if cdata.dType:
    #                 add_text(get.dict_weapon_dtype_description[cdata.dType])

    #     with group(parent=tag.wactions.cell("Notes", idx)):
    #         with group(horizontal=True):
    #             for prop in cdata.Prop:
    #                 if prop == "Special": sc = get.dict_weapon_prop["Special"]["SC"]; desc = get.dict_weapon_prop["Special"][cdata.Name]
    #                 else: sc = get.dict_weapon_prop[prop]["SC"]; desc = get.dict_weapon_prop[prop]["Desc"]
    #                 add_text(sc, tag=tag.wactions.text("wprop", prop, idx))
    #                 item_delete(tag.wactions.tooltip("wprop", prop, idx))
    #                 with tooltip(tag.wactions.text("wprop", prop, idx), tag=tag.wactions.tooltip("wprop", prop, idx)):
    #                     add_text(prop, color=c_h1)
    #                     add_text(desc, wrap=240)