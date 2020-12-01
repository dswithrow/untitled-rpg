import pygame as pg, pygame_gui, random
from os import path
from .. import prepare, tools, sprites
from .constants import items, map_info, dex, units, mechanics

# aliases for legibility
bestiary = dex.monsterDex
enemy = units.Monster
ally = units.PlayerCharacter
gui = pygame_gui.elements
select = pygame_gui.elements.ui_selection_list.UISelectionList
textbox = pygame_gui.elements.ui_text_box.UITextBox

# menu elements
command_list = ["ATTACK", "ITEM", "DEFEND", "RUN"]
test_list = [("ONE", "TWO"), ("THREE", "FOUR")]
hidden = (800, 200)
manager = pygame_gui.UIManager((800, 600))
menu = gui.ui_panel.UIPanel(   relative_rect=pg.Rect((0, 400), (800, 200)),
                starting_layer_height=1, manager=manager, object_id="base_menu")
# hp_panel = select(  relative_rect=pg.Rect((206,0), (294, 194)), item_list=[],
#                     starting_height=2, manager=manager, container=menu, object_id="hp_panel")
command_panel = select( relative_rect=pg.Rect((500,0), (294, 194)), item_list=command_list,
                        starting_height=2, manager=manager, container=menu, object_id="command_panel")

# battle render coordinates
enemy_coords = [(100, 0), (50, 100), (250, 50)]



