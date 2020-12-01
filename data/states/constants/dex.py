from . import items

monsterDex = {
    "blueslime": {  # Low power cannon fodder, relatively high def
        "name": "Slime",
        "family": "SLIME",
        "stats": [30, 5, 7, 12, 1, 5, 7],
        "gold": 10,
        "item": {
            "C": items.herb,
            "MR": items.stargel
        },
        "moves": {
            "basic": items.Attack("Slam", "PHYSICAL", "PHYS", 10, 400, ["SLASH"])
        },
        "resist": {
            "PHYS": .75,
            "FIRE": 1.5
        }
    },
    "greenslime": {  # Low power cannon fodder, capable of healing
        "name": "Green Slime",
        "family": "SLIME",
        "stats": [40, 20, 6, 10, 8, 6, 7],
        "gold": 10,
        "item": {
            "C": items.herb,
            "R": items.mpberry,
            "MR": items.stargel
        },
        "moves": {
            "basic": items.Attack("Slam", "PHYSICAL", "PHYS", 10, 400, ["SLASH"]),
            "heal": items.WhiteSpell("Restorative Goo", "RESTORE", ["HP", 15], 10, 500)
        },
        "resist": {
            "PHYS": .75,
            "FIRE": 1.5
        }
    },
    "floateye": {  # First toughie, low defenses but higher attack
        "name": "Floating Eye",
        "family": "AHRIMAN",
        "stats": [50, 20, 10, 8, 6, 8, 12],
        "gold": 15,
        "item": {
            "C": items.eyedrop,
            "R": items.potion,
            "MR": items.thunderstone
        },
        "moves": {
            "basic": items.Attack("Bite", "PHYSICAL", "PHYS", 10, 400, ["FANG"]),
            "spell": items.Attack("Beam", "MAGICAL", "PHYS", 20, 500, ["BEAM"], mp=10)
        },
        "resist": {
            "ELEC": 1.5
        }
    },
    "goblin": {  # Balanced starter monster
        "name": "Goblin",
        "family": "GOBLIN",
        "stats": [60, 10, 12, 10, 1, 10, 10],
        "gold": 20,
        "item": {
                "C": items.herb,
                "R": items.potion,
                "MR": items.throwdagger
        },
        "moves": {
            "basic": items.Attack("Punch", "PHYSICAL", "PHYS", 15, 400, ["BASH"])
        },
        "resist": {
            "FIRE": .75
        }
    }
}


familyGrowthRate = {
    #   [hp, mp, str, def, mag, res, spd, gold]
    "SLIME": [1, .5, .34, .67, .34, .5, .2, .3], # 3.5333...
    "GOBLIN": [1.5, .25, .34, .5, .34, .34 , .34, .4], # 3.5833...
    "AHRIMAN": [1, .67, .5, .2, .34, .2, .75, .3], # 3.65
}


jobDex = {
    "swordsman": {
        "name": "swordsman",
        "stats": [50, 20, 12, 11, 8, 8, 12],
        "growth": [1, .25, .4, .35, .25, .25, .5],
        "equipment": ["SWORD", "LIGHT", "CLOTH", "ACC", "OFF"],
    },
    "cleric": {
        "name": "cleric ",
        "stats": [30, 40, 8, 9, 10, 13, 9],
        "growth": [.8, .5, .25, .25, .4, .4, .4],
        "equipment": ["BOW", "CLOTH", "ACC"],
    },
    "wizard": {
        "name": "wizard",
        "stats": [20, 40, 7, 7, 14, 12, 10],
        "growth": [.7, .5, .2, .2, .5, .4, .5],
        "equipment": ["STAFF", "CLOTH", "ACC", "OFF"],
    },
    "knight": {
        "name": "knight",
        "stats": [70, 10, 14, 14, 8, 8, 8],
        "growth": [1.2, .2, .5, .5, .2, .2, .2],
        "equipment": ["SPEAR", "LIGHT", "HEAVY", "ACC"],
    },
    
}