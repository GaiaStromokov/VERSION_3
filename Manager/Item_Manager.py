import q

class ItemManager:
    def __init__(self):
        self.cache = {}
        self.map_tier = {} 
        self.map_cat = {}
        self._populate()

    def _populate(self):
        for cls in Item.registry:
            for t in cls.lTier:
                item = cls(t)
                self.cache[item.id] = item

                if t not in self.map_tier: self.map_tier[t] = set()
                self.map_tier[t].add(item.id)

                for c in item.cat:
                    if c not in self.map_cat: self.map_cat[c] = set()
                    self.map_cat[c].add(item.id)

    def get(self, iid): return self.cache.get(iid, self.cache.get("def_Item"))

    def Search(self, tiers, categories):
        valid_ids = set().union(*(self.map_tier[t] for t in tiers))
        
        for c in categories:
            valid_ids.intersection_update(self.map_cat[c])

        return list(valid_ids)


class Item:
    registry = []
    
    base_name = ""
    cat = set()
    prop = set()
    lTier = []
    cost = 0
    weight = 0
    
    Attune = False

    def __init__(self, tier):
        self.tier = tier

    def __init_subclass__(cls, **kwargs):
        super().__init_subclass__(**kwargs)
        Item.registry.append(cls)

    @property
    def id(self):
        if self.tier == 0:
            return self.base_name
        return f"{self.base_name}_{self.tier}"

    def Atr(self, key):
        if "Finesse" in self.prop: return max(getattr(q.dbm.db.Atr, "STR").Mod, getattr(q.dbm.db.Atr, "DEX").Mod)
        return getattr(q.dbm.db.Atr, key).Mod

class Weapon(Item):
    dType = ""
    Range = ""
    Roll = ""
    sDam = 1
    dMod = ""

    def __init_subclass__(cls, **kwargs):
        cls.cat.add("Weapon")
        super().__init_subclass__(**kwargs)
        
    @property
    def Hit(self): return self.Atr(self.dMod) + q.dbm.db.Core.PB + self.tier

    @property
    def Dam(self): return self.Atr(self.dMod) + (self.tier * self.sDam)

    def __repr__(self):
        lines = [f"Class_Name: {self.__class__.__name__}",f"Base_Name: {self.base_name}",f"Cat: {self.cat}",f"Prop: {self.prop}",f"dType: {self.dType}",f"dMod: {self.dMod}",f"Range: {self.Range}",f"Roll: {self.Roll}"]
        if hasattr(self, 'vRoll'): lines.append(f"vRoll: {self.vRoll}")
        lines.extend([f"Cost: {self.cost}",f"Weight: {self.weight}",f"Tier: {self.tier}"])
        return "\n".join(lines)

class Armor(Item):
    bAC = 0
    sDis = False
    sReq = 0
    dMax = 0

    def __init_subclass__(cls, **kwargs):
        cls.cat.add("Armor")
        super().__init_subclass__(**kwargs)
        
    @property
    def AC(self):
        if "Shield" in self.cat: return self.bAC + self.tier
        return self.bAC + self.tier + min(self.Atr("DEX"), self.dMax)

    def __repr__(self):
        return "\n".join([f"item name: {self.__class__.__name__}",f"base_name: {self.base_name}",f"cat: {self.cat}",f"bAC: {self.bAC}",f"sDis: {self.sDis}",f"sReq: {self.sReq}",f"dMax: {self.dMax}",f"Cost: {self.cost}",f"Weight: {self.weight}",f"Tier: {self.tier}"])

class def_Item(Item):
    base_name = "def_Item"
    lTier = [0]

class Grip(Item):
    base_name = "Grip"
    lTier = [0]
    
class Club(Weapon):
    base_name = "Club"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Light"}
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d4"
    Cost = 1
    Weight = 2
    lTier = [0, 1, 2, 3]

