import pygame as pg
from . import dex, items
from ... import prepare

baseStatKeys = ['BASEHP', 'BASEMP', 'BASESTRENGTH', 'BASEDEFENSE', 'BASEMAGIC', 'BASERESISTANCE', 'BASESPEED']
totalStatKeys = ['MAXHP', 'MAXMP', 'STRENGTH', 'DEFENSE', 'MAGIC', 'RESISTANCE', 'SPEED']
# ally_coords = [(710, 45), (610, 95), (505, 150), (400, 200)]
# ally_coords = [(610, 85), (540, 115), (505, 150), (400, 200)]
ally_coords = [(630, 105), (560, 135), (525, 170), (420, 220)]


class Unit:
    def __init__(self, name, level, stats):
        self.type = "Unit"
        self.name = name
        self.battle_sprite = None
        self.portrait = None
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.renderLoc = (0,0)
        self.level = level
        self.hp = stats[0]
        self.mp = stats[1]
        self.wait = 0
        self.stats = {
            "BASEHP": stats[0],
            "MAXHP": stats[0],
            "BASEMP": stats[1],
            "MAXMP": stats[1],
            "BASESTRENGTH": stats[2],
            "STRENGTH": stats[2],
            "BASEDEFENSE": stats[3],
            "DEFENSE": stats[3],
            "BASEMAGIC": stats[4],
            "MAGIC": stats[4],
            "BASERESISTANCE": stats[5],
            "RESISTANCE": stats[5],
            "BASESPEED": stats[6],
            "SPEED": stats[6],
        }
        self.resist = {}
        self.conditions = {}
        self.ko = False
        self.defend = False


class Monster(Unit):
    def __init__(self, species, level=1):
        self.type = "Monster"
        self.mon = dex.monsterDex[species]
        statHolder = self.mon["stats"][:]
        if level > 1:
            self.monsterLeveller(level, statHolder, self.mon["family"], self.mon["gold"])
        super().__init__(name=self.mon["name"], level=level, stats=statHolder)
        self.species = species
        self.resist = self.mon["resist"]
        self.gold = self.mon["gold"] if level == 1 else statHolder[-1]
        self.exp = sum(statHolder[2:7]) + statHolder[0]//10 + statHolder[1]//5

    def monsterLeveller(self, level, stats, family, gold):
        level -= 1
        growth = dex.familyGrowthRate[family]
        stats[0] += int(growth[0] * level) * 10
        stats[1] += int(growth[1] * level) * 5
        for i in range(2, 7):
            stats[i] += int(growth[i] * level)
        stats.append(gold + int(growth[7] * gold * level))
        return stats


class PlayerCharacter(Unit):
    def __init__(self, name, job):
        self.type = "PlayerCharacter"
        self.job = dex.jobDex[job]
        self.exp = 0
        self.nextLevel= 100
        self.statHolder = [0,0,0,0,0,0,0]
        super().__init__(name = name, level = 1, stats=self.job["stats"])
        self.equip = {
            "main": None,
            "off": None,
            "head": None,
            "body": None,
            "hands": None,
            "feet": None,
            "acc": None
        }
        self.equipStats = [0,0,0,0,0,0,0]

    def updateStats(self):
        updater = []
        for gear in self.equip.values():
            if gear and gear.type == "Gear":
                # print(f"{self.name}, {gear.name} {gear.stats}")
                updater.append(gear.stats[:])
        self.equipStats = [sum(stats) for stats in zip(*updater)]
        # print(f"{self.name}, equip total: {self.equipStats}")
        for i in range(7):
            self.stats[totalStatKeys[i]] = self.stats[baseStatKeys[i]] + self.equipStats[i]
        if self.hp > self.stats["MAXHP"]:
            self.hp = self.stats["MAXHP"]
        if self.mp > self.stats["MAXMP"]:
            self.mp = self.stats["MAXMP"]
        # print(self.stats.items())

    def levelUp(self):
        self.exp -= self.nextLevel
        self.nextLevel = int(self.nextLevel * 1.1)
        self.level += 1
        level_announcement = [f"{self.name} is now level {self.level}!", ""]
        for i in range(7):
            self.statHolder[i] += self.job["growth"][i]
            while self.statHolder[i] > 1:
                self.statHolder[i] -= 1
                if i == 0:
                    self.stats[baseStatKeys[i]] += 10
                    level_announcement[1] += "HP increased! "
                elif i == 1:
                    self.stats[baseStatKeys[i]] += 5
                    level_announcement[1] += "MP increased! "
                else:
                    self.stats[baseStatKeys[i]] += 1
                    level_announcement += f"{totalStatKeys[i].title()} increased! "
        self.updateStats()
        return level_announcement

