import pygame
import os

import pathlib


def load_image(name, colorkey=None, scale=1):
    fullname = pathlib.Path(__file__).resolve().parent / name
    image = pygame.image.load(fullname)
    image = image.convert_alpha()

    image = pygame.transform.scale_by(image, scale)

    if colorkey is not None:
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey, pygame.RLEACCEL)
    return image, image.get_rect()


def load_sound(name):
    class NoneSound:
        def play(self):
            pass

    if not pygame.mixer or not pygame.mixer.get_init():
        return NoneSound()

    fullname = pathlib.Path(__file__).resolve().parent / name
    sound = pygame.mixer.Sound(fullname)

    return sound


def draw_text(text, font, color, surface, x, y):
    textobj = font.render(text, 1, color)
    textrect = textobj.get_rect()
    textrect.topleft = (x, y)
    surface.blit(textobj, textrect)