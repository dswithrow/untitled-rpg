import random, pygame as pg
from . import units
from ... import prepare

screen = pg.display.get_surface()

#----------------------------------------------------------------------
#   BATTLE FUNCTIONS
#----------------------------------------------------------------------
def defend(user: "PlayerCharacter or Monster"):
    """Activates unit's defend flag, should always target self."""
    user.defend = True
    user.wait = int(0.4 * (100 - user.stats["SPEED"]))

def restore(effect: list, target: "PlayerCharacter or Monster"):
    """Expecting a list slice of effect, e.g. ['HP', 50] and the unit ref of the target"""
    heal = effect[1]
    if target.ko:
        return
    if "ALL" in effect or "HP" in effect:
        if target.hp + heal > target.stats["MAXHP"]:
            target.hp = target.stats["MAXHP"]
        else:
            target.hp += heal
    if "ALL" in effect or "MP" in effect:
        if target.mp + heal > target.stats["MAXMP"]:
            target.mp = target.stats["MAXMP"]
        else:
            target.mp += heal

def buff(effect: list, target: "PlayerCharacter or Monster"):
    """Expecting a list of the effect, e.g. ['BUFF-STRENGTH', 1.2, 200]."""
    buffs = target.conditions.keys()
    direction, stat = effect[0].split("-")
    opp = f"{'BUFF' if direction == 'DEB' else 'DEB'}-{stat}"
    if effect[0] in buffs:
        if direction == "BUFF" and target.conditions[effect[0]][0] * target.conditions[effect[0]][1] > effect[1] * effect[2]:
            return
        if direction == "DEB" and (target.conditions[effect[0]][0] - 1) * target.conditions[effect[0]][1] < (effect[1] - 1) * effect[2]:
            return
        buffReset(effect[0], target)
    if opp in buffs:
        buffReset(opp, target)
    target.stats[stat] *= effect[1]
    target.conditions[effect[0]] = effect[1:]


def buffReset(buff: str, target: "PlayerCharacter or Monster"):
    """Expecting a string of buff/debuff, e.g. 'DEB-STRENGTH'."""
    statIndex = units.totalStatKeys.index(buff.split("-")[1])
    target.conditions.pop(buff, None)
    target.stats[totalStatKeys[statIndex]] = target.stats[units.baseStatKeys[statIndex]]
    if type(target) == "PlayerCharacter":
        target.stats[units.totalStatKeys[statIndex]] += target.equipStats[statIndex]


def remove(effect: str, target: "PlayerCharacter or Monster"):
    """Expecting a string of a condition, e.g. 'POISON', to remove from target.
    Some special strings, e.g. 'DISPEL' or 'PANACEA' can remove multiple of a set category."""
    if effect == "KO":
        target.ko = False
        target.hp = int(target.stats["MAXHP"] / 2)
        return
    if not target.conditions:
        return
    conditions = target.conditions.keys()
    if effect == "PANACEA":
        # Panacea removes ailments, but not buffs/debuffs
        conditions = filter(lambda x: "-" not in x, conditions)
        for ail in conditions:
            target.conditions.pop(ail, None)
        return
    if effect == "DISPEL":
        conditions = filter(lambda x: "-" in x, conditions)
        for key in conditions:
            buffReset(key, target)
        return
    if effect == "BREAK":
        for key in conditions:
            if "BUFF-" in key:
                buffReset(key, target)
        return
    if effect == "MEND":
        for key in conditions:
            if "DEB-" in key:
                buffReset(key, target)
        return
    target.conditions.pop(effect, None)


def inflict(ailment: list, target: "PlayerCharacter or Monster"):
    """Expecting an ailment list, e.g. ['POISON', 0.05, 200]. Attempts to afflict the target with the status ailment."""
    name = ailment[0]
    if name in target.resist.keys():
        if random.random() > target.resist[name]:
            return
    if name in target.conditions.keys():
        oldCon = target.conditions[name]
        if name in ["POISON", "BURN"]:
            # if new(frequency / intensity) is stronger than remaining(frequency / intensity)
            if ailment[2] / ailment[1] < oldCon[1] / oldCon[2]:
                oldCon[0], oldCon[1] = ailment[1], ailment[2]
        else:
            if ailment[1] > oldCon[0]:
                oldCon[0] = ailment[1]
        return
    target.conditions[name]= ailment[1:]

def targeting(enemies_size: int, target: "list or string", hits: int):
    """Returns a list of target indices."""
    if type(target) is not str:
        target *= hits
    elif target == "ALL":
        target = list(range(enemies_size))
        if hits > 1:
            extraTarget = target[:]
        for i in range(1, hits):
            target.extend(extraTarget)
    elif target == "RANDOM":
        target = []
        for i in range(hits):
            target.append(random.randint(0, enemies_size - 1))
    return target

