import random

import pygame

from utils import load_image


class Cookie(pygame.sprite.DirtySprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.rect = None
        self.name = ""

    def hide(self):
        self.visible = 0

    def show(self):
        self.visible = 1

    def update(self, *args, **kwargs):
        self.dirty = 1

    def set_random_location(self, minx, maxx, miny, maxy):
        if self.rect is not None:
            self.rect.topleft = (
                random.randrange(minx, maxx - self.rect.width),
                random.randrange(miny, maxy - self.rect.height),
            )
            # TODO: if cookie overlap place somewhere else


class SugarCookie(Cookie):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image, self.rect = load_image("assets/sugarcookie.png", None, 0.3)


class ChocCookie(Cookie):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image, self.rect = load_image("assets/cookie.png", None, 0.25)


class Paw(pygame.sprite.DirtySprite):
    def __init__(self, *groups):
        super().__init__(*groups)
        #self.image, self.rect = load_image("assets/paw_old.png", None, 0.6)
        self.image, self.rect = load_image("assets/paw.png", None, 0.35)
        self.rect.top = 800
        self.rect.left = 0
        self.grabbing = False
        self.returning = False
        self.targety = 0
        self.target_cookie = None
        self.particles = []
        self.cat_speed = 2000

    def grab(self, cookie, pos):
        self.returning = False
        self.grabbing = True
        self.rect.left = pos[0] - self.rect.width / 2
        self.targety = cookie.rect.y + self.rect.height
        self.target_cookie = cookie
        #cookie.hide()

    def update(self, *args, **kwargs):
        dt = kwargs.get("dt")
        if self.returning:
            #screen = kwargs.get("screen")
            self.particles.append([[self.rect.centerx, self.rect.y], [random.randint(0, 20) / 10 - 1, -2], random.randint(4, 30)])
            for particle in self.particles:
                particle[0][0] += particle[1][0]
                particle[0][1] += particle[1][1]
                particle[2] -= 0.5
                particle[1][1] += 0.5
                #pygame.draw.circle(screen, (239, 239, 239), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))
                if particle[2] <= 0:
                    self.particles.remove(particle)
        else:
            for particle in self.particles:
                self.particles.remove(particle)

        if self.grabbing:
            self.rect.top -= self.cat_speed * dt
            if self.rect.top <= self.targety - self.rect.height:
                self.grabbing = False
                self.returning = True
        elif self.returning:
            self.rect.top += self.cat_speed * dt
            self.target_cookie.rect.top += self.cat_speed * dt
            if self.rect.top > 800:
                self.returning = False
                self.grabbing = False
                self.target_cookie = None
                # destroy cookie?
        self.dirty = 1

    def draw(self, screen):
        for particle in self.particles:
            pygame.draw.circle(screen, (239, 239, 239), [int(particle[0][0]), int(particle[0][1])], int(particle[2]))


class Bomb(Cookie):
    def __init__(self, *groups):
        super().__init__(*groups)
        self.image, self.rect = load_image("assets/dabomb.png", None, 0.3)

    # def update(self, *args, **kwargs):
    #     pass