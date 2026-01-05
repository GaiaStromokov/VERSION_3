from Utils.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing


t_tb = Tag.block.tabbar.Spells()
twindow_main = Tag.block.Spells.window()


tcast_Abil = Tag.spell.text("Abil")
tcast_Atk  = Tag.spell.text("Atk")
tcast_DC   = Tag.spell.text("DC")
tcast_window_A = Tag.Spells.Cast.A()
tcast_window_B = Tag.Spells.Cast.B()


tlearn_window_A = Tag.Spells.Learn.A()
tlearn_window_B = Tag.Spells.Learn.B()
tlearn_a_cantrip = Tag.Spells.Learn.Available.Cantrip()
tlearn_a_spell = Tag.Spells.Learn.Available.Spell()
tlearn_k_cantrip = Tag.Spells.Learn.Known.Cantrip()
tlearn_k_spell = Tag.Spells.Learn.Known.Spell()


tprep_current = Tag.Spells.Prepare.current()
tprep_available = Tag.Spells.Prepare.available()

l_Spell_Type = ["Cantrip", "Spell", "Spell", "Spell", "Spell", "Spell", "Spell", "Spell", "Spell", "Spell"] 

d_Spell_Type = {
    "Cantrip": "Will",
    "Spell": "Cast"
}

l_Spell_Handle = ["Cantrip", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9"]

class pat_Caster:
    def __init__(self):
        self.Cast = Cast(self)
        self.Learn = Learn(self)
        self.Prepare = Prepare(self)


    @property
    def data(self):
        return q.dbm.db.Caster
    
    @property
    def dToggle(self):
        return self.data.Toggle

    
    
    def Refresh(self):
        if self.dToggle:
            show_item(t_tb)
            self.Cast.Refresh()
            self.Learn.Refresh()
            self.Prepare.Refresh()
        else: hide_item(t_tb)
    
    def Cast_Spell(self):
        self.Cast.Refresh_B()


        

class Cast:
    def __init__(self, mgr):
        self.mgr = mgr
        self.l_sh = ["Cantrip", "Level 1", "Level 2", "Level 3", "Level 4", "Level 5", "Level 6", "Level 7", "Level 8", "Level 9"]

    def Refresh(self):
        self.Refresh_A()
        self.Refresh_B()

    def Refresh_A(self):
        data = self.mgr.data
        configure_item(tcast_Abil, default_value=data.Abil)
        configure_item(tcast_Atk, default_value=data.ATK)
        configure_item(tcast_DC, default_value=data.DC)

    def Refresh_B(self):
        data = self.mgr.data
        icl(tcast_window_B)
        with group(parent=tcast_window_B):
            for level in [0,1,2,3,4,5,6,7,8,9]:
                spell_list = data.Prepared[level]
                if not spell_list: continue
                spell_type = l_Spell_Type[level]
                with group(horizontal=False):
                    with group(horizontal=True):
                        add_text(self.l_sh[level], color=Coler.Header.B)
                        
                        if spell_type == "Spell":
                            for idx, value in enumerate(data.Slot[level]):
                                t = Tag.Spells.Cast.Toggle(level, idx)
                                add_checkbox(default_value=value, enabled=False, tag=t)
                                

                    button_label = d_Spell_Type[spell_type]
                    for spell in spell_list:
                        t_btn = Tag.Spells.Cast.Button(level, spell)
                        t_text = Tag.Spells.Cast.Text(level, spell)
                        t_tt = Tag.Spells.Cast.Tooltip(level, spell)
                        
                        with group(horizontal=True):
                            add_button(label=button_label, width=50, user_data=[level], callback=q.cbh.Spell_Cast, tag=t_btn)
                            add_text(spell, color=Coler.Header.G, tag=t_text)
                            idel(t_tt)
                            with tooltip(t_text, tag=t_tt):
                                spell_detail(spell)
                    add_separator()



class Learn:
    def __init__(self, mgr):
        self.mgr = mgr
        
    def Refresh(self):
        self.Refresh_A()
        self.Refresh_B()

    def Refresh_A(self):
        data = self.mgr.data
        configure_item(tlearn_k_cantrip, default_value=data.Cantrips_Known)
        configure_item(tlearn_a_cantrip, default_value=data.Cantrips_Available)
        configure_item(tlearn_k_spell, default_value=data.Spells_Known)
        configure_item(tlearn_a_spell, default_value=data.Spells_Available)

    def Refresh_B(self):
        data = self.mgr.data
        cast_list_name = data.Caster_List
        
        for level in [0,1,2,3,4,5,6,7,8,9]:
            spell_type = l_Spell_Type[level]
            t_win = Tag.Spells.Learn.WLevel(level)
            
            available_spells = q.fTome(Level=level, Caster=cast_list_name)
            current_spells = data.Book[level]
            
            icl(t_win)
            with group(parent=t_win):
                for spell in available_spells:
                    is_known = spell in current_spells
                    t_sel = Tag.Spells.Learn.Toggle(level, spell)
                    t_tt = Tag.Spells.Learn.Tooltip(level, spell)
                    add_selectable(label=spell, default_value=is_known, width=680, user_data=[spell, level, spell_type], callback=q.cbh.Spell_Learn, tag=t_sel)
                    idel(t_tt)
                    with tooltip(t_sel, tag=t_tt):
                        spell_detail(spell)


class Prepare:
    def __init__(self, mgr):
        self.mgr = mgr

    def Refresh(self):
        self.Refresh_A()
        self.Refresh_B()


    def Refresh_A(self):
        data = self.mgr.data
        v_Prepared_Available = data.Prepared_Available
        if data.Prepared_Available == 99999: v_Prepared_Available = "INF"
        configure_item(tprep_current, default_value=data.Spells_Prepared)
        configure_item(tprep_available, default_value=v_Prepared_Available)

    def Refresh_B(self):
        data = self.mgr.data
        for level in [1,2,3,4,5,6,7,8,9]:
            t_win = Tag.Spells.Prepare.WLevel(level)
            known_spells = data.Book[level]
            prepared_spells = data.Prepared[level]
            
            icl(t_win)
            if not known_spells: continue
            
            with group(parent=t_win):
                for spell in known_spells:
                    t_sel = Tag.Spells.Prepare.Toggle(level, spell)
                    t_tt = Tag.Spells.Prepare.Tooltip(level, spell)

                    is_prepared = spell in prepared_spells
                    
                    add_selectable(label=spell, default_value=is_prepared, width=680, user_data=[spell, level], callback=q.cbh.Spell_Prepare, tag=t_sel)
                    idel(t_tt)
                    with tooltip(t_sel, tag=t_tt):
                        spell_detail(spell)