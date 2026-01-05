from Utils.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing


class pat_Class:
    def __init__(self):
        self.parent = Tag.block.c.feature()
        self.t_Skill = Tag.block.c.skill()
        self.t_Feature = Tag.block.c.feature()

    @property
    def dbm(self):
        return q.dbm

    @property
    def db(self):
        return q.dbm.db

    def Refresh(self):
        self.Skill_Select()
        self.Features()
        

    def Skill_Select(self):
        data = self.db.Class.Skill
        t_Clear = Tag.block.c.skill.clear()
        icl(self.t_Skill)
        with group(parent=self.t_Skill):
            with group(horizontal=True):
                add_text("Skill Select", color=Coler.Header.G)
                for idx, key in enumerate(data.Select):
                    t_toggle = Tag.block.c.skill.toggle(idx)
                    add_combo(items=data.Options, default_value=key,  width=100, no_arrow_button=True, user_data=[idx], callback=q.cbh.Class_S_Select, tag=t_toggle)
                add_button(label = "Clear", user_data=[], callback=q.cbh.Class_S_Clear, tag=t_Clear)


    def Features(self):
        icl(self.parent)
        for key, data in self.db.Class.Features.items():
            tag = data["Tag"]
            fn = getattr(self, f"gen_{tag}", None)

            temp = tgen(key)
            if callable(fn):
                fn(temp.name, temp.tag, data)


    def gen_Passive(self, name, t, data):
            l_Desc = data["Desc"]
            t_header = Tag.block.c.feature.header(t)
            tl_Desc = [Tag.block.c.feature.text(t, f"{i+1}") for i in range(len(l_Desc))]
            
            with group(parent=self.parent):
                add_text(name, color=Coler.Header.G, tag=t_header)
                for i, Desc in enumerate(l_Desc):
                    add_text(Desc, color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])

    def gen_Select(self, name, t, data):
        select_list = data["Select"]
        desc_list = data["Desc"]
        item_list = data["Options"]
        t_header = Tag.block.c.feature.header(t)
        t_popup = Tag.block.c.feature.popup(t)
        
        tl_Label = [Tag.block.c.feature.label(t, f"{i}") for i in range(len(desc_list))]
        tl_Select = [Tag.block.c.feature.select(t, f"{i}") for i in range(len(select_list))]
        



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
        t_header = Tag.block.c.feature.header(t)
        tl_Desc = [Tag.block.c.feature.text(t, f"{i}") for i in range(len(l_Desc))]
        tl_Toggle = [Tag.block.c.feature.toggle(t, f"{i}") for i in range(len(l_Use))]
        
        

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                for idx, val in enumerate(l_Use):
                    add_checkbox(default_value=val, enabled=True, user_data=[t, idx], callback=q.cbh.Class_F_Use, tag=tl_Toggle[idx])

            for i, Desc in enumerate(l_Desc):
                add_text(Desc, color=Coler.Text, wrap=sz.Wrap, tag=tl_Desc[i])

    def gen_Spell_Mastery(self, name, t, data):
        t_header = Tag.block.c.feature.header(t)
        t_select = [Tag.block.c.feature.select.A(t), Tag.block.c.feature.select.B(t)]
        t_tool = [Tag.block.c.feature.tool.A(t), Tag.block.c.feature.tool.B(t)]

        selected = data["Select"]
        options = data["Options"]

        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
            for i in [0,1]:
                with group(horizontal=True):
                    add_text(f"Sel {i}: ", color=Coler.Header.C)
                    add_combo(items=options[i], default_value=selected[i], width=150, no_arrow_button=True, callback=q.cbh.Class_F_Select, user_data=[t, i], tag=t_select[i])
                    add_text(f"Will", color=Coler.Header.B)
                idel(t_tool[i])
                with tooltip(t_select[i], tag=t_tool[i]):
                    spell_detail(selected[i])

    def gen_Signature_Spell(self, name, t, data):
        selected = data["Select"]
        options = data["Options"]
        uses = data["Use"]
        
        t_header = Tag.block.c.feature.header(t)
    
        t_select = [Tag.block.c.feature.select.A(t), Tag.block.c.feature.select.B(t)]
        t_tool = [Tag.block.c.feature.tool.A(t), Tag.block.c.feature.tool.B(t)]
        t_toggle = [Tag.block.c.feature.toggle.A(t), Tag.block.c.feature.toggle.B(t)]



        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
            for i in [0,1]:
                with group(horizontal=True):
                    add_text(f"Sel {i}: ", color=Coler.Header.C)
                    add_combo(items=options[i], default_value=selected[i], width=150, no_arrow_button=True, callback=q.cbh.Class_F_Select, user_data=[t, i], tag=t_select[i])
                    add_checkbox(default_value=uses[i], enabled=True, user_data=[t, i], callback=q.cbh.Class_F_Use, tag=t_toggle[i])
                idel(t_tool[i])
                with tooltip(t_select[i], tag=t_tool[i]):
                    spell_detail(selected[i])

                
    def gen_Use_Select(self, name, t, data):
        t_header = Tag.block.c.feature.header(t)
        t_sel_1 = Tag.block.c.feature.select(t, "opt_1")
        t_sel_2 = Tag.block.c.feature.select(t, "opt_2")
        t_text_1 = Tag.block.c.feature.text(t, "opt_1")
        t_text_2 = Tag.block.c.feature.text(t, "opt_2")
        t_tool_1 = Tag.block.c.feature.tooltip(t, "opt_1")
        t_tool_2 = Tag.block.c.feature.tooltip(t, "opt_2")
        t_toggle_1 = Tag.block.c.feature.toggle(t, 1)
        t_toggle_2 = Tag.block.c.feature.toggle(t, 2)
        sel_1, sel_2 = data["Select"][1], data["Select"][2]
        
        sl_1, sl_2 = [""] + q.fTome(Level=data["Options"][1][1], Caster=data["Options"][1][0]), [""] + q.fTome(Level=data["Options"][2][1], Caster=data["Options"][2][0])
        use_1, use_2 = data["Use"][1], data["Use"][2]
        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
            with group(horizontal=True):
                add_text("Sel 1: ", color=Coler.Header.C)
                add_combo(items=sl_1, default_value=sel_1, width=150, no_arrow_button=True, callback=q.cbh, user_data=["Class Feature Select", t, 1], tag=t_sel_1)
                add_checkbox(default_value=use_1, enabled=True, user_data=["Class Feature Use", t, 1], callback=q.cbh, tag=t_toggle_1)
            with group(horizontal=True):
                add_text("Sel 2: ", color=Coler.Header.C)
                add_combo(items=sl_2, default_value=sel_2, width=150, no_arrow_button=True, callback=q.cbh, user_data=["Class Feature Select", t, 2], tag=t_sel_2)
                add_checkbox(default_value=use_2, enabled=True, user_data=["Class Feature Use", t, 2], callback=q.cbh, tag=t_toggle_2)


            idel(t_tool_1)
            with tooltip(t_sel_1, tag=t_tool_1):
                spell_detail(sel_1)
            idel(t_tool_2)
            with tooltip(t_sel_2, tag=t_tool_2):
                spell_detail(sel_2)
                
                
    def gen_Familiar(self, name, t, data):
        t_header = Tag.block.c.feature.header(t)
        t_desc = Tag.block.c.feature.text(t)
        t_hp = Tag.block.c.feature.HP(t)
        t_use = Tag.block.c.feature.toggle(t)
        
        with group(parent=self.parent):
            with group(horizontal=True):
                add_text(name, color=Coler.Header.G, tag=t_header)
                add_text("---", color=Coler.Header.G)
                add_checkbox(default_value=data["Use"][0], enabled=True, user_data=[t, 0], callback=q.cbh.Class_F_Use, tag=t_use)
                add_text("---", color=Coler.Header.G)
                add_button(label="-", user_data=[t, -1], width=20, callback=q.cbh.Familiar_Update)
                add_button(label=f"{data['HP']['Current']} / {data['HP']['Max']}",  enabled=False, tag=t_hp)
                add_button(label="+", user_data=[t, 1], width=20, callback=q.cbh.Familiar_Update)
                

            with group(horizontal=True):
                add_text(data["Desc"][0], color=Coler.Text, wrap=sz.Wrap, tag=t_desc)

