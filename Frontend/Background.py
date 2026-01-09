from Utils.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler
sz = q.Sizing

t_Panel = Tag.block.bg.panel()
t_Feature = Tag.block.bg.feature()


                
class pat_Background:
    def __init__(self):
        pass

    @property
    def dbm(self):
        return q.dbm

    @property
    def db(self):
        return q.dbm.db

    @property
    def BG(self):
        return q.dbm.Background

    @property
    def Features(self):
        return q.dbm.db.Background.Features

    @property
    def Tools(self):
        return q.dbm.db.Background.Tool

    @property
    def Langs(self):
        return q.dbm.db.Background.Lang

    def Refresh(self):
        self.Panel()
        self.Feature()

    def Panel(self):
        icl(t_Panel)
        with group(parent=t_Panel):
            with group(horizontal=True):
                data = self.Tools
                if data.Options:
                    add_text("Tool Select", color=Coler.Header.B)
                    for val, key in enumerate(data.Select):
                            t_combo = Tag.block.bg.panel.select(val,key)
                            add_combo(items=data.Options, default_value=val, width=100, no_arrow_button=True, user_data=[val, key], callback=q.cbh.Background_Tool_Select, tag=t_combo)
            with group(horizontal=True):
                data = self.Langs
                if data.Options:
                    add_text("Language Select", color=Coler.Header.B)
                    for val, key in enumerate(data.Select):
                            t_combo = Tag.block.bg.panel.select(val,key)
                            add_combo(items=data.Options, default_value=val, width=100, no_arrow_button=True, user_data=[val, key], callback=q.cbh.Background_Lang_Select, tag=t_combo)

    def Feature(self):
        data = self.Features
        Name = data.Name
        Desc = data.Desc
        
        t_text = Tag.block.bg.feature.text()
        
        icl(t_Feature)
        with group(parent=t_Feature):
            add_text(Name, color=Coler.Header.B, tag=t_text)
            add_text(Desc, color=Coler.Text, wrap=sz.Wrap)