#   ORIGINAL ATTACK PROCESS, keep around until new one is fully tested
#
# def attackProcess(attack: list, attacker: "PlayerCharacter or Monster", enemies: list, targetID: int):
#     """Takes the details out of the attack's list and implements them."""
#     attack = attack[:]
#     hits, target, ail = 1, [targetID], None
#     anim = attack[-1] if type(attack[-1]) is list else attack [-2]
#     if type(attack[-1]) is dict:    # handles special attack keys
#         hits =  attack[-1]["HITS"] if "HITS" in attack[-1].keys() else hits
#         target =  attack[-1]["TARGET"] if "TARGET" in attack[-1].keys() else target
#         ail =  attack[-1]["INFLICT"][:] if "INFLICT" in attack[-1].keys() else None
#     target = targeting(len(enemies), target, hits)
#     attackName = attack[0]
#     attackType = attack[1]
#     if attackType == "MAG":
#         element = attack.pop(2)
#         attacker.mp -= attack.pop(3)
#         attackerPower = attacker.stats["MAGIC"]
#     else:
#         element = "PHYS"
#         attackerPower = attacker.stats["STRENGTH"]
#         attackerPower *= 0.6 if "BURN" in attacker.conditions.keys() else 1
#     power = attack[2]
#     power *= attacker.stats["STRENGTH"] if attackType == "PHYS" else attacker.stats["MAGIC"]
#     wait = attack[3] * (100 - attacker.stats["SPEED"]) / 100
#     for i in target:
#         roll = random.random()
#         targetSpeed = 1 if "STUN" in enemies[i].conditions.keys() else enemies[i].stats["SPEED"]
#         hitChance = ((attacker.stats["SPEED"] + attackerPower/10) / targetSpeed)
#         hitChance *= 0.6 if "BLIND" in attacker.conditions.keys() else 1
#         hitCheck = roll < hitChance
#         if hitCheck:
#             critCheck = roll < hitChance / 10
#             resist = enemies[i].resist[element] if element in enemies[i].resist.keys() else 1
#             damage = power * resist * (random.randint(95, 105)/100)
#             if critCheck:
#                 damage *= 2
#                 print("Critical hit!")
#             damage /= 2 if enemies[i].defend else 1
#             damage /= enemies[i].stats["DEFENSE"] if element == "PHYS" else enemies[i].stats["RESISTANCE"]
#             damage = int(damage)
#             enemies[i].hp -= damage
#             if enemies[i].hp < 0:
#                 enemies[i].ko = True
#                 enemies[i].hp = 0
#             print(f"\n{attacker.name}'s {attackName} dealt {damage} damage to {enemies[i].name}!")
#             print(f"{enemies[i].name} {enemies[i].hp}/{enemies[i].stats['MAXHP']}\n")
#             if ail and not enemies[i].ko:
#                 inflict(ail, enemies[i])
#         else:
#             print(f"\n{attacker.name} missed!")
#     attacker.wait = wait // 10


def attackProcess(attack: "Attack", attacker: "PlayerCharacter or Monster", enemies: list, targetID: int):
    """Reads the details of the Attack object and implments them."""
    hits, target, ail = 1, [targetID], None
    damageRange, critChance, critMultiplier = (95, 105), 0.1, 2
    if (attack.special):
        hits = attack.special["HITS"] if "HITS" in attack.special.keys() else 1
        target = attack.special["TARGET"] if "TARGET" in attack.special.keys() else target
        ail = attack.special["INFLICT"] if "INFLICT" in attack.special.keys() else None
        damageRange = attack.special["DAMAGE RANGE"] if "DAMAGE RANGE" in attack.special.keys() else damageRange
        critChance = attack.special["CRIT CHANCE"] if "CRIT CHANCE" in attack.special.keys() else critChance
        critMultiplier = attack.special["CRIT MULTIPLIER"] if "CRIT MULTIPLIER" in attack.special.keys() else critMultiplier
    target = targeting(len(enemies), target, hits)
    if attack.category == "MAGICAL":
        attackerPower = attacker.stats["MAGIC"]
        attackerPower *= 0.6 if "MUDDLE" in attacker.conditions.keys() else 1
    else:
        attackerPower = attacker.stats["STRENGTH"]
        attackerPower *= 0.6 if "BURN" in attacker.conditions.keys() else 1
    attackerPower *= 0.8 if "LETHARGY" in attacker.conditions.keys() else 1
    power = attack.power * attackerPower
    for i in target:
        roll = random.random()
        targetSpeed = 1 if "STUN" in enemies[i].conditions.keys() else enemies[i].stats["SPEED"]
        hitChance = ((attacker.stats["SPEED"] + attackerPower/10) / targetSpeed)
        hitChance *= 0.6 if "BLIND" in attacker.conditions.keys() else 1
        hitCheck = roll < hitChance
        if hitCheck:
            critCheck = roll < critChance
            resist = enemies[i].resist[attack.element] if attack.element in enemies[i].resist.keys() else 1
            damage = power * resist * (random.randint(damageRange[0], damageRange[1])/100)
            if critCheck:
                damage *= critMultiplier
                print("Critical hit!")
            damage /= 2 if enemies[i].defend else 1
            damage //= enemies[i].stats["DEFENSE"] if attack.category == "PHYSICAL" else enemies[i].stats["RESISTANCE"]
            enemies[i].hp -= damage
            if enemies[i].hp < 0:
                enemies[i].ko = True
                enemies[i].hp = 0
            print(f"\n{attacker.name}'s {attack.name} dealt {damage} damage to {enemies[i].name}!")
            print(f"{enemies[i].name} {enemies[i].hp}/{enemies[i].stats['MAXHP']}\n")
            if ail and not enemies[i].ko:
                inflict(ail, enemies[i])
        else:
            print(f"\n{attacker.name} missed!")
    attacker.wait = attack.wait * (100 - (1 if "STUN" in attacker.conditions.keys() else attacker.stats["SPEED"])) // 1000


