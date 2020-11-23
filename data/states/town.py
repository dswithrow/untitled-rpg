import pygame as pg
from os import path
import random
from .. import prepare, tools, sprites
from .lib import map_info, units


class Town(tools._State):
    """
    This is the state for travelling on the overworld, and can lead to encounters and 
    """
    def __init__(self):
        tools._State.__init__(self)
        self.startup(self.start_time, self.persist)
        self.player_sprite = prepare.SPRITES["swordsman_world"]
        self.all_sprites = pg.sprite.Group()
        self.walls = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.name == 'block':
                sprites.Obstacle(self,  tile_object.x,
                                tile_object.y,
                                tile_object.width,
                                tile_object.height)
        self.ports = pg.sprite.Group()
        for tile_object in self.map.tmxdata.objects:
            if tile_object.type == 'Port':
                sprites.Port(self, tile_object.name,
                                tile_object.x,
                                tile_object.y,
                                tile_object.width,
                                tile_object.height)
        self.landings = pg.sprite.Group()
        self.player = sprites.Player(self, 15, 15)
        for tile_object in self.map.tmxdata.objects:
            if tile_object.type == 'Landing':
                sprites.Landing(self, tile_object.name,
                                tile_object.x,
                                tile_object.y,
                                tile_object.width,
                                tile_object.height)
                if "PORT" in self.persist.keys() and tile_object.name == self.persist["PORT"]:
                    self.player.pos = (tile_object.x, tile_object.y)
                    self.player.port = ""
                    del self.persist["PORT"]
        self.player.last_battle = 0
        self.camera = tools.Camera(self.map.width, self.map.height)
        self.dt = 0
        self.next = "OVERWORLD"

    def startup(self, current_time, persistant):
        self.persist = persistant
        self.start_time = current_time
        self.map = tools.TiledMap(prepare.MAPS["town"])
        self.map_image = self.map.make_map()
        self.map_rect = self.map_image.get_rect()
        self.info = map_info.map_info["town"]
        if "PARTY" not in self.persist.keys():
            self.persist["PARTY"] = units.start_party
        for tile_object in self.map.tmxdata.objects:
            if tile_object.type == 'Landing':
                if "PORT" in self.persist.keys() and tile_object.name == self.persist["PORT"]:
                    self.player.pos = (tile_object.x, tile_object.y)
                    self.player.port = ""
                    del self.persist["PORT"]

    def check_encounter(self, debug=False):
        if random.randint(1, 100) < (self.info["ENC_RATE"] * self.player.last_battle) or debug:
            self.player.last_battle = 0
            self.done = True
            self.persist["MAP"] = "town"

    def get_event(self, event):
        if event.type == pg.KEYDOWN:
            # if event.key == pg.K_SPACE:
            #     self.check_encounter(True)
            if event.key == pg.K_h:
                for ally in self.persist["PARTY"].units:
                    ally.hp = ally.stats["MAXHP"]
                    ally.mp = ally.stats["MAXMP"]
                    ally.ko = False

    def draw(self, surface):
        surface.blit(self.map_image, self.camera.apply_rect(self.map_rect))
        for sprite in self.all_sprites:
            surface.blit(sprite.image, self.camera.apply(sprite) )

    def update(self, surface, keys, current_time, dt):
        self.dt = dt
        self.all_sprites.update()
        self.camera.update(self.player)
        if "Town" in self.player.port:
            self.next = "OVERWORLD"
            self.persist["PORT"] = self.player.port
            self.player.port = ""
            self.done = True
        # if self.player.walking:
        #     self.check_encounter()
        self.draw(surface)
