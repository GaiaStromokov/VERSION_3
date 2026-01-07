from Utils.UI.f_Utility import *
Tag = q.Tag
Rules = q.Rules
Coler = q.Coler

class pat_Sheet:
    def __init__(self):
        pass

    @property
    def dbm(self):
        return q.dbm
    
    @property
    def db(self):
        return q.dbm.db

    def All(self):
        self.Core()
        self.Atr()
        
        self.Health()
        self.Initiative()
        
        self.Skill()
        self.Vision()
        self.Speed()
        self.Prof()
        
        self.Condition()

        
    def Core(self):
        Level, PB, R, SR, C, SC, BG = self.dbm.Vis.upd_Sheet
        configure_item(Tag.core.val.level(), label=Level)
        configure_item(Tag.core.val.pb(), label = f"PB: +{PB}")
        configure_item(Tag.core.select.r(), items=Rules.l.Race, default_value=R)
        configure_item(Tag.core.select.sr(), items=Rules.d.Race[R], default_value=SR)
        configure_item(Tag.core.select.c(), items=Rules.l.Class, default_value=C)
        configure_item(Tag.core.select.sc(), items=Rules.d.Class[C] if q.dbm.Validate.Class else [], default_value=SC)
        configure_item(Tag.core.select.bg(), items=Rules.l.Background, default_value=BG)

    def Atr(self):
        data = self.db.Atr.View()
        for key in q.Rules.l.Atr:
            v = data[key]
            configure_item(Tag.atr.val(key), label=v.Val)
            configure_item(Tag.atr.mod(key), label=v.Mod)
            configure_item(Tag.atr.select(key), default_value=v.Base)
            configure_item(Tag.atr.source(key, "Base"), label=v.Base)
            configure_item(Tag.atr.source(key, "Race"), label=v.Race)
            configure_item(Tag.atr.source(key, "Feat"), label=v.Milestone)

    def Health(self):
        data = self.db.HP
        configure_item(Tag.health.hp(), label = f"{data.Current} / {data.Max}")
        configure_item(Tag.health.temp(), label = data.Temp)
        set_value(Tag.health.max(), data.Max)
        
    def Initiative(self):
        data = self.db.Initiative
        configure_item(Tag.init.val(), label = data.Val)
        configure_item(Tag.init.source("Dex"), label=self.db.Atr.DEX.Mod)
        configure_item(Tag.init.source("Race"), label = data.Race)
        configure_item(Tag.init.source("Class"), label = data.Class)
        configure_item(Tag.init.source("Milestone"), label = data.Milestone)

    def Vision(self):
        data = self.db.Vision.View()
        configure_item(Tag.vision.val(), label=data["Dark"].Val)
        for v in data:
            d = data[v].Val
            configure_item(Tag.vision.source(v), label=d)


    def Speed(self):
        data = self.db.Speed.View()
        configure_item(Tag.speed.val(), label=data["Walk"].Val)
        for v in data:
            d = data[v].Val
            configure_item(Tag.speed.source(v), label=d)

    def Condition(self):
        data = self.db.Condition.View()
        for key in data:
            i = data[key]
            configure_item(Tag.cond.toggle(key),default_value = i)
            configure_item(Tag.cond.text(key), color = Coler.Toggle(i))

    def Skill(self):
        data = self.db.Skill.View()
        for key in data:
            d=data[key]
            configure_item(Tag.skill.toggle(key), default_value=d.Val)
            configure_item(Tag.skill.mod(key), label= f"{d.Mod:+}")
            # configure_item(f"skill_Player_{key}", default_value = key in cdata["Player"])
            configure_item(Tag.skill.source(key, "Race"), default_value = d.Race[0])
            configure_item(Tag.skill.source(key, "Class"), default_value = d.Class[0])
            configure_item(Tag.skill.source(key, "BG"), default_value = d.Background[0])
            configure_item(Tag.skill.source(key, "Milestone"), default_value = d.Milestone[0])


    def Prof(self):
        data = self.db.Prof
        
        d_W = data.Weapon.Val
        d_A = data.Armor.Val
        d_T = data.Tool.Val
        d_L = data.Lang.Val
        for i in q.itm.Search([0], ["Simple"]):
            val = i in d_W
            configure_item(Tag.prof.toggle("Simple", i), default_value=val)
            configure_item(Tag.prof.text("Simple", i), color=Coler.Toggle(val))

        for i in q.itm.Search([0], ["Martial"]):
            val = i in d_W
            configure_item(Tag.prof.toggle("Martial", i), default_value=val)
            configure_item(Tag.prof.text("Martial", i), color=Coler.Toggle(val))
        for i in Rules.l.Armor:
            val = i in d_A
            configure_item(Tag.prof.toggle("Armor", i), default_value=val)
            configure_item(Tag.prof.text("Armor", i), color=Coler.Toggle(val))

        for i in Rules.l.Job:
            val = i in d_T
            configure_item(Tag.prof.toggle("Artisan", i), default_value=val)
            configure_item(Tag.prof.text("Artisan", i), color=Coler.Toggle(val))

        for i in Rules.l.Game:
            val = i in d_T
            configure_item(Tag.prof.toggle("Gaming", i), default_value=val)
            configure_item(Tag.prof.text("Gaming", i), color=Coler.Toggle(val))

        for i in Rules.l.Music:
            val = i in d_T
            configure_item(Tag.prof.toggle("Musical", i), default_value=val)
            configure_item(Tag.prof.text("Musical", i), color=Coler.Toggle(val))

        for i in Rules.l.Lang:
            val = i in d_L
            configure_item(Tag.prof.toggle("Languages", i), default_value=val)
            configure_item(Tag.prof.text("Languages", i), color=Coler.Toggle(val))


    # def AC(self):
    #     data = q.dbm.Armor.g.Visual
    #     configure_item(Tag.ac.val(), label = data.Sum)
    #     configure_item(Tag.ac.source("base"), label = data.Base)
    #     configure_item(Tag.ac.source("dex"), label = data.Dex)
    #     configure_item(Tag.ac.source("shield"), label = data.Shield)



    # def Char(self):
    #     cdata=q.db.Characteristic
    #     for i in Rules.list_Ideals:
    #         name = i.lower()
    #         configure_item(Tag.char.input(name), default_value=cdata[i])
    #         configure_item(Tag.char.text(name), default_value=cdata[i])
        
    #     cdata=q.db.Description
    #     for i in Rules.list_Description:
    #         configure_item(Tag.pDesc.input(i), default_value=cdata[i])
    #         configure_item(Tag.pDesc.text(i), default_value=cdata[i])

