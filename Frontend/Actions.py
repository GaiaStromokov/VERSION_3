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
            if hand.base_name == "def_Item": continue
            if idx == 1:
                if hand.base_name == "Grip": continue

            if "Weapon" in hand.cat: 
                Roll = hand.Roll
                if idx == 0 and "Versatile" in hand.prop and hands[1].base_name == "Grip": Roll = hand.vRoll
                self.table_weapon(hand, idx, Roll)

            if "Shield" in hand.cat: 
                self.table_shield(hand, idx)


    def table_weapon(self, cdata, idx, Roll):
        name = cdata.base_name
        if cdata.tier != 0: name = f"{name} +{cdata.tier}"

        with group(parent=Tag.block.actions.cell("Name", idx)): add_text(name)
        with group(parent=Tag.block.actions.cell("Range", idx)): add_text(cdata.Range)
        with group(parent=Tag.block.actions.cell("Hit", idx)):
            with group(horizontal=True):
                add_text(f"{cdata.Hit:+}")

        with group(parent=Tag.block.actions.cell("Damage", idx)):
            with group(horizontal=True):
                add_text(f"{Roll} {cdata.Dam:+}")

        with group(parent=Tag.block.actions.cell("Type", idx)):
            t_text  = Tag.block.actions.text("Type", idx)
            t_tooltip = Tag.block.actions.tooltip("Type", idx)
            add_text(cdata.dType, tag=Tag.block.actions.text("Type", idx))
            idel(t_tooltip)
            with tooltip(t_text, tag=t_tooltip):
                if cdata.dType:
                    add_text(Rules.d.dType_Desc[cdata.dType], color=Coler.Header.G)

        with group(parent=Tag.block.actions.cell("Notes", idx)):
            with group(horizontal=True):
                for prop in cdata.prop:
                    t_text = Tag.block.actions.text("wprop", prop, idx)
                    t_tooltip = Tag.block.actions.tooltip("wprop", prop, idx)
                    rules = Rules.d.Weapon_Prop[prop]
                    add_text(rules[0], tag=t_text)
                    idel(t_tooltip)
                    with tooltip(t_text, tag=t_tooltip):
                        add_text(prop, color=Coler.Header.G)
                        add_text(rules[1], wrap=240, color=Coler.Header.B)

    def table_shield(self, cdata, idx):
        with group(parent=Tag.block.actions.cell("Name", idx)):add_text(cdata.id)
        with group(parent=Tag.block.actions.cell("Range", idx)): add_text("")
        with group(parent=Tag.block.actions.cell("Hit", idx)): add_text("")
        with group(parent=Tag.block.actions.cell("Damage", idx)): add_text("")
        with group(parent=Tag.block.actions.cell("Type", idx)): add_text("")
        with group(parent=Tag.block.actions.cell("Notes", idx)): add_text(f"AC: {cdata.AC}")

