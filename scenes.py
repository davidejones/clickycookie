import math
import time
from random import randrange

import pygame

from contants import MAINMENU_SCENE, GAME_SCENE, GAMEOVER_SCENE, TIMER_EVENT
from sprites import Bomb, ChocCookie, SugarCookie, Paw, Cookie
from utils import load_sound, load_image, draw_text


class Scene:
    def __init__(self, clock, width, height):
        self.clock = clock
        self.width = width
        self.height = height
        self.font = pygame.font.SysFont(None, 30)

    def on_event(self, event):
        pass

    def update(self, dt):
        pass

    def draw(self, surface):
        pass

    def cleanup(self):
        pass

class GameOverScene(Scene):

    def __init__(self, clock, width, height, score):
        super().__init__(clock, width, height)
        self.score = score
        self.click = False
        self.rotation = 0
        self.rotation_direction = 1
        self.rotation_speed = 3
        self.play_again_btn = pygame.Rect(200, 250, 200, 50)
        self.end_snd = load_sound("assets/meowmeow.wav")
        self.end_snd.play()
        self.bg, self.bg_rect = load_image("assets/Over.png", None, 1)
        #self.cathead, self.cat_rect = load_image("assets/cathead.png", (255, 255, 255), 0.8)
        self.cathead, self.cat_rect = load_image("assets/Cathead-transparent.png", None, 0.8)
        self.pos = pygame.mouse.get_pos()

    def cleanup(self):
        super().cleanup()
        self.click = False
        self.rotation = 0
        self.end_snd.stop()

    def on_event(self, event):
        super().on_event(event)
        self.click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            self.pos = pygame.mouse.get_pos()
            if event.button == 1:
                self.click = True

    def update(self, dt):
        self.rotation += self.rotation_speed * self.rotation_direction
        if self.rotation > 45:
            self.rotation_direction = -1
        elif self.rotation < -45:
            self.rotation_direction = 1
        if self.play_again_btn.collidepoint(self.pos) and self.click:
            pygame.event.post(pygame.event.Event(MAINMENU_SCENE))


    def draw(self, screen):
        super().draw(screen)
        screen.fill((128, 128, 128))
        screen.blit(self.bg, (0, 0))
        rotated_cathead = pygame.transform.rotate(self.cathead, self.rotation)
        rotated_cathead_rect = rotated_cathead.get_rect()
        screen.blit(rotated_cathead,
                    (self.width * 0.5 - rotated_cathead_rect.width * 0.5,
                     (self.height * 0.5 - rotated_cathead_rect.height * 0.5) + 150))
        # screen.blit(rotated_cathead, (WIDTH * 0.5 - cat_rect.width * 0.5, HEIGHT * 0.5 - cat_rect.height * 0.5))
        #draw_text('GAME OVER', self.font, (0, 0, 0), screen, self.width * 0.5 - 55, 20)
        pygame.draw.rect(screen, (255, 150, 150), self.play_again_btn)
        draw_text('MAIN MENU', self.font, (0, 0, 0), screen, self.play_again_btn.x + 40, self.play_again_btn.y + 15)
        draw_text(f'Score: {self.score}', self.font, (0, 0, 0), screen, self.play_again_btn.x + 40, self.play_again_btn.y + 80)


class MainMenuScene(Scene):

    def __init__(self, clock, width, height):
        super().__init__(clock, width, height)
        self.click = False
        #self.bg, self.bg_rect = load_image("assets/title3.jpg", None, 1)
        self.bg, self.bg_rect = load_image("assets/Menu.png", None, 1)

    def cleanup(self):
        super().cleanup()
        self.click = False

    def on_event(self, event):
        super().on_event(event)
        self.click = False
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1:
                self.click = True

    def draw(self, screen):
        super().draw(screen)
        screen.fill((0, 0, 0))

        # gradient bg
        # colour_rect = pygame.Surface((2, 2))
        # pygame.draw.line(colour_rect, (255, 233, 233), (0, 0), (0, 1))
        # pygame.draw.line(colour_rect, (255, 180, 180), (1, 0), (1, 1))
        # colour_rect = pygame.transform.smoothscale(colour_rect, (self.width, self.height))
        # screen.blit(colour_rect, pygame.Rect(0, 0, self.width, self.height))

        screen.blit(self.bg, (0, 0))

        mx, my = pygame.mouse.get_pos()

        btn_width = 200
        btn_height = 50
        button_1 = pygame.Rect(100, 250, btn_width, btn_height)
        button_2 = pygame.Rect(310, 250, btn_width, btn_height)
        if button_1.collidepoint((mx, my)):
            if self.click:
                pygame.event.post(pygame.event.Event(GAME_SCENE))
        if button_2.collidepoint((mx, my)):
            if self.click:
                pygame.event.post(pygame.event.Event(pygame.QUIT))

        pygame.draw.rect(screen, (255, 150, 150), button_1)
        pygame.draw.rect(screen, (255, 150, 150), button_2)
        draw_text('PLAY GAME', self.font, (255, 255, 255), screen, button_1.x + 40, button_1.y + 15)
        draw_text('QUIT', self.font, (255, 255, 255), screen, button_2.x + 75, button_2.y + 15)
        pygame.display.update()