def whiteMagicFilter(spell: "WhiteSpell", caster: "PlayerCharacter or Monster", target_team: list, target_id: int):
    """Expecting the full Spell object."""
    target, hits = [target_id], 1
    if spell.special:
        target = spell.special["TARGET"] if "TARGET" in spell.special.keys() else target
        hits = spell.special["HITS"] if "HITS" in spell.special.keys() else 1
    target = targeting(len(target_team), target, hits)
    for i in target:
        if spell.category == "RESTORE":
            power = spell.effect[1] * caster.stats["MAGIC"] // 4
            restore([spell.effect[0], power], target_team[i])
        elif spell.category == "REMOVE":
            remove(spell.effect, target_team[i])
        elif spell.category == "BUFF":
            buff(spell.effect, target_team[i])
        elif spell.category == "INFLICT":
            inflict(spell.effect, target_team[i])
    caster.mp -= spell.mp
    caster.wait = spell.wait * (100 - (1 if "STUN" in caster.conditions.keys() else caster.stats["SPEED"])) // 1000

def itemFilter(effect: list, user: "PlayerCharacter or Monster", target_team: list, target_id: int):
    """Expecting the full item effect list, e.g. ["DAMAGE", "Throwing Dagger", "PHYS", 15, 0]"""
    target, hits = [target_id], 1
    if type(effect[-1]) is dict:
        target = effect[-1]["TARGET"] if "TARGET" in effect[-1].keys() else target
        hits = effect[-1]["HITS"] if "HITS" in effect[-1].keys() else 1
        effect.pop()
    target = targeting(len(target_team), target, hits)
    for val in target:
        if effect[0] =="DAMAGE":
            attackProcess(effect[1:], user, target_team, val)
        elif effect[0] == "RESTORE":
            restore(effect[1:], target_team[val])
        elif effect[0] == "REMOVE":
            remove(effect[-1], target_team[val])
        elif effect[0][-4:] == "BUFF":
            buff(effect[1:], target_team[val])
        elif effect[0] == "INFLICT":
            inflict(effect[1:], target_team[val])
    user.wait = int(0.4 * (100 - user.stats["SPEED"]))

def killEXP(monster: list):
    """Expecting the monster's self.stats list. Calculates and returns how much exp that monster is worth."""
    exp = monster["BASEHP"] // 10
    exp += monster["BASEMP"] // 5
    for i in range(2, 7):
        exp += monster[units.baseStatKeys[i]]
    return exp

def dropItem(item_drop: dict):
    """Expecting the monster's item drop dict. Returns an item ref if the monster drops an item."""
    roll = random.randint(1, 100)
    if roll > 20:
        return False
    if roll == 1 and "UR" in item_drop.keys():
        return item_drop["UR"]
    if roll < 6 and "MR" in item_drop.keys():
        return item_drop["MR"]
    if roll < 11 and "R" in item_drop.keys():
        return item_drop["R"]
    if "C" in item_drop.keys():
        return item_drop["C"]

def trySpec(weapon: dict):
    """Expecting the weapon's self.spec dict. Rolls to determine which, if any, special attacks should be used"""
    roll = random.randint(1, 100)
    if roll > 20:
        return False
    if roll == 1 and "UR" in weapon.keys():
        return weapon["UR"]
    if roll < 6 and "MR" in weapon.keys():
        return weapon["MR"]
    if roll < 11 and "R" in weapon.keys():
        return weapon["R"]
    if "C" in weapon.keys():
        return weapon["C"]

