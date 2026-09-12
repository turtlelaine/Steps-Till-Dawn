import pygame
import sys
import os
from game import Game

pygame.init()
pygame.mixer.init()

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Steps Till Dawn")
clock = pygame.time.Clock()

menu_bg = pygame.image.load("assets/backgrounds/Mainpagebg.png").convert()
menu_bg = pygame.transform.scale(menu_bg, (SCREEN_WIDTH, SCREEN_HEIGHT))
title_img = pygame.image.load("assets/backgrounds/Title.png").convert_alpha()

# bgm
pygame.mixer.music.load("assets/bgm/main.mp3")
pygame.mixer.music.set_volume(0.5)
pygame.mixer.music.play(-1)

# main page buttons
newgame_img = pygame.image.load("assets/backgrounds/Newgame.png").convert_alpha()
loadgame_img = pygame.image.load("assets/backgrounds/Loadgame.png").convert_alpha()
exit_img = pygame.image.load("assets/backgrounds/Exit.png").convert_alpha()

# button coverage
newgame_cov = pygame.image.load("assets/objects/mainpage/Newgame_coverage.png").convert_alpha()
loadgame_cov = pygame.image.load("assets/objects/mainpage/Loadgame_coverage.png").convert_alpha()
exit_cov = pygame.image.load("assets/objects/mainpage/Exit_coverage.png").convert_alpha()

title_img = pygame.transform.scale(title_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
newgame_img = pygame.transform.scale(newgame_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
loadgame_img = pygame.transform.scale(loadgame_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
exit_img = pygame.transform.scale(exit_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
newgame_cov = pygame.transform.scale(newgame_cov, (SCREEN_WIDTH, SCREEN_HEIGHT))
loadgame_cov = pygame.transform.scale(loadgame_cov, (SCREEN_WIDTH, SCREEN_HEIGHT))
exit_cov = pygame.transform.scale(exit_cov, (SCREEN_WIDTH, SCREEN_HEIGHT))

NEWGAME_RECT = newgame_cov.get_bounding_rect()
LOADGAME_RECT = loadgame_cov.get_bounding_rect()
EXIT_RECT = exit_cov.get_bounding_rect()

STATE_MENU = "menu"
STATE_GAME = "game"
current_state = STATE_MENU
game = None

SAVE_FILE = "save.json"

def has_save():
    return os.path.exists(SAVE_FILE)

# Main loop
running = True
while running:
    # only main page reads mouse
    if current_state == STATE_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if NEWGAME_RECT.collidepoint(mouse_pos):
                    print("new game")
                    game = Game(screen)
                    current_state = STATE_GAME

                elif LOADGAME_RECT.collidepoint(mouse_pos):
                    if has_save():
                        print("you read the diary and choose to come back.")
                        game = Game(screen)
                        game.load()
                        current_state = STATE_GAME
                    else:
                        print("You did not write anything in the diary yet.")

                elif EXIT_RECT.collidepoint(mouse_pos):
                    print("Good morning, player, and goodbye.")
                    running = False

    # independent state
    elif current_state == STATE_GAME:
        if game:
            game.update()
            game.draw()
            if game.should_exit():
                game.save()
                current_state = STATE_MENU
                game = None

    if current_state == STATE_MENU:
        screen.blit(menu_bg, (0, 0))
        screen.blit(title_img, (0, 0))
        screen.blit(newgame_img, (0, 0))
        screen.blit(loadgame_img, (0, 0))
        screen.blit(exit_img, (0, 0))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()