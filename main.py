import pygame
import sys
import os
from game import Game
from scene import Scene

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
STATE_LOAD = "load"
STATE_GAME = "game"
current_state = STATE_MENU
game = None

SAVE_FILE = ".venv/save.json"

def has_save():
    return os.path.exists(SAVE_FILE)

def get_save_slots():
    import json
    import os
    slots = []
    for i in range(1, 4):
        filename = f"save_slot_{i}.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)
            slots.append({
                "slot": i,
                "time": data.get("time", "Unknown"),
                "scene": data.get("scene", "Unknown"),
            })
        else:
            slots.append({
                "slot": i,
                "time": "Empty",
                "scene": "",
            })
    return slots

# Main loop
running = True
while running:
    if current_state == STATE_MENU:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()

                if NEWGAME_RECT.collidepoint(mouse_pos):
                    game = Game(screen)
                    current_state = STATE_GAME

                elif LOADGAME_RECT.collidepoint(mouse_pos):
                    current_state = STATE_LOAD

                elif EXIT_RECT.collidepoint(mouse_pos):
                    running = False

        screen.blit(menu_bg, (0, 0))
        screen.blit(title_img, (0, 0))
        screen.blit(newgame_img, (0, 0))
        screen.blit(loadgame_img, (0, 0))
        screen.blit(exit_img, (0, 0))

    elif current_state == STATE_LOAD:
        screen.fill((0, 0, 0))

        font = pygame.font.Font(None, 36)
        title = font.render("Select Save Slot", True, (255, 255, 255))
        title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, 50))
        screen.blit(title, title_rect)

        slots = get_save_slots()
        slot_rects = []
        for i, slot in enumerate(slots):
            y = 150 + i * 80
            rect = pygame.Rect(100, y, 600, 60)
            pygame.draw.rect(screen, (50, 50, 50), rect)
            pygame.draw.rect(screen, (255, 255, 255), rect, 2)

            slot_font = pygame.font.Font(None, 28)
            if slot["time"] == "Empty":
                text = slot_font.render(f"Slot {slot['slot']}: Empty", True, (100, 100, 100))
            else:
                text = slot_font.render(f"Slot {slot['slot']}: {slot['time']}", True, (255, 255, 255))
            screen.blit(text, (120, y + 20))
            slot_rects.append((rect, slot))

        back_font = pygame.font.Font(None, 24)
        back = back_font.render("[ESC] Back", True, (200, 200, 200))
        screen.blit(back, (20, SCREEN_HEIGHT - 40))

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    current_state = STATE_MENU
            if event.type == pygame.MOUSEBUTTONDOWN:
                mouse_pos = pygame.mouse.get_pos()
                for rect, slot in slot_rects:
                    if rect.collidepoint(mouse_pos) and slot["time"] != "Empty":
                        game = Game(screen)
                        game.load_slot(slot["slot"])
                        current_state = STATE_GAME

    elif current_state == STATE_GAME:
        if game:
            game.update()
            game.draw()
            if game.should_exit():
                current_state = STATE_MENU
                game = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()