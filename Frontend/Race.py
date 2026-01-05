from Utils.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing


class pat_Race:
    def __init__(self):
        self.parent = Tag.block.r.feature()
        self.t_Feature = Tag.block.r.feature()

    @property
    def dbm(self):
        return q.dbm

    @property
    def db(self):
        return q.dbm.db

    def Refresh(self):
        self.Asi_Select()
        self.Features()
        

    def Asi_Select(self):
        pass

    def Features(self):
        icl(self.parent)
        for key, data in self.db.Race.Features.items():
            tag = data["Tag"]
            fn = getattr(self, f"gen_{tag}", None)

            temp = tgen(key)
            if callable(fn):
                fn(temp.name, temp.tag, data)


    def gen_Passive(self, name, t, data):
        l_Desc = data["Desc"]
        t_header = Tag.block.r.feature.header(t)
        tl_Desc = [Tag.block.r.feature.text(t, f"{i}") for i in range(len(l_Desc))]
        
        with group(parent=self.parent):
            add_text(name, color=Coler.Header.G, tag=t_header)
            for i, Desc in enumerate(l_Desc):
                add_text(Desc, color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])

    def gen_Select(self, name, t, data):
        select_list = data["Select"]
        desc_list = data["Desc"]
        item_list = data["Options"]
        t_header = Tag.block.r.feature.header(t)
        t_popup = Tag.block.r.feature.popup(t)
        
        tl_Label = [Tag.block.r.feature.label(t, f"{i}") for i in range(len(desc_list))]
        tl_Select = [Tag.block.r.feature.select(t, f"{i}") for i in range(len(select_list))]
        
        with group(parent=self.parent):
            add_text(name, color=Coler.Header.G, tag=t_header)
            for key, v in enumerate(select_list):
                if v:
                    add_text(v, color=Coler.Header.HP, tag=tl_Label[key])
                    add_text(desc_list[key], color=Coler.Text, wrap=sz.Wrap)
                    
            
            idel(t_popup)
            with popup(t_header, mousebutton=mvMouseButton_Left, tag=t_popup):
                for idx, v in enumerate(select_list):
                    in_other_lists = select_list[:idx] + select_list[idx+1:]
                    items = [x for x in item_list if x not in in_other_lists]
                    add_combo(items=items, default_value=select_list[idx], width=120, no_arrow_button=True, user_data=[t, idx], callback=q.cbh.Class_F_Select, tag=tl_Select[idx])

    def gen_Use(self, name, t, data):
        l_Desc = data["Desc"]
        l_Use = data["Use"]
        t_header = Tag.block.r.feature.header(t)
        tl_Desc = [Tag.block.r.feature.text(t, f"{i}") for i in range(len(l_Desc))]
        tl_Toggle = [Tag.block.r.feature.toggle(t, f"{i}") for i in range(len(l_Use))]
        
        

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                for idx, val in enumerate(l_Use):
                    add_checkbox(default_value=val, enabled=True, user_data=[t, idx], callback=q.cbh.Class_F_Use, tag=tl_Toggle[idx])

            for i, Desc in enumerate(l_Desc):
                add_text(Desc, color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])


    def gen_Spell(self, name, t, data):
        t_header = Tag.block.r.feature.header(t)

        with group(parent=self.parent):
            add_text(name, color=Coler.Header.G, tag=t_header)
            
            spell_items = data["Spells"]

            for spell, val in spell_items.items():
                t_label = Tag.block.r.feature.label(t, spell)
                t_tooltip = Tag.block.r.feature.tooltip(t, spell)
                t_toggle = Tag.block.r.feature.toggle(t, spell)
                with group(horizontal=True):
                    add_text(spell, color=Coler.Header.B, tag=t_label)
                    if val == "Will": add_text("Will", color=Coler.Header.HP)
                    else: add_checkbox(default_value=val[0], enabled=True, user_data=[t, spell], callback=q.cbh.Race_Spell_Toggle, tag=t_toggle)
                
                idel(t_tooltip)
                with tooltip(t_label, tag=t_tooltip):
                    spell_detail(spell)

    def gen_High_Cantrip(self, name, t, data):
        selection = data["Select"][0]
        option_list = data["Options"]
        t_header = Tag.block.r.feature.header(t)
        t_popup = Tag.block.r.feature.popup(t)
        t_select = Tag.block.r.feature.select(t)
        t_label = Tag.block.r.feature.label(t)
        t_tooltip = Tag.block.r.feature.tooltip(t)
        
        with group(parent=self.parent):
            add_text(name, color=Coler.Header.G, tag=t_header)
            if selection:
                add_text(selection, color=Coler.Header.HP, tag=t_label)
                idel(t_tooltip)
                with tooltip(t_label, tag=t_tooltip):
                    spell_detail(selection)
            
            idel(t_popup)
            with popup(t_header, mousebutton=mvMouseButton_Left, tag=t_popup):
                add_combo(items=option_list, default_value=selection, width=120, no_arrow_button=True, user_data=[t, 0], callback=q.cbh.Race_F_Select, tag=t_select)



    def gen_Select(self, name, t, data):
        select_list = data["Select"]
        desc_list = data["Desc"]
        item_list = data["Options"]
        t_header = Tag.block.r.feature.header(t)
        t_popup = Tag.block.r.feature.popup(t)
        
        tl_Label = [Tag.block.r.feature.label(t, f"{i}") for i in range(len(desc_list))]
        tl_Select = [Tag.block.r.feature.select(t, f"{i}") for i in range(len(select_list))]
        
        with group(parent=self.parent):
            add_text(name, color=Coler.Header.G, tag=t_header)
            for key, v in enumerate(select_list):
                if v:
                    add_text(v, color=Coler.Header.HP, tag=tl_Label[key])
                    add_text(desc_list[key], color=Coler.Text, wrap=sz.Wrap)
                    
            
            idel(t_popup)
            with popup(t_header, mousebutton=mvMouseButton_Left, tag=t_popup):
                for idx, v in enumerate(select_list):
                    in_other_lists = select_list[:idx] + select_list[idx+1:]
                    items = [x for x in item_list if x not in in_other_lists]
                    add_combo(items=items, default_value=select_list[idx], width=120, no_arrow_button=True, user_data=[t, idx], callback=q.cbh.Class_F_Select, tag=tl_Select[idx])




    def gen_Tinker(self, name, t, data):

        selection = data["Select"][0]
        options = data["Options"]
        desc = data["Desc"][0]
        t_header = Tag.block.r.feature.header(t)
        
        t_select = Tag.block.r.feature.select(t)
        t_popup = Tag.block.r.feature.tool(t)



        with group(parent=self.parent):
            add_text(name, color=Coler.Header.G, tag=t_header)
            add_text(desc, color=Coler.Header.B)
                
            idel(t_popup)
            with popup(t_header, mousebutton=mvMouseButton_Left, tag=t_popup):
                add_combo(items=options, default_value=selection, width=150, no_arrow_button=True, callback=q.cbh.Race_F_Select, user_data=[t, 0], tag=t_select)

            if selection:
                with group(horizontal=True):
                    add_text(selection, color=Coler.Header.C)
                    add_text(data["Multi_Desc"][selection], color=Coler.Header.HP)