class Battle(tools._State):
    """
    This is the state for battling 
    """
    def __init__(self):
        tools._State.__init__(self)
        self.next = "OVERWORLD"
        self.enemies = []
        self.enemy_name_list = []
        self.allies = []
        self.ally_name_list = []
        self.all_combatants = []
        self.current_actor = None
        self.consumables = {}
        self.consumables_names = []
        self.gold = 0
        self.exp = 0
        self.items = []
        self.command_flag = ""
        self.using_item = ""



    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time
        if "PARTY" not in self.persist:
            self.form_party()
        self.get_allies()
        self.get_encounter(self.persist["MAP"])
        self.all_combatants = self.allies + self.enemies
        self.roll_initiative()


    def get_encounter(self, location):
        dupe_name, repeat, suffix = "", 0, [" A", " B", " C"]
        encounter = map_info.map_info[location]["ENCOUNTERS"]
        level_range = map_info.map_info[location]["LEVEL"]
        level = level_range[0] if level_range[0] >= self.player_level else min(self.player_level, level_range[1])
        roll = random.randint(0, len(encounter) - 1)
        encounter = encounter[roll]
        self.enemies = []
        self.enemy_name_list = []
        for i in range(len(encounter)):
            self.enemies.append(enemy(encounter[i], level))
            if dupe_name == encounter[i] or encounter[i] in encounter[i + 1:]:
                dupe_name = encounter[i]
                self.enemies[-1].name += suffix[repeat]
                repeat += 1
            self.enemies[-1].battle_sprite = prepare.MONSTERS[encounter[i]]
            self.enemies[-1].renderLoc = enemy_coords[i]
            self.enemy_name_list.append(self.enemies[-1].name)


    def get_allies(self):
        self.allies = []
        self.player_level = 0
        for chara in self.persist["PARTY"].units:
            self.allies.append(chara)
            self.player_level += chara.level


    def form_party(self):
        self.persist["PARTY"] = units.start_party


    def roll_initiative(self):
        for chara in self.all_combatants:
            chara.wait = random.randint(100, 600) * (100 - chara.stats["SPEED"]) // 1000
        self.get_next_turn()


    def get_next_turn(self):
        self.all_combatants.sort(key=lambda x: x.wait)
        self.current_actor = self.all_combatants[0]
        self.current_actor.defend = False
        lowest_wait = self.current_actor.wait
        for chara in self.all_combatants:
            chara.wait -= lowest_wait
            if chara.ko:
                chara.wait += lowest_wait
            # if chara.conditions:  For eventual buff/ailment implementation
            #     pass
        print(f"{self.current_actor.name}'s turn!")
        if self.current_actor in self.allies:
            command_panel.set_item_list(command_list)
            self.command_flag = ""
            self.using_item = ""
            self.enemy_name_list = [x.name for x in self.enemies]
            self.ally_name_list = [x.name for x in self.allies]
        else:
            command_panel.set_item_list([])
            self.enemy_turn()


    def enemy_turn(self):
        targeting_list = random.sample(range(4), 4)
        target = None
        for index in targeting_list:
            if not self.allies[index].ko:
                target = index
                break
        if target == None:
            return
        move = self.current_actor.mon["moves"]["basic"]
        mechanics.attackProcess(
            move,
            self.current_actor,
            self.allies,
            target
        )
        self.ko_handler()
        self.get_next_turn()


    def ko_handler(self):
        ally_ko = 0
        for ally in self.allies:
            if ally.ko:
                ally_ko += 1
        if ally_ko == 4:
            # add a game over state change here
            self.done = True

        last_index = len(self.enemies) - 1
        for i in range(last_index, -1, -1):
            if self.enemies[i].ko:
                self.exp += mechanics.killEXP(self.enemies[i].stats)
                self.gold += self.enemies[i].gold
                drop = mechanics.dropItem(self.enemies[i].mon["item"])
                if drop:
                    self.items.append(drop)
                del self.enemies[i]
        if not self.enemies:
            # victory
            self.persist["PARTY"].gold += self.gold
            print(f"Gained {self.gold} gold! New total is {self.persist['PARTY'].gold}")
            for item in self.items:
                print(f"Found {item.name}!")
                if item.name in self.persist["PARTY"].inventory[item.type].keys():
                    self.persist["PARTY"].inventory[item.type][item.name][1] += 1
                else:
                    self.persist["PARTY"].inventory[item.type][item.name] = [item, 1]
            self.exp /= 4 - ally_ko
            print(f"Gained {int(self.exp)} experience!")
            for ally in self.allies:
                if not ally.ko:
                    ally.exp += int(self.exp)
                    if ally.exp > ally.nextLevel:
                        print(ally.levelUp())
            self.done = True


    def try_flee(self):
        enemy_speed = sum([0 if x.ko else x.stats["SPEED"] for x in self.enemies])
        ally_speed = sum([0 if x.ko else x.stats["SPEED"] for x in self.allies])
        escape = (ally_speed - enemy_speed + 60) < random.randint(1, 100)
        if escape:
            self.done = True
        else:
            self.current_actor.wait = (100 - self.current_actor.stats["SPEED"]) // 0.4
            self.get_next_turn()


    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            if event.key == pg.K_SPACE:
                self.done = True
            if event.key == pg.K_RETURN:
                self.get_next_turn()

        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                # print(f"{self.command_flag} {command_panel.get_single_selection()}")
                #
                #   ATTACK
                #
                if command_panel.get_single_selection() == "ATTACK":
                    self.command_flag = "ATTACK"
                    command_panel.set_item_list(self.enemy_name_list + ["BACK"])
                if self.command_flag == "ATTACK" and command_panel.get_single_selection() in self.enemy_name_list:
                    target = self.enemy_name_list.index(command_panel.get_single_selection())
                    spec = None
                    if self.current_actor.equip["main"].spec:
                        spec = mechanics.trySpec(self.current_actor.equip["main"].spec)
                    move = spec if spec else self.current_actor.equip["main"].attack
                    mechanics.attackProcess(
                        move,
                        self.current_actor,
                        self.enemies,
                        target
                    )
                    self.ko_handler()
                    self.get_next_turn()
                #
                #   DEFEND
                #
                if command_panel.get_single_selection() == "DEFEND":
                    self.current_actor.defend = True
                    self.get_next_turn()
                #
                #   ITEM
                #
                if command_panel.get_single_selection() == "ITEM":
                    self.item_dict = self.persist["PARTY"].inventory["Consumable"]
                    self.command_flag = "ITEM"
                    self.using_item = ""
                    self.consumables = {}
                    self.consumables_names = []
                    for name, ref_quan in self.item_dict.items():
                        self.consumables[name] = ref_quan[0]
                        self.consumables_names.append(f"{name}: {ref_quan[1]}")
                    self.consumables_names.sort(key=lambda x: self.item_dict[x.split(":")[0]][0].sortID)
                    command_panel.set_item_list(self.consumables_names + ["BACK"])
                if self.command_flag == "ITEM" and command_panel.get_single_selection() in self.consumables_names:
                    self.using_item = command_panel.get_single_selection().split(":")[0]
                    command_panel.set_item_list(self.enemy_name_list + self.ally_name_list + ["BACK"])
                elif self.using_item and command_panel.get_single_selection() != "BACK":
                    if command_panel.get_single_selection() in self.enemy_name_list:
                        mechanics.itemFilter(
                            self.consumables[self.using_item].effect,
                            self.current_actor,
                            self.enemies,
                            self.enemy_name_list.index(command_panel.get_single_selection())
                        )
                    if command_panel.get_single_selection() in self.ally_name_list:
                        mechanics.itemFilter(
                            self.consumables[self.using_item].effect,
                            self.current_actor,
                            self.allies,
                            self.ally_name_list.index(command_panel.get_single_selection())
                        )
                    self.item_dict[self.using_item][1] -= 1
                    if self.item_dict[self.using_item][1] == 0:
                        del self.item_dict[self.using_item]
                    self.ko_handler()
                    self.get_next_turn()
                #
                #   RUN
                #
                if command_panel.get_single_selection() == "RUN":
                    self.try_flee()
                #
                #   BACK
                #
                if command_panel.get_single_selection() == "BACK":
                    self.command_flag = ""
                    self.using_item = ""
                    command_panel.set_item_list(command_list)

        manager.process_events(event)


    def draw(self, surface):
        """Blit all elements to surface."""
        surface.fill(pg.Color(40, 40, 40))
        portrait = gui.ui_image.UIImage(relative_rect=pg.Rect((5, 2), (200, 190)),
                                        image_surface=self.current_actor.portrait,
                                        manager=manager,
                                        container=menu)
        for ally in self.allies:
            if ally.ko:
                surface.blit(ally.battle_sprite, ally.renderLoc, special_flags=pg.BLEND_RGBA_SUB)
            else:
                surface.blit(ally.battle_sprite, ally.renderLoc)
        for enemy in self.enemies:
            surface.blit(enemy.battle_sprite[enemy.current_frame], enemy.renderLoc)
        manager.draw_ui(surface)


    def update(self, surface, keys, current_time, dt):
        """Update function for state.  Must be overloaded in children."""
        hp_tracking = ""
        for chara in self.allies:
            hp_tracking += (f"{chara.name} {'&nbsp;'*(10 - len(chara.name))}{chara.hp}/{chara.stats['MAXHP']} HP {'&nbsp;'*(10 - len(str(chara.hp) + str(chara.stats['MAXHP'])))}{chara.mp}/{chara.stats['MAXMP']} MP<br>")
        # hp_panel.set_item_list(hp_tracking)
        hp_panel = textbox(html_text=hp_tracking, relative_rect=pg.Rect((206, 0), (294, 194)), manager=manager, container=menu)
        for enemy in self.enemies:
            if current_time - enemy.last_update > 150:
                enemy.last_update = current_time
                enemy.current_frame = (enemy.current_frame + 1) % 4
        manager.update(dt)
        self.draw(surface)
