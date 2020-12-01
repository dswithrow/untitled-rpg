import pygame as pg, pygame_gui
from .. import prepare, tools, sprites
from .constants import items, units, mechanics

gui = pygame_gui.elements
select = pygame_gui.elements.ui_selection_list.UISelectionList
textbox = pygame_gui.elements.ui_text_box.UITextBox

base_list = ["STATUS", "EQUIP", "ITEMS", "EXIT"]
party_list = ["ANNA", "ELISE", "XAVIER", "BEAU"]


manager = pygame_gui.UIManager((800, 600))
menu = gui.ui_panel.UIPanel(   relative_rect=pg.Rect((0, 0), (800, 600)),
                starting_layer_height=1, manager=manager)
main_menu = select(relative_rect=pg.Rect((3, 3), (194, 594)), item_list=base_list, manager=manager, container=menu)
text1 = textbox(html_text="", relative_rect=pg.Rect((200, 3), (150, 194)), manager=manager, container=menu)
text2 = textbox(html_text="", relative_rect=pg.Rect((350, 3), (150, 194)), manager=manager, container=menu)
text3 = textbox(html_text="", relative_rect=pg.Rect((500, 3), (150, 194)), manager=manager, container=menu)
text4 = textbox(html_text="", relative_rect=pg.Rect((650, 3), (150, 194)), manager=manager, container=menu)
desc = textbox(html_text="", relative_rect=pg.Rect((200, 200), (600, 100)), manager=manager, container=menu)
sub_menu = select(relative_rect=pg.Rect((200, 300), (600, 294)), item_list=[], manager=manager, container=menu)


class Menu(tools._State):
    """This is a prototype class for States.  All states should inherit from it.
    No direct instances of this class should be created. get_event and update
    must be overloaded in the childclass.  startup and cleanup need to be
    overloaded when there is data that must persist between States."""
    def __init__(self):
        self.start_time = 0.0
        self.current_time = 0.0
        self.done = False
        self.quit = False
        self.next = None
        self.previous = None
        self.persist = {}
        self.command_flag = ""
        self.unit = ""
        self.inv_list = []
        self.weap_list = []
        self.gear_list = []

    def get_event(self, event):
        """Processes events that were passed from the main event loop.
        Must be overloaded in children."""
        if event.type == pg.KEYDOWN:
            pass

        if event.type == pg.USEREVENT:
            if event.user_type == pygame_gui.UI_SELECTION_LIST_NEW_SELECTION:
                print(f"{self.command_flag} {main_menu.get_single_selection()} {sub_menu.get_single_selection()}")
                if main_menu.get_single_selection() == "EQUIP":
                    self.command_flag = "EQUIP"
                    main_menu.set_item_list(party_list + ["BACK"])
                if self.command_flag == "EQUIP" and main_menu.get_single_selection() in party_list and not sub_menu.get_single_selection():
                    self.unit = party_list.index(main_menu.get_single_selection())
                    self.unit = self.persist["PARTY"].units[self.unit]
                    self.inv_list = []
                    self.gear_list = []
                    for name, ref_q in self.persist["PARTY"].inventory["Weapon"].items():
                        weapon = ref_q[0]
                        if weapon.equip in self.unit.job["equipment"]:
                            self.inv_list.append(weapon.name)
                            self.gear_list.append(weapon.name)
                            self.gear_list.append(weapon)
                    for name, ref_q in self.persist["PARTY"].inventory["Gear"].items():
                        gear = ref_q[0]
                        if gear.equip in self.unit.job["equipment"]:
                            self.inv_list.append(gear.name)
                            self.gear_list.append(gear.name)
                            self.gear_list.append(gear)
                    sub_menu.set_item_list(self.inv_list + ["BACK"])
                    print(self.gear_list)
                if self.command_flag == "EQUIP" and sub_menu.get_single_selection() in self.gear_list:
                    item = self.gear_list[self.gear_list.index(sub_menu.get_single_selection()) + 1]
                    print(self.gear_list.index(sub_menu.get_single_selection()))
                    if item.type == "Weapon":
                        temp = self.unit.equip["main"]
                        self.unit.equip["main"] = item
                        if temp.name in self.persist["PARTY"].inventory["Weapon"].keys():
                            self.persist["PARTY"].inventory["Weapon"][temp.name][1] += 1
                        else:
                            self.persist["PARTY"].inventory["Weapon"][temp.name] = [temp, 1]
                        self.persist["PARTY"].inventory["Weapon"][item.name][1] -= 1
                        if self.persist["PARTY"].inventory["Weapon"][item.name][1] == 0:
                            del self.persist["PARTY"].inventory["Weapon"][item.name]
                            
                    if item.type == "Gear":
                        pass
                    main_menu.set_item_list(base_list)
                    sub_menu.set_item_list([])
                    self.command_flag = ""
                    self.unit = ""
                if main_menu.get_single_selection() == "BACK" or sub_menu.get_single_selection() == "BACK":
                    main_menu.set_item_list(base_list)
                    sub_menu.set_item_list([])
                    self.command_flag = ""
                    self.unit = ""
                if main_menu.get_single_selection() == "EXIT":
                    self.done = True
        manager.process_events(event)

    def startup(self, current_time, persistant):
        """Add variables passed in persistant to the proper attributes and
        set the start time of the State to the current time."""
        self.persist = persistant
        self.start_time = current_time
        self.next = "OVERWORLD"
        self.command_flag = ""

    def draw(self, surface):
        """Blit all elements to surface."""
        manager.draw_ui(surface)

    def update(self, surface, keys, current_time, dt):
        """Update function for state.  Must be overloaded in children."""
        text1 = textbox(html_text=
                f"{self.persist['PARTY'].units[0].name} <br>HP: {self.persist['PARTY'].units[0].hp}/{self.persist['PARTY'].units[0].stats['MAXHP']} <br>MP: {self.persist['PARTY'].units[0].mp}/{self.persist['PARTY'].units[0].stats['MAXMP']}",
                relative_rect=pg.Rect((200, 3), (150, 194)), manager=manager, container=menu)
        text2 = textbox(html_text=
                f"{self.persist['PARTY'].units[1].name} <br>HP: {self.persist['PARTY'].units[1].hp}/{self.persist['PARTY'].units[1].stats['MAXHP']} <br>MP: {self.persist['PARTY'].units[1].mp}/{self.persist['PARTY'].units[1].stats['MAXMP']}",
                relative_rect=pg.Rect((350, 3), (150, 194)), manager=manager, container=menu)
        text3 = textbox(html_text=
                f"{self.persist['PARTY'].units[2].name} <br>HP: {self.persist['PARTY'].units[2].hp}/{self.persist['PARTY'].units[2].stats['MAXHP']} <br>MP: {self.persist['PARTY'].units[2].mp}/{self.persist['PARTY'].units[2].stats['MAXMP']}",
                relative_rect=pg.Rect((500, 3), (150, 194)), manager=manager, container=menu)
        text4 = textbox(html_text=
                f"{self.persist['PARTY'].units[3].name} <br>HP: {self.persist['PARTY'].units[3].hp}/{self.persist['PARTY'].units[3].stats['MAXHP']} <br>MP: {self.persist['PARTY'].units[3].mp}/{self.persist['PARTY'].units[3].stats['MAXMP']}",
                relative_rect=pg.Rect((650, 3), (150, 194)), manager=manager, container=menu)
        manager.update(dt)
        self.draw(surface)