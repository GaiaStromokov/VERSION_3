from dearpygui.dearpygui import *
import q, re, math
from colorist import *
Coler = q.Coler
Rules = q.Rules
Grimoir = q.Grimoir


class tgen:
    def __init__(self, name: str):
        self.name = name.replace("_", " ")
        self.tag = name.replace(" ", "_")


def gen_abil(name: str):
    an = name
    tn = name.replace(" ", "_")
    return an, tn 

def idel(tag):
    if does_item_exist(tag): delete_item(item=tag, children_only=False)

def icl(tag):
    if does_item_exist(tag): delete_item(item=tag, children_only=True)
    



def item_detail_handler(item_id):
    data = q.itm.get(item_id)
    if not data:
        return

    lcat = ["Weapon", "Armor"]
    detail_functions = {
        "Weapon": item_detail_weapon,
        "Armor": item_detail_armor,
    }
    for cat in lcat:
        if cat in data.cat:
            detail_functions[cat](data)
            return
        
def item_detail_weapon(data):
    with group(horizontal=True):
        add_text("Range", color=Coler.Header.G)
        add_text(data.Range, color=Coler.Text)

    with group(horizontal=True):
        add_text("Damage", color=Coler.Header.G)
        add_text(f"{data.Hit:+} to hit, {data.Roll} {data.Dam:+} Damage", color=Coler.Header.HP)

    with group(horizontal=True):
        add_text("Prop", color=Coler.Header.G)
        for prop in data.prop: add_text(prop, color=Coler.Text)

        add_text("Rarity", color=Coler.Header.G)
        add_text(Rules.g_Item_Rarity(data.tier), color=Coler.Text)

        add_text("Weight", color=Coler.Header.G)
        add_text(data.weight, color=Coler.Text)

        add_text("Cost", color=Coler.Header.G)
        add_text(data.cost, color=Coler.Item.M)


def item_detail_armor(data):
    with group(horizontal=True):
        add_text("AC", color=Coler.Header.G)
        add_text(data.AC, color=Coler.Text)

        add_text("Prop", color=Coler.Header.G)
        for prop in data.prop: add_text(prop, color=Coler.Text)

        add_text("Rarity", color=Coler.Header.G)
        add_text(Rules.g_Item_Rarity(data.tier), color=Coler.Text)

        add_text("Weight", color=Coler.Header.G)
        add_text(data.weight, color=Coler.Text)

        add_text("Cost", color=Coler.Header.G)
        add_text(data.cost, color=Coler.Item.M)

def spell_detail(spell):
    try: data = Grimoir[spell]
    except (KeyError, AttributeError, TypeError): return 
    with group(horizontal=True):
        add_text("Level", color=Coler.Header.G)
        if data["Level"] == 0: add_text("Cantrip", color=Coler.Text)
        else: add_text(data["Level"], color=Coler.Text)
        add_text("School", color=Coler.Header.G)
        add_text(data["School"], color=getattr(Coler.School, data['School']))
    with group(horizontal=True):
        add_text("Range", color=Coler.Header.G)
        add_text(data["Range"], color=Coler.Text)
        add_text("Components", color=Coler.Header.G)
        add_text(data["Components"], color=Coler.Text)
    with group(horizontal=True):
        add_text("Casting Time", color=Coler.Header.G)
        add_text(data["Casting Time"], color=Coler.Text)
        add_text("Duration", color=Coler.Header.G)
        add_text(data["Duration"], color=Coler.Text)
    with group(horizontal=True):
        if data.get("Ritual"):
            add_text("Ritual", color=Coler.Header.G)
            add_text(data["Ritual"], color=Coler.Text)
        if data.get("Concentration"):
            add_text("Concentration", color=Coler.Header.G)
            add_text(data["Concentration"], color=Coler.Text)
    with group(horizontal=False):
            add_text("Description", color=Coler.Header.G)
            descs = data["Desc"].replace(".", ".\n").split("\n")
            for item in descs:
                if item.strip():
                    add_text(item.strip(), color=Coler.Text, wrap=420)