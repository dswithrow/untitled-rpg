class Consumable:
    def __init__(self, name, sortID, effectList, val, desc):
        self.category = "Consumable"
        self.name = name
        self.sortID = sortID
        self.effect = effectList
        self.value = val
        self.desc = desc


class Weapon:
    def __init__(self, name, sortID, hands, equip, attack, val, desc, spec={}):
        self.category = "Weapon"
        self.name = name
        self.sortID = sortID
        self.hands = hands
        self.equip = equip
        self.attack = attack
        self.value = val
        self.desc = desc
        self.spec = spec

class Gear:
    def __init__(self, name, sortID, weight, equip, stats, val, desc, resist={}):
        self.category = "Gear"
        self.name = name
        self.sortID = sortID
        self.weight = weight
        self.equip = equip
        self.stats = stats
        self.value = val
        self.desc = desc
        self.resist = resist

class Attack:
    def __init__(self, name, category, element, power, wait, animation, mp=0, special=None):
        self.name = name
        self.category = category
        self.element = element
        self.power = power
        self.wait = wait
        self.mp = mp
        self.special = special
        self.animation = animation

class WhiteSpell:
    def __init__(self, name, category, effect, mp, wait, special=None):
        self.name = name
        self.category = category
        self.effect = effect
        self.mp = mp
        self.wait = wait
        self.special = special

# -------------------------------------------------
#      CONSUMABLE LIST
# -------------------------------------------------
# sort 00s are HP restore
herb = Consumable("healing herb", 0, ["RESTORE", "HP", 20], 10, "A common remedy. Restores 20 HP.")
potion = Consumable("potion", 1, ["RESTORE", "HP", 50], 30, "Required for any adventure. Restores 50 HP.")
# sort 10s are MP restore
mpberry = Consumable("magic berry", 10, ["RESTORE", "MP", 20], 15, "A fruit that absorbed mana. Restores 20 MP.")
ether = Consumable("ether", 11, ["RESTORE", "MP", 50], 50, "A go-to for any mage. Restores 50 MP.")
# sort 20s are HP & MP restore
stargel = Consumable("star gel", 20, ["RESTORE", "ALL", 20], 40, "A mysterious, shining goo. Restores 20 HP/MP.")
dstargel = Consumable("deluxe star gel", 21, ["RESTORE", "ALL", 50], 150, "Stargel refined for potency. Restores 50 HP/MP.")
# sort 30s are ailment remove
antidote = Consumable("antidote", 30, ["REMOVE", "POISON"], 15, "A bitter herb. Removes poison.")
eyedrop = Consumable("eye drops", 31, ["REMOVE", "BLIND"], 15, "A dropper of clear liquid. Removes blind.")
smellsalt = Consumable("smelling salt", 32, ["REMOVE", "STUN"], 15, "Snaps you out of a daze. Removes stun.")
# sort 40s are buffs
musclecream = Consumable("muscle cream", 40, ["BUFF", "BUFF-STRENGTH", 1.2, 200], 30, "Topical cream for sore muscles. Buffs strength temporarily.")
focusincense = Consumable("focus incense", 41, ["BUFF", "BUFF-MAGIC", 1.2, 200], 30, "Incense that sharpens the mind. Buffs magic temporarily.")
# sort 50s are damage dealers
throwdagger = Consumable("throwing dagger", 50, ["DAMAGE", "Throwing Dagger", "PHYS", 15, 0], 20, "A common blade designed for throwing. Phys. Power 15.")
blastscroll = Consumable("blast scroll", 55, ["DAMAGE", "Blast", "MAG", "FORCE", 15, 0, 0], 20, "A scroll for a simple force blast. Mag. Power 15.")
# sort 60s are ailment inflicts
toxin = Consumable("toxic vial", 60, ["INFLICT", "POISON", 0.01, 10], 25, "A small vial of dark liquid. Inflicts poison.")
shadowsand = Consumable("shadow sand", 61, ["INFLICT", "BLIND", 150], 25, "Sand as dark as night. Inflicts blind.")
thunderstone = Consumable("thunder stone", 62, ["INFLICT", "STUN", 80], 25, "A rock with concussive force. Inflicts stun.")
# sort 70s are debuffs
lethargygas = Consumable("lethargy gas", 70, ["DEBUFF", "DEB-STRENGTH", 0.8, 200], 30, "A canister of noxious fumes. Lowers strength temporarily.")
disruptcharm = Consumable("disruptive talisman", 71, ["DEBUFF", "DEB-MAGIC", 0.8, 200], 30, "A paper charm that hinders mana. Lowers magic temporarily.")


