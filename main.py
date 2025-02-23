import pygame

from scenes import MainMenuScene, GameOverScene, GameScene
from contants import WIDTH, HEIGHT, MAINMENU_SCENE, GAME_SCENE, GAMEOVER_SCENE

def main():
    running = True
    dt = 0
    pygame.init()
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    clock = pygame.time.Clock()
    currentScene = MainMenuScene(clock, WIDTH, HEIGHT)
    while running:

        # check for exit and scene switches
        for event in pygame.event.get():
            if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
                running = False
            elif event.type == MAINMENU_SCENE:
                currentScene.cleanup()
                currentScene = MainMenuScene(clock, WIDTH, HEIGHT)
            elif event.type == GAME_SCENE:
                currentScene.cleanup()
                currentScene = GameScene(clock, WIDTH, HEIGHT)
            elif event.type == GAMEOVER_SCENE:
                currentScene.cleanup()
                currentScene = GameOverScene(clock, WIDTH, HEIGHT)
            else:
                currentScene.on_event(event)

        # update and render current scene
        currentScene.update(dt)
        currentScene.draw(screen)

        pygame.display.flip()
        dt = clock.tick(60) / 1000

    pygame.quit()


if __name__ == '__main__':
    main()