class GameScene(Scene):

    def __init__(self, clock, width, height):
        super().__init__(clock, width, height)
        self.num_cookies = 7
        self.score = 0
        self.timer_sec = 10
        self.pos = pygame.mouse.get_pos()

        # setup our sounds
        self.cat_snd1 = load_sound("assets/Bubs1.wav")
        self.cat_snd2 = load_sound("assets/Bubs2.wav")
        self.cat_snd3 = load_sound("assets/Bubs3.wav")
        self.cat_sounds = [self.cat_snd1, self.cat_snd2, self.cat_snd3]

        # background sound
        self.bg_snd = load_sound("assets/background.wav")
        self.bg_snd.set_volume(0.2)
        self.bg_snd.play(loops=-1)

        # setup our sprites
        self.all_sprites = pygame.sprite.LayeredDirty()
        for i in range(self.num_cookies):
            if i == 0:
                bomb = Bomb()
                bomb.set_random_location(0, 600, 0, 800)
                self.all_sprites.add(bomb)
            else:
                cookie_choice = randrange(0, 2)
                if cookie_choice == 1:
                    cookie = ChocCookie()
                else:
                    cookie = SugarCookie()
                cookie.set_random_location(0, 600, 0, 800)
                self.all_sprites.add(cookie)

        self.paw = Paw()
        self.all_sprites.add(self.paw)
        self.bg, self.bg_rect = load_image("assets/background.png", None, 1)

        pygame.time.set_timer(TIMER_EVENT, 1000)

    def cleanup(self):
        super().cleanup()
        self.num_cookies = 7
        self.score = 0
        self.timer_sec = 5
        self.cat_snd1.stop()
        self.cat_snd2.stop()
        self.cat_snd3.stop()
        self.bg_snd.stop()

    def on_event(self, event):
        super().on_event(event)
        if event.type == TIMER_EVENT:
            if self.timer_sec > 0:
                self.timer_sec -= 1
            else:
                pygame.event.post(pygame.event.Event(GAMEOVER_SCENE, {"score": self.score}))
        if event.type == pygame.MOUSEBUTTONUP:
            self.pos = pygame.mouse.get_pos()
            # get a list of all cookie sprites that are under the mouse cursor
            clicked_sprites = [s for s in self.all_sprites if s.rect.collidepoint(self.pos) and isinstance(s, Cookie)]
            # If we clicked a cookie then lets grab it!
            if clicked_sprites:
                self.cat_sounds[randrange(0, len(self.cat_sounds))].play()
                # just use the first match for now to avoid overlaps causing 2 to run
                for c in clicked_sprites[:1]:
                    if isinstance(c, ChocCookie):
                        self.score += 10
                    elif isinstance(c, SugarCookie):
                        self.score += 5
                    self.paw.grab(c, self.pos)

    def update(self, dt):
        # event updates for sprites
        self.all_sprites.update(dt=dt)

    def draw(self, screen):
        super().draw(screen)
        # fill the screen with a color to wipe away anything from last frame
        screen.fill((200, 200, 200))
        screen.blit(self.bg, (0, 0))

        # render sprites
        self.all_sprites.draw(screen)

        # Draw the score to the screen
        pygame.draw.rect(screen, (255, 150, 150), pygame.Rect(0, 0, 120, 40))
        score_text = self.font.render(f'Score: {self.score}', True, (0, 0, 0))
        screen.blit(score_text, (10, 10))

        # Draw the timer to the screen
        pygame.draw.rect(screen, (255, 150, 150), pygame.Rect(screen.width - 80, 0, 80, 40))
        timer_text = self.font.render(time.strftime('%M:%S', time.gmtime(self.timer_sec)), True, (0, 0, 0))
        screen.blit(timer_text, (screen.width - 60, 10))