# -------------------------------------------------
#      WEAPON LIST
# -------------------------------------------------
# sort 00-19 are swords
ironsword = Weapon("iron sword", 0, 1, "SWORD", Attack("Slash", "PHYSICAL", "PHYS", 10, 400, ["SLASH"]), 50, "A basic iron blade. Phys. Power 10")
steelsword = Weapon("steel sword", 1, 1, "SWORD", Attack("Slash", "PHYSICAL", "PHYS", 15, 400, ["SLASH"]), 150, "A sturdy blade to be respected. Phys. Power 15")
rapier = Weapon("rapier", 2, 1, "SWORD", Attack("Thrust", "PHYSICAL", "PHYS", 12, 300, ["PIERCE"]), 250, "A lightweight blade for fast attacks. May hit twice. Phys. Power 12", spec={"R": Attack("Redouble", "PHYSICAL", "PHYS", 10, 300, ["PIERCE"], special={"HITS": 2})})
# sort 20-39 are spears
ironspear = Weapon("iron spear", 20, 2, "SPEAR", Attack("Pierce", "PHYSICAL", "PHYS", 12, 450, ["PIERCE"]), 60, "A spear suitable for a squire. Phys. Power 12")
steelspear = Weapon("steel spear", 21, 2, "SPEAR", Attack("Pierce", "PHYSICAL", "PHYS", 17, 450, ["PIERCE"]), 170, "A heavier spear for extra damage. Phys. Power 17")
toxiclance = Weapon("toxic lance", 22, 2, "SPEAR", Attack("Pierce", "PHYSICAL", "PHYS", 16, 500, ["PIERCE"], special={"INFLICT": ["POSION", 0.01, 20]}), 250, "A wicked lance that sometimes inflicts poison. Power 16")
# sort 40-59 are bows
oakbow = Weapon("oaken bow", 40, 2, "BOW", Attack("Arrow Shot", "PHYSICAL", "PHYS", 8, 400, ["PIERCE"]), 40, "A simple bow of unadorned wood. Phys. Power 8")
supplebow = Weapon("supple bow", 41, 2, "BOW", Attack("Arrow Shot", "PHYSICAL", "PHYS", 11, 400, ["PIERCE"]), 110, "A bow with good draw strength. Phys. Power 11")
enchantbow = Weapon("enchanted bow", 42, 2, "BOW", Attack("Arrow Shot", "PHYSICAL", "PHYS", 13, 400, ["PIERCE"]), 250, "A magical bow that sometimes empowers arrows. Phys. Power 13", spec={"C": Attack("Magic Arrow", "MAGICAL", "PHYS", 15, 400, ["PIERCE"])})
# sort 60+ are staves
beginnerstaff = Weapon("apprentice staff", 60, 2, "STAFF", Attack("Magical Blast", "MAGICAL", "PHYS", 10, 400, ["BLAST"]), 60, "A magical staff for a beginner. Mag. Power 10", spec={"C": Attack("Magical Detonation", "MAGICAL", "PHYS", 10, 500, ["BLAST"], special={"TARGET": "ALL"})})
ashstaff = Weapon("ashen staff", 61, 2, "STAFF", Attack("Firebolt", "MAGICAL", "FIRE", 14, 400, ["BLAST"]), 200, "A staff warm with the fire magic inside. Mag. Power 14", spec={"C": Attack("Bolide", "MAGICAL", "FIRE", 19, 500, ["BLAST"])})
coldstaff = Weapon("cold staff", 62, 2, "STAFF", Attack("Coldsnap", "MAGICAL", "ICE", 14, 400, ["SHATTER"]), 200, "This staff always feels like it was left outside in winter. Mag. Power 14", spec={"C": Attack("Winter Winds", "MAGICAL", "ICE", 14, 500, ["SHATTER"], special={"TARGET": "ALL"})})
boltstaff = Weapon("thunder's call", 63, 2, "STAFF", Attack("Thundershock", "MAGICAL", "ELEC", 14, 400, ["BOLT"]), 200, "The faint hum of electricity can be heard from this staff. Mag. Power 14", spec={"C": Attack("Wild Lightning", "MAGICAL", "ELEC", 12, 500, ["BOLT"], special={"HITS": 5, "TARGET": "RANDOM"})})


