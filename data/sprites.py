import pygame as pg
from os import path
from . import prepare, tools
vec = pg.math.Vector2

class Player(pg.sprite.Sprite):
    def __init__(self, game, x, y):
        self.groups = game.all_sprites
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.image = game.player_sprite.subsurface((0,0,50,50))
        self.rect = self.image.get_rect()
        self.vel = vec(0, 0)
        self.pos = vec(x, y) * prepare.TILESIZE
        self.walking = False
        self.dash = 1
        self.direction = "DOWN"
        self.current_frame = 0
        self.last_update = pg.time.get_ticks()
        self.animation_dict = self.load_sprite(game.player_sprite)
        self.last_battle = 0
        self.port = ""

    def load_sprite(self, spritesheet):
        down, up, left, right = [],[],[],[]
        for i in range(0,4):
            down.append(spritesheet.subsurface((50*(i),0,50,50)))
            up.append(spritesheet.subsurface((50*(i),50,50,50)))
            left.append(spritesheet.subsurface((50*(i),100,50,50)))
            right.append(spritesheet.subsurface((50*(i),150,50,50)))
        walking_dict= {
            "UP": up,
            "DOWN": down,
            "LEFT": left,
            "RIGHT": right
        }
        return walking_dict

    def animate(self):
        self.walking = self.vel.x != 0 or self.vel.y != 0
        if self.walking:
            now = pg.time.get_ticks()
            if abs(self.vel.y) > abs(self.vel.x):
                self.direction = "UP" if self.vel.y < 0 else "DOWN"
            if abs(self.vel.y) < abs(self.vel.x):
                self.direction = "LEFT" if self.vel.x < 0 else "RIGHT"
            if now - self.last_update > (200 / self.dash):
                self.last_update = now
                self.current_frame = (self.current_frame + 1) % 4
                self.image = self.animation_dict[self.direction][self.current_frame]
                self.last_battle += 1
        else:
            self.current_frame = 0
            self.image = self.animation_dict[self.direction][0]

    def wall_collision(self, direction):
        if direction == "X":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.x > 0: # Check if collided going right
                    self.pos.x = hits[0].rect.left - self.rect.width
                if self.vel.x < 0: # check if collided going left
                    self.pos.x = hits[0].rect.right
                self.vel.x = 0
                self.rect.x = self.pos.x
        if direction == "Y":
            hits = pg.sprite.spritecollide(self, self.game.walls, False)
            if hits:
                if self.vel.y > 0: # Check if collided going down
                    self.pos.y = hits[0].rect.top - self.rect.height
                if self.vel.y < 0: # check if collided going up
                    self.pos.y = hits[0].rect.bottom
                self.vel.y = 0
                self.rect.y = self.pos.y
        port = pg.sprite.spritecollide(self, self.game.ports, False)
        if port:
            self.port = port[0].name
        

    def get_keys(self):
        self.vel = vec(0, 0)
        keys = pg.key.get_pressed()
        self.dash = 1
        if keys[pg.K_LSHIFT] or keys[pg.K_RSHIFT]:
            self.dash = 1.7
        if keys[pg.K_LEFT] or keys[pg.K_a]:
            self.vel.x = -prepare.PLAYERSPEED * self.dash
        if keys[pg.K_RIGHT] or keys[pg.K_d]:
            self.vel.x = prepare.PLAYERSPEED * self.dash
        if keys[pg.K_UP] or keys[pg.K_w]:
            self.vel.y = -prepare.PLAYERSPEED * self.dash
        if keys[pg.K_DOWN] or keys[pg.K_s]:
            self.vel.y = prepare.PLAYERSPEED * self.dash
        if self.vel.x != 0 and self.vel.y !=0:
            self.vel *= .7

    def update(self):
        self.get_keys() 
        self.pos += self.vel * self.game.dt
        self.rect.x = self.pos.x
        self.wall_collision("X")
        self.rect.y = self.pos.y
        self.wall_collision("Y")
        self.animate()

class Obstacle(pg.sprite.Sprite):
    def __init__(self, game, x, y, w, h):
        self.groups = game.walls
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Port(pg.sprite.Sprite):
    def __init__(self, game, name, x, y, w, h):
        self.groups = game.ports
        self.name = name
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y

class Landing(pg.sprite.Sprite):
    def __init__(self, game, name, x, y, w, h):
        self.groups = game.landings
        self.name = name
        pg.sprite.Sprite.__init__(self, self.groups)
        self.game = game
        self.rect = pg.Rect(x, y, w, h)
        self.x = x
        self.y = y
        self.rect.x = x
        self.rect.y = y