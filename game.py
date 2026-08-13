import pygame
import sys
from pygame import mask

pygame.init()

ORIGINAL_WIDTH = 2240
ORIGINAL_HEIGHT = 1400
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 500

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Steps Till Dawn")
clock = pygame.time.Clock()

# background
bg = pygame.image.load("background.png").convert()
bg = pygame.transform.scale(bg, (SCREEN_WIDTH, SCREEN_HEIGHT))

# Obstacle mask (map)
collision_map = pygame.image.load("collision.png").convert_alpha()
collision_map = pygame.transform.scale(collision_map, (SCREEN_WIDTH, SCREEN_HEIGHT))

def is_walkable(px, py):
    if px < 0 or px >= SCREEN_WIDTH or py < 0 or py >= SCREEN_HEIGHT:
        return False
    color = collision_map.get_at((int(px), int(py)))
    if color[0] > 200 and color[1] > 200 and color[2] > 200:
        return False
    return True

# load interactive object
object_files = [
    ("Bed.png", "Bed", "Do you want to go to sleep?"),
    ("Chair.png", "Chair", "Chair."),
    ("Bed_desk.png", "Bed desk", "A small desk near the bed."),
    ("Closet.png", "Closet", "Just some clothes inside"),
    ("Desk.png", "Desk", "There's a diary on it"),
    ("Diary.png", "Diary", "Do you want to read the diary?"),
    ("Clock.png", "Clock", "It's not working."),
]

objects_surfaces = []
interaction_data = []

for filename, name, dialog in object_files:
    try:
        img = pygame.image.load(filename).convert_alpha()
        img_scaled = pygame.transform.scale(img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        objects_surfaces.append(img_scaled)

        # Calculate original coordinates
        rect = img.get_bounding_rect()
        if rect.width > 0 and rect.height > 0:
            orig_x = rect.x + rect.width // 2
            orig_y = rect.y + rect.height // 2
            scaled_x = int(orig_x * (SCREEN_WIDTH / ORIGINAL_WIDTH))
            scaled_y = int(orig_y * (SCREEN_HEIGHT / ORIGINAL_HEIGHT))

            interaction_data.append({
                "name": name,
                "x": scaled_x,
                "y": scaled_y,
                "radius": 50,
                "dialog": dialog
            })
        else:
            print(f"{filename} error")

    except FileNotFoundError:
        print(f"{filename} not found")

# Obstacle mask
def create_obstacle_mask():
    combined = pygame.Surface((SCREEN_WIDTH, SCREEN_HEIGHT), pygame.SRCALPHA)
    for img in objects_surfaces:
        combined.blit(img, (0, 0))
    return mask.from_surface(combined)

obstacle_mask = create_obstacle_mask()

# Character animation
sample_frame = pygame.image.load("walk_1.png").convert_alpha()
frame_width, frame_height = sample_frame.get_width(), sample_frame.get_height()
CHAR_HEIGHT = 60
CHAR_WIDTH = int(CHAR_HEIGHT * (frame_width / frame_height))

walk_frames = []
walk_masks = []
for i in range(1, 5):
    frame = pygame.image.load(f"walk_{i}.png").convert_alpha()
    frame = pygame.transform.scale(frame, (CHAR_WIDTH, CHAR_HEIGHT))
    walk_frames.append(frame)
    walk_masks.append(mask.from_surface(frame))

walk_frames_flipped = []
walk_masks_flipped = []
for f in walk_frames:
    flipped = pygame.transform.flip(f, True, False)
    walk_frames_flipped.append(flipped)
    walk_masks_flipped.append(mask.from_surface(flipped))

# Character settings
x, y = SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2
speed = 3
char_width, char_height = CHAR_WIDTH, CHAR_HEIGHT

current_frame = 0
frame_counter = 0
animation_speed = 6
facing_right = True
is_moving = False

# Interaction
near_object = None
interact_text = ""
text_timer = 0

def check_near_object():
    char_center_x = x + char_width // 2
    char_center_y = y + char_height // 2

    for obj in interaction_data:
        dx = char_center_x - obj["x"]
        dy = char_center_y - obj["y"]
        distance = (dx ** 2 + dy ** 2) ** 0.5

        if distance < obj["radius"]:
            return obj
    return None

def interact():
    global interact_text, text_timer
    if near_object:
        interact_text = near_object["dialog"]
        text_timer = 120

def can_move_to(new_x, new_y):
    if new_x < 0 or new_x + char_width > SCREEN_WIDTH:
        return False
    if new_y < 0 or new_y + char_height > SCREEN_HEIGHT:
        return False

    corners = [
        (new_x, new_y),
        (new_x + char_width - 1, new_y),
        (new_x, new_y + char_height - 1),
        (new_x + char_width - 1, new_y + char_height - 1)
    ]
    for (cx, cy) in corners:
        if not is_walkable(cx, cy):
            return False

    char_mask = walk_masks[current_frame] if facing_right else walk_masks_flipped[current_frame]
    offset = (int(new_x), int(new_y))

    if obstacle_mask.overlap(char_mask, offset):
        return False
    return True

# Main loop
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                interact()

    keys = pygame.key.get_pressed()
    dx, dy = 0, 0

    if keys[pygame.K_LEFT]:
        dx = -speed
        facing_right = False
    if keys[pygame.K_RIGHT]:
        dx = speed
        facing_right = True
    if keys[pygame.K_UP]:
        dy = -speed
    if keys[pygame.K_DOWN]:
        dy = speed

    is_moving = (dx != 0 or dy != 0)

    if dx != 0:
        new_x = x + dx
        if can_move_to(new_x, y):
            x = new_x
    if dy != 0:
        new_y = y + dy
        if can_move_to(x, new_y):
            y = new_y

    near_object = check_near_object()

    if text_timer > 0:
        text_timer -= 1
        if text_timer == 0:
            interact_text = ""

    if is_moving:
        frame_counter += 1
        if frame_counter >= animation_speed:
            frame_counter = 0
            current_frame = (current_frame + 1) % len(walk_frames)
    else:
        current_frame = 0
        frame_counter = 0

    screen.blit(bg, (0, 0))

    for img in objects_surfaces:
        screen.blit(img, (0, 0))

    # interaction hint
    if near_object:
        font = pygame.font.Font(None, 24)
        hint_text = font.render("[SPACE]", True, (255, 255, 255))
        hint_rect = hint_text.get_rect(center=(near_object["x"], near_object["y"] - 40))
        screen.blit(hint_text, hint_rect)

    # interaction text
    if interact_text:
        font = pygame.font.Font(None, 28)
        dialog_text = font.render(interact_text, True, (255, 255, 200))
        text_rect = dialog_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT - 30))

        s = pygame.Surface((text_rect.width + 20, text_rect.height + 10))
        s.set_alpha(180)
        s.fill((0, 0, 0))
        screen.blit(s, (text_rect.x - 10, text_rect.y - 5))
        screen.blit(dialog_text, text_rect)

    if facing_right:
        screen.blit(walk_frames[current_frame], (x, y))
    else:
        screen.blit(walk_frames_flipped[current_frame], (x, y))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()