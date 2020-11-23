"""
This module initializes the display and creates dictionaries of resources.
"""

import os
import pygame as pg

from . import tools

# Constants
SCREEN_SIZE = (800, 600)
ORIGINAL_CAPTION = "Untitled RPG"
PLAYERSPEED = 150
TILESIZE = 50


# Initialization
pg.init()
pg.key.set_repeat(500, 100)
os.environ['SDL_VIDEO_CENTERED'] = "TRUE"
pg.display.set_caption(ORIGINAL_CAPTION)
SCREEN = pg.display.set_mode(SCREEN_SIZE)
SCREEN_RECT = SCREEN.get_rect()


# Resource loading (Fonts and music just contain path names).
FONTS = tools.load_all_fonts(os.path.join("resources", "fonts"))
MUSIC = tools.load_all_music(os.path.join("resources", "music"))
SFX   = tools.load_all_sfx(os.path.join("resources", "sound"))
GFX   = tools.load_all_gfx(os.path.join("resources", "graphics"))
MOV   = tools.load_all_movies(os.path.join("resources", "movies"))
MAPS  = tools.load_all_maps(os.path.join("resources", "maps"))
SPRITES  = tools.load_all_gfx(os.path.join("resources", "sprites"))
MONSTERS = tools.load_all_gfx(os.path.join("resources", "battle_sprites"))
for key, sprite in MONSTERS.items():
    temp_sprite = []
    w = sprite.get_width()//4
    h = sprite.get_height()
    for i in range(0,4):
        temp_sprite.append(sprite.subsurface((w*(i),0,w,h)))
    MONSTERS[key] = temp_sprite
ALLIES = tools.load_all_gfx(os.path.join("resources", "battle_sprites/allies"))
MOVES = tools.load_all_gfx(os.path.join("resources", "battle_sprites/moves"))
for key, sprite in MOVES.items():
    temp_sprite = []
    for i in range(0,4):
        temp_sprite.append(sprite.subsurface((200*(i),0,200,200)))
    MOVES[key] = temp_sprite