# -------------------------------------------------
#      GEAR LIST
# -------------------------------------------------
# gear is sorted by weight and grouped in sets
# sort 000s are light gear
linenbody = Gear("linen armor", 0, "LIGHT", "BODY", [0,0,0,2,0,1,0], 50, "Basic armor, even a peasant could afford it. Def 2/Res 1")
linenhead = Gear("linen helmet", 1, "LIGHT", "HEAD", [0,0,0,1,0,0,0], 20, "Too bad this embarrassing helmet doesn't cover your face. Def 1")
linenhand = Gear("linen gloves", 2, "LIGHT", "HAND", [0,0,0,1,0,0,0], 20, "These gloves are better than nothing. Barely. Def 1")
linenfeet = Gear("linen boots", 3, "LIGHT", "FEET", [0,0,0,1,0,1,0], 35, "These boots keep you warm, at least. Def 1/Res 1")
woodenshield = Gear("wooden shield", 4, "LIGHT", "OFF", [0,0,0,1,0,1,0], 25, "Little more than planks of scrap wood. Def 1/ Res 1")
leatherbody = Gear("leather cuirass", 5, "LIGHT", "BODY", [0,0,0,3,0,2,0], 160, "The kind of armor a new adventurer would be proud to own. Def 3/Res 2")
leatherhead = Gear("leather helmet", 6, "LIGHT", "HEAD", [0,0,0,2,0,0,0], 60, "A helmet great for cushioning blows. Def 2")
leatherhand = Gear("leather gloves", 7, "LIGHT", "HAND", [0,0,0,1,0,1,0], 60, "Supple gloves with ease of movement. Def 1/Res 1")
leatherfeet = Gear("leather boots", 8, "LIGHT", "FEET", [0,0,0,2,0,1,1], 80, "Boots to keep your feet dry in style. Def 2/ Res 1")
leathershield = Gear("leather shield", 9, "LIGHT", "OFF", [0,0,0,2,0,1,0], 70, "Leather over wood, for deflecting attacks. Def 2/Res 1")
# sort 100s are heavy gear
bronzebody = Gear("bronze armor", 100, "HEAVY", "BODY", [0,0,0,3,0,2,-1], 80, "Heavy armor that's a little easy to dent. Def 3/Res 2")
bronzehead = Gear("bronze helmet", 101, "HEAVY", "HEAD", [0,0,0,2,0,0,0], 50, "This helmet is... fine, I guess. Def 2")
bronzehand = Gear("bronze gauntlets", 102, "HEAVY", "HAND", [0,0,0,2,0,0,0], 50, "Good for punching, okay for protecting. Def 2")
bronzefeet = Gear("bronze boots", 103, "HEAVY", "FEET", [0,0,0,2,0,1,-1], 70, "Boots so heavy that every day is leg day. Def 2/Res 1")
bronzeshield = Gear("bronze shield", 104, "HEAVY", "OFF", [0,0,0,2,0,1,0], 70, "A basic shield of bronze. Def 2/Res 1")
steelbody = Gear("steel plate", 105, "HEAVY", "BODY", [0,0,0,4,0,2,-1], 170, "You almost look like a respectable knight. Def 4/Res 2")
steelhead = Gear("steel helmet", 106, "HEAVY", "HEAD", [0,0,0,2,0,1,0], 170, "A helmet so strong, you could headbutt through a wall. Try it! Def 2/ Res 1")
steelhand = Gear("steel gauntlets", 107, "HEAVY", "HAND", [0,0,0,2,0,1,0], 170, "You could catch a sword blade first if you wanted. Def 2/ Res 1")
steelfeet = Gear("steel boots", 108, "HEAVY", "FEET", [0,0,0,3,0,1,-1], 170, "Heavy boots, great for stompin'. Def 3/ Res 1")
steelshield = Gear("steel shield", 109, "HEAVY", "OFF", [0,0,0,3,0,2,0], 160, "A large and sturdy shield with good protection. Def 3/ Res 2")
# sort 200s are cloth gear
apprenticebody = Gear("apprentice robes", 200, "CLOTH", "BODY", [0,10,0,2,0,3,0], 70, "Robes marked with a newbie emblem. Def 2/ Res 3")
apprenticehead = Gear("apprentice headband", 201, "CLOTH", "HEAD", [0,5,0,0,0,2,0], 20, "A headband to help novices focus. Res 2")
apprenticehand = Gear("apprentice gloves", 202, "CLOTH", "HAND", [0,5,0,0,0,2,0], 20, "Gloves to protect from spell mishaps. Res 2")
apprenticefeet = Gear("apprentice shoes", 203, "CLOTH", "FEET", [0,5,0,1,0,2,0], 35, "Soft-soled shoes, common in any village. Def 1/ Res 2")
apprenticefocus = Gear("apprentice focus", 204, "CLOTH", "OFF", [0,10,0,0,1,1,0], 50, "A rudimentary focus for empowering spellcraft. Mag 1/ Res 1")
silkenbody = Gear("silken robes", 205, "CLOTH", "BODY", [0,20,0,3,1,6,0], 130, "Soft robes detailed with arcane runes. Def 3/ Res 6", resist={"FORCE": 0.75})
silkenhead = Gear("silken hat", 206, "CLOTH", "HEAD", [0,10,0,1,0,4,0], 55, "A wide brimmed hat that keeps cool. Def 1/ Res 4")
silkenhand = Gear("silken gloves", 207, "CLOTH", "HAND", [0,10,0,1,0,4,0], 55, "Beautiful gloves for an accomplished mage. Def 1/Res 4")
silkenfeet = Gear("silken boots", 208, "CLOTH", "FEET", [0,10,0,2,0,4,0], 75, "Boots so soft, it's like walking on clouds. Def 2/ Res 4")
sturdyfocus = Gear("sturdy focus", 209, "CLOTH", "OFF", [0,20,0,1,1,2,0], 130, "An arcane focus that amplifies barriers. Mag 1/ Def 1/ Res 2")
# sort 300s are accessories
hpcharm = Gear("health charm", 30, "ACC", "ACC", [20,0,0,0,0,0,0], 200, "A red charm shaped like a heart. Max HP 20")
mpcharm = Gear("mental charm", 30, "ACC", "ACC", [0,20,0,0,0,0,0], 200, "A blue charm etched with a circle. Max MP 20")
strcharm = Gear("muscle charm", 30, "ACC", "ACC", [0,0,2,0,0,0,0], 200, "A black charm shaped like a blade. Str 2")
defcharm = Gear("sturdy charm", 30, "ACC", "ACC", [0,0,0,2,0,0,0], 200, "A brown charm shaped like a shield. Def 2")
magcharm = Gear("focus charm", 30, "ACC", "ACC", [0,0,0,0,2,0,0], 200, "A pink charm shaped like a star. Mag 2")
rescharm = Gear("will charm", 30, "ACC", "ACC", [0,0,0,0,0,2,0], 200, "A purple charm polished into a sphere. Res 2")
spdcharm = Gear("quick charm", 30, "ACC", "ACC", [0,0,0,0,0,0,2], 200, "A green charm shaped like a wing. Spd 2")
firecharm = Gear("fire charm", 307, "ACC", "ACC", [0,0,0,0,0,0,0], 100, "An orange charm etched with a campfire. Resist fire 10%", resist={"FIRE": 0.9})
frostcharm = Gear("frost charm", 308, "ACC", "ACC", [0,0,0,0,0,0,0], 100, "A white charm etched with a snowman. Resist ice 10%", resist={"ICE": 0.9})
eleccharm = Gear("shock charm", 309, "ACC", "ACC", [0,0,0,0,0,0,0], 100, "a yellow charm shaped like a lightning bolt. Resist shock 10%", resist={"ELEC": 0.9})