class Dart(Weapon):
    base_name = "Dart"
    cat = {"Simple", "Ranged", "Main", "Off"}
    prop = {"Finesse", "Thrown"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "20/60 ft"
    Roll = "1d4"
    Cost = 0.05
    Weight = 0.25
    lTier = [0, 1, 2, 3]

class Handaxe(Weapon):
    base_name = "Handaxe"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Light", "Thrown"}
    dType = "Slashing"
    dMod = "STR"
    Range = "5 - 20/60 ft"
    Roll = "1d6"
    Cost = 2
    Weight = 2
    lTier = [0, 1, 2, 3]

class Javelin(Weapon):
    base_name = "Javelin"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Thrown"}
    dType = "Piercing"
    dMod = "STR"
    Range = "5 - 30/120 ft"
    Roll = "1d6"
    Cost = 0.5
    Weight = 2
    lTier = [0, 1, 2, 3]

class Light_Hammer(Weapon):
    base_name = "Light_Hammer"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Light", "Thrown"}
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 - 20/60 ft"
    Roll = "1d4"
    Cost = 2
    Weight = 2
    lTier = [0, 1, 2, 3]

class Mace(Weapon):
    base_name = "Mace"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = set()
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d6"
    Cost = 5
    Weight = 4
    lTier = [0, 1, 2, 3]

class Quarterstaff(Weapon):
    base_name = "Quarterstaff"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Versatile"}
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d6"
    vRoll = "1d8"
    Cost = 0.2
    Weight = 4
    lTier = [0, 1, 2, 3]

class Sickle(Weapon):
    base_name = "Sickle"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Light"}
    dType = "Slashing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d4"
    Cost = 1
    Weight = 2
    lTier = [0, 1, 2, 3]

class Spear(Weapon):
    base_name = "Spear"
    cat = {"Simple", "Melee", "Main", "Off"}
    prop = {"Thrown", "Versatile"}
    dType = "Piercing"
    dMod = "STR"
    Range = "5 - 20/60 ft"
    Roll = "1d6"
    vRoll = "1d8"
    Cost = 1
    Weight = 3
    lTier = [0, 1, 2, 3]

class Light_Crossbow(Weapon):
    base_name = "Light_Crossbow"
    cat = {"Simple", "Ranged", "Main"}
    prop = {"Ammunition", "Loading", "Two-handed"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "80/320 ft"
    Roll = "1d8"
    Cost = 25
    Weight = 5
    lTier = [0, 1, 2, 3]

class Shortbow(Weapon):
    base_name = "Shortbow"
    cat = {"Simple", "Ranged", "Main"}
    prop = {"Ammunition", "Two-handed"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "80/320 ft"
    Roll = "1d6"
    Cost = 25
    Weight = 2
    lTier = [0, 1, 2, 3]

class Sling(Weapon):
    base_name = "Sling"
    cat = {"Simple", "Ranged", "Main", "Off"}
    prop = {"Ammunition"}
    dType = "Bludgeoning"
    dMod = "DEX"
    Range = "30/120 ft"
    Roll = "1d4"
    Cost = 0.1
    Weight = 0
    lTier = [0, 1, 2, 3]

class Battle_axe(Weapon):
    base_name = "Battle_axe"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Versatile"}
    dType = "Slashing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    vRoll = "1d10"
    Cost = 10
    Weight = 4
    lTier = [0, 1, 2, 3]

class Flail(Weapon):
    base_name = "Flail"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = set()
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    Cost = 10
    Weight = 2
    lTier = [0, 1, 2, 3]

class Glaive(Weapon):
    base_name = "Glaive"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Heavy", "Reach", "Two-handed"}
    dType = "Slashing"
    dMod = "STR"
    Range = "10 ft"
    Roll = "1d10"
    Cost = 20
    Weight = 6
    lTier = [0, 1, 2, 3]

class Great_axe(Weapon):
    base_name = "Great_axe"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Heavy", "Two-handed"}
    dType = "Slashing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d12"
    Cost = 30
    Weight = 7
    lTier = [0, 1, 2, 3]

class Halberd(Weapon):
    base_name = "Halberd"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Heavy", "Reach", "Two-handed"}
    dType = "Slashing"
    dMod = "STR"
    Range = "10 ft"
    Roll = "1d10"
    Cost = 20
    Weight = 6
    lTier = [0, 1, 2, 3]

class Longsword(Weapon):
    base_name = "Longsword"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Versatile"}
    dType = "Slashing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    vRoll = "1d10"
    Cost = 15
    Weight = 3
    lTier = [0, 1, 2, 3]

class Maul(Weapon):
    base_name = "Maul"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Heavy", "Two-handed"}
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 ft"
    Roll = "2d6"
    Cost = 10
    Weight = 10
    lTier = [0, 1, 2, 3]

class Morningstar(Weapon):
    base_name = "Morningstar"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = set()
    dType = "Piercing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    Cost = 15
    Weight = 4
    lTier = [0, 1, 2, 3]

class Pike(Weapon):
    base_name = "Pike"
    cat = {"Martial", "Melee", "Main"}
    prop = {"Heavy", "Reach", "Two-handed"}
    dType = "Piercing"
    dMod = "STR"
    Range = "10 ft"
    Roll = "1d10"
    Cost = 5
    Weight = 18
    lTier = [0, 1, 2, 3]

class Rapier(Weapon):
    base_name = "Rapier"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Finesse"}
    dType = "Piercing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    Cost = 25
    Weight = 2
    lTier = [0, 1, 2, 3]

class Scimitar(Weapon):
    base_name = "Scimitar"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Finesse", "Light"}
    dType = "Slashing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d6"
    Cost = 25
    Weight = 3
    lTier = [0, 1, 2, 3]

class Shortsword(Weapon):
    base_name = "Shortsword"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Finesse", "Light"}
    dType = "Piercing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d6"
    Cost = 10
    Weight = 2
    lTier = [0, 1, 2, 3]

class Trident(Weapon):
    base_name = "Trident"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Thrown", "Versatile"}
    dType = "Piercing"
    dMod = "STR"
    Range = "5 - 20/60 ft"
    Roll = "1d6"
    vRoll = "1d8"
    Cost = 5
    Weight = 4
    lTier = [0, 1, 2, 3]

class War_Pick(Weapon):
    base_name = "War_Pick"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = set()
    dType = "Piercing"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    Cost = 5
    Weight = 2
    lTier = [0, 1, 2, 3]

class Warhammer(Weapon):
    base_name = "Warhammer"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Versatile"}
    dType = "Bludgeoning"
    dMod = "STR"
    Range = "5 ft"
    Roll = "1d8"
    vRoll = "1d10"
    Cost = 15
    Weight = 2
    lTier = [0, 1, 2, 3]

class Whip(Weapon):
    base_name = "Whip"
    cat = {"Martial", "Melee", "Main", "Off"}
    prop = {"Finesse", "Reach"}
    dType = "Slashing"
    dMod = "STR"
    Range = "10 ft"
    Roll = "1d4"
    Cost = 2
    Weight = 3
    lTier = [0, 1, 2, 3]

class Blowgun(Weapon):
    base_name = "Blowgun"
    cat = {"Martial", "Ranged", "Main", "Off"}
    prop = {"Ammunition", "Loading"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "25/100 ft"
    Roll = "1"
    Cost = 10
    Weight = 1
    lTier = [0, 1, 2, 3]

class Hand_Crossbow(Weapon):
    base_name = "Hand_Crossbow"
    cat = {"Martial", "Ranged", "Main", "Off"}
    prop = {"Ammunition", "Light", "Loading"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "30/120 ft"
    Roll = "1d6"
    Cost = 75
    Weight = 3
    lTier = [0, 1, 2, 3]

class Heavy_Crossbow(Weapon):
    base_name = "Heavy_Crossbow"
    cat = {"Martial", "Ranged", "Main"}
    prop = {"Ammunition", "Heavy", "Loading", "Two-handed"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "100/400 ft"
    Roll = "1d10"
    Cost = 50
    Weight = 18
    lTier = [0, 1, 2, 3]

class Long_bow(Weapon):
    base_name = "Long_bow"
    cat = {"Martial", "Ranged", "Main"}
    prop = {"Ammunition", "Heavy", "Two-handed"}
    dType = "Piercing"
    dMod = "DEX"
    Range = "150/600 ft"
    Roll = "1d8"
    Cost = 50
    Weight = 2
    lTier = [0, 1, 2, 3]

class Padded(Armor):
    base_name = "Padded"
    cat = {"Light", "Primary"}
    bAC = 11
    sDis = True
    sReq = 0
    dMax = 999
    Cost = 5
    Weight = 8
    lTier = [0, 1, 2, 3]

class Leather(Armor):
    base_name = "Leather"
    cat = {"Light", "Primary"}
    bAC = 11
    sDis = False
    sReq = 0
    dMax = 999
    Cost = 10
    Weight = 10
    lTier = [0, 1, 2, 3]

class Studded_Leather(Armor):
    base_name = "Studded_Leather"
    cat = {"Light", "Primary"}
    bAC = 12
    sDis = False
    sReq = 0
    dMax = 999
    Cost = 45
    Weight = 13
    lTier = [0, 1, 2, 3]

class Hide(Armor):
    base_name = "Hide"
    cat = {"Medium", "Primary"}
    bAC = 12
    sDis = False
    sReq = 0
    dMax = 2
    Cost = 10
    Weight = 12
    lTier = [0, 1, 2, 3]

class Chain_Shirt(Armor):
    base_name = "Chain_Shirt"
    cat = {"Medium", "Primary"}
    bAC = 13
    sDis = False
    sReq = 0
    dMax = 2
    Cost = 50
    Weight = 20
    lTier = [0, 1, 2, 3]

class Scale_Mail(Armor):
    base_name = "Scale_Mail"
    cat = {"Medium", "Primary"}
    bAC = 14
    sDis = True
    sReq = 0
    dMax = 2
    Cost = 50
    Weight = 45
    lTier = [0, 1, 2, 3]

class Breastplate(Armor):
    base_name = "Breastplate"
    cat = {"Medium", "Primary"}
    bAC = 14
    sDis = False
    sReq = 0
    dMax = 2
    Cost = 400
    Weight = 20
    lTier = [0, 1, 2, 3]

class Half_Plate(Armor):
    base_name = "Half_Plate"
    cat = {"Medium", "Primary"}
    bAC = 15
    sDis = True
    sReq = 0
    dMax = 2
    Cost = 750
    Weight = 40
    lTier = [0, 1, 2, 3]

class Ring_Mail(Armor):
    base_name = "Ring_Mail"
    cat = {"Heavy", "Primary"}
    bAC = 14
    sDis = True
    sReq = 0
    dMax = 0
    Cost = 30
    Weight = 40
    lTier = [0, 1, 2, 3]

class Chain_Mail(Armor):
    base_name = "Chain_Mail"
    cat = {"Heavy", "Primary"}
    bAC = 16
    sDis = True
    sReq = 13
    dMax = 0
    Cost = 75
    Weight = 55
    lTier = [0, 1, 2, 3]

class Splint(Armor):
    base_name = "Splint"
    cat = {"Heavy", "Primary"}
    bAC = 17
    sDis = True
    sReq = 15
    dMax = 0
    Cost = 200
    Weight = 60
    lTier = [0, 1, 2, 3]

class Shield(Armor):
    base_name = "Shield"
    cat = {"Shield", "Off"}
    bAC = 2
    Cost = 100
    Weight = 6
    lTier = [0, 1, 2, 3]