class Party:
    def __init__(self):
        self.gold = 100
        self.inventory = {
            "Consumable":{
                items.herb.name: [items.herb, 3],
                items.mpberry.name: [items.mpberry, 2],
                items.stargel.name: [items.stargel, 1],
                items.throwdagger.name: [items.throwdagger, 2],
                items.blastscroll.name: [items.blastscroll, 2],
                items.potion.name: [items.potion, 1],
                items.ether.name: [items.ether, 1],
            },
            "Weapon":{
                items.steelsword.name: [items.steelsword, 1],
                items.rapier.name: [items.rapier, 1],
                items.steelspear.name: [items.steelspear, 1],
                items.toxiclance.name: [items.toxiclance, 1],
                items.supplebow.name: [items.supplebow, 1],
                items.enchantbow.name: [items.enchantbow, 1],
                items.ashstaff.name: [items.ashstaff, 1],
                items.coldstaff.name: [items.coldstaff, 1],
                items.boltstaff.name: [items.boltstaff, 1],
            },
            "Gear":{
                items.leatherbody.name : [items.leatherbody, 1],
                items.leatherhead.name : [items.leatherhead, 1],
                items.leatherhand .name : [items.leatherhand, 1],
                items.leatherfeet.name : [items.leatherfeet, 1],
                items.leathershield .name : [items.leathershield, 1],
                items.steelbody.name : [items.steelbody, 1],
                items.steelhead .name : [items.steelhead, 1],
                items.steelhand.name : [items.steelhand, 1],
                items.steelfeet.name : [items.steelfeet, 1],
                items.silkenbody.name : [items.silkenbody, 2],
                items.silkenhead .name : [items.silkenhead, 2],
                items.silkenhand.name : [items.silkenhand, 2],
                items.silkenfeet.name : [items.silkenfeet, 2],
                items.sturdyfocus.name : [items.sturdyfocus, 1],
                items.hpcharm .name : [items.hpcharm, 4],
                items.mpcharm .name : [items.mpcharm, 4],
                items.strcharm .name : [items.strcharm, 4],
                items.defcharm.name : [items.defcharm, 4],
                items.magcharm.name : [items.magcharm, 4],
                items.rescharm.name : [items.rescharm, 4],
                items.spdcharm.name : [items.spdcharm, 4],
                items.firecharm .name : [items.firecharm, 4],
                items.frostcharm .name : [items.frostcharm, 4],
                items.eleccharm .name : [items.eleccharm, 4],
            }
        }
        self.units = []

    def add_member(self, chara: PlayerCharacter):
        self.units.append(chara)
        return self



anna = PlayerCharacter("Anna", "swordsman")
anna.equip["main"] = items.ironsword
anna.equip["off"] = items.woodenshield
anna.equip["head"] = items.linenhead
anna.equip["body"] = items.linenbody
anna.equip["hands"] = items.linenhand
anna.equip["feet"] = items.linenfeet
anna.equip["acc"] = items.spdcharm
anna.updateStats()
anna.battle_sprite = prepare.ALLIES["swordsman_battle"]
anna.portrait = prepare.SPRITES["swordsman_portrait"]
anna.renderLoc = ally_coords[0]

elise = PlayerCharacter("Elise", "cleric")
elise.equip["main"] = items.oakbow
elise.equip["head"] = items.apprenticehead
elise.equip["body"] = items.apprenticebody
elise.equip["hands"] = items.apprenticehand
elise.equip["feet"] = items.apprenticefeet
elise.equip["acc"] = items.rescharm
elise.updateStats()
elise.battle_sprite = prepare.ALLIES["cleric_battle"]
elise.portrait = prepare.SPRITES["cleric_portrait"]
elise.renderLoc = ally_coords[1]

xavier = PlayerCharacter("Xavier", "wizard")
xavier.equip["main"] = items.beginnerstaff
xavier.equip["off"] = items.apprenticefocus
xavier.equip["head"] = items.apprenticehead
xavier.equip["body"] = items.apprenticebody
xavier.equip["hands"] = items.apprenticehand
xavier.equip["feet"] = items.apprenticefeet
xavier.equip["acc"] = items.magcharm
xavier.updateStats()
xavier.battle_sprite = prepare.ALLIES["wizard_battle"]
xavier.portrait = prepare.SPRITES["wizard_portrait"]
xavier.renderLoc = ally_coords[2]

beau = PlayerCharacter("Beau", "knight")
beau.equip["main"] = items.ironspear
beau.equip["head"] = items.bronzehead
beau.equip["body"] = items.bronzebody
beau.equip["hands"] = items.bronzehand
beau.equip["feet"] = items.bronzefeet
beau.equip["acc"] = items.strcharm
beau.updateStats()
beau.battle_sprite = prepare.ALLIES["knight_battle"]
beau.portrait = prepare.SPRITES["knight_portrait"]
beau.renderLoc = ally_coords[3]

start_party = Party().add_member(anna).add_member(elise).add_member(xavier).add_member(beau)