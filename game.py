import pygame
import sys
from pygame import mask

class Scene:
    def __init__(self, screen, bg_path, collision_path, object_files, portals):
        self.screen = screen
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()

        # background
        self.bg = pygame.image.load(bg_path).convert()
        self.bg = pygame.transform.scale(self.bg, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # collision map
        self.collision_map = pygame.image.load(collision_path).convert_alpha()
        self.collision_map = pygame.transform.scale(self.collision_map, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))

        # objects
        self.objects_surfaces = []
        self.interaction_data = []

        for obj in object_files:
            if len(obj) == 5:
                filename, name, dialog, custom_pos, radius = obj
            elif len(obj) == 4:
                filename, name, dialog, custom_pos = obj
                radius = 70
            else:
                filename, name, dialog = obj
                custom_pos = None
                radius = 70

            try:
                img = pygame.image.load(filename).convert_alpha()
                orig_width = img.get_width()
                orig_height = img.get_height()

                img_scaled = pygame.transform.scale(img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
                self.objects_surfaces.append(img_scaled)

                rect = img.get_bounding_rect()
                if rect.width > 0 and rect.height > 0:
                    if custom_pos:
                        scaled_x, scaled_y = custom_pos
                    else:
                        orig_x = rect.x + rect.width // 2
                        orig_y = rect.y + rect.height // 2
                        scaled_x = int(orig_x * (self.SCREEN_WIDTH / orig_width))
                        scaled_y = int(orig_y * (self.SCREEN_HEIGHT / orig_height))

                    self.interaction_data.append({
                        "name": name,
                        "x": scaled_x,
                        "y": scaled_y,
                        "radius": radius,
                        "dialog": dialog
                    })
            except FileNotFoundError:
                print(f"{filename} not found")

        # collision mask
        self.obstacle_mask = self.create_obstacle_mask()

        # portals
        self.portals = portals

    def create_obstacle_mask(self):
        combined = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT), pygame.SRCALPHA)
        for img in self.objects_surfaces:
            combined.blit(img, (0, 0))
        return mask.from_surface(combined)

    def is_walkable(self, px, py):
        if px < 0 or px >= self.SCREEN_WIDTH or py < 0 or py >= self.SCREEN_HEIGHT:
            return False
        color = self.collision_map.get_at((int(px), int(py)))
        if color[0] > 200 and color[1] > 200 and color[2] > 200:
            return False
        return True

    def check_portal(self, char_rect):
        for portal in self.portals:
            if char_rect.colliderect(portal["rect"]):
                return portal
        return None

    def draw(self):
        self.screen.blit(self.bg, (0, 0))
        for img in self.objects_surfaces:
            self.screen.blit(img, (0, 0))


class Game:
    def __init__(self, screen):
        self.screen = screen
        self.SCREEN_WIDTH = screen.get_width()
        self.SCREEN_HEIGHT = screen.get_height()
        self.exit_requested = False
        self.show_inventory = False

        # create scenes
        self.scenes = {}

        # scene 1 : room1
        self.scenes["room1"] = Scene(
            screen,
            "assets/backgrounds/background.png",
            "assets/objects/room1/collision.png",
            [
                ("assets/objects/room1/Bed.png", "Bed", "Do you want to go to sleep?"),
                ("assets/objects/room1/Chair.png", "Chair", "Chair."),
                ("assets/objects/room1/Bed_desk.png", "Bed desk", "A small desk near the bed."),
                ("assets/objects/room1/Closet.png", "Closet", "Just some clothes inside"),
                ("assets/objects/room1/Desk.png", "Desk", "There's a diary on it"),
                ("assets/objects/room1/Diary.png", "Diary", "Do you want to read the diary?"),
                ("assets/objects/room1/Clock.png", "Clock", "It's not working."),
            ],
            portals=[
                {"rect": pygame.Rect(560, 265, 30, 115), "target": "room2", "spawn": (125, 250),
                 "name": "Corridor"}
            ]
        )

        # scene 2 : corridor
        self.scenes["room2"] = Scene(
            screen,
            "assets/backgrounds/Corridor.png",
            "assets/objects/corridor/collision2.png",
            [
                ("assets/objects/corridor/book_shelf.png", "Book shelf",
                 "Maybe it has something interesting.", (320, 229)),
                ("assets/objects/corridor/corriphoto.png", "Photos", "Good old days."),
            ],
            portals=[
                # to room 1
                {"rect": pygame.Rect(101, 163, 30, 33), "target": "room1",
                 "spawn": (500, 300), "name": "Room"},

                # to kitchen (key required)
                {"rect": pygame.Rect(195, 210, 73, 30), "target": "room3",
                 "spawn": (340, 250), "name": "Kitchen", "key_required": "key1"},

                # rooftop (key required)
                {"rect": pygame.Rect(647, 164, 30, 36), "target": "rooftop",
                 "spawn": (14, 240), "name": "Rooftop", "key_required": "key2"},

                # room 2 (key required)
                {"rect": pygame.Rect(555, 215, 70, 30), "target": "secret_room",
                 "spawn": (400, 250), "name": "Seren's room", "key_required": "key3"},
            ]
        )

        # scene 3: kitchen
        self.scenes["room3"] = Scene(
            screen,
            "assets/backgrounds/Room3 bg.png",
            "assets/objects/kitchen/collision3.png",
            [
                ("assets/objects/kitchen/Romm3couch.png", "Couch", "We used to chill here a lot."),
                ("assets/objects/kitchen/Room3chair1.png", "Chair", "A wooden chair."),
                ("assets/objects/kitchen/Room3chair2.png", "Chair", "Another chair."),
                ("assets/objects/kitchen/Room3chair3.png", "Chair", "Yet another chair."),
                ("assets/objects/kitchen/Room3clothstick.png", "Cloth stick", "His hat is still here."),
                ("assets/objects/kitchen/Room3fire.png", "Fireplace", "Better not play with fire."),
                ("assets/objects/kitchen/Room3tv.png", "TV", "Do you want to turn the TV on?"),
            ],
            portals=[
                {"rect": pygame.Rect(280, 259, 72, 30), "target": "room2", "spawn": (230, 200),
                 "name": "Corridor"}
            ]
        )

        # scene 4: rooftop (sky)
        self.scenes["rooftop"] = Scene(
            screen,
            "assets/backgrounds/skybg.png",
            "assets/objects/sky/Collision4.png",
            [],
            portals=[
                {"rect": pygame.Rect(0, 200, 30, 100), "target": "room2",
                 "spawn": (600, 250), "name": "Corridor"}
            ]
        )

        self.current_scene_name = "room1"
        self.scene = self.scenes[self.current_scene_name]

        # game process tracker
        self.keys_spawned = set()          # key appeared alr
        self.keys_collected = set()        # keys collected
        self.inventory = []
        self.bookshelf_checked = 0
        self.endings_seen = set()          # endings check
        self.total_endings = 3             # total endings to check

        # dialogue system
        self.dialogue_choices = None
        self.selected_choice = 0

        # character animation
        sample_frame = pygame.image.load("assets/characters/Zyrou/walk_1.PNG").convert_alpha()
        frame_width, frame_height = sample_frame.get_width(), sample_frame.get_height()
        self.CHAR_HEIGHT = 60
        self.CHAR_WIDTH = int(self.CHAR_HEIGHT * (frame_width / frame_height))

        self.walk_frames = []
        self.walk_masks = []

        for i in range(1, 5):
            frame = pygame.image.load(f"assets/characters/Zyrou/walk_{i}.PNG").convert_alpha()
            frame = pygame.transform.scale(frame, (self.CHAR_WIDTH, self.CHAR_HEIGHT))
            self.walk_frames.append(frame)
            self.walk_masks.append(mask.from_surface(frame))

        self.walk_frames_flipped = []
        self.walk_masks_flipped = []
        for f in self.walk_frames:
            flipped = pygame.transform.flip(f, True, False)
            self.walk_frames_flipped.append(flipped)
            self.walk_masks_flipped.append(mask.from_surface(flipped))

        # character position
        self.x = self.SCREEN_WIDTH // 2
        self.y = self.SCREEN_HEIGHT // 2
        self.speed = 3
        self.char_width = self.CHAR_WIDTH
        self.char_height = self.CHAR_HEIGHT

        self.current_frame = 0
        self.frame_counter = 0
        self.animation_speed = 6
        self.facing_right = True
        self.is_moving = False

        self.near_object = None
        self.current_portal = None
        self.pending_portal = None
        self.interact_text = ""
        self.text_timer = 0

    def spawn_key(self, key_name, dialog):
        filename = f"assets/objects/corridor/{key_name}.png"
        try:
            img = pygame.image.load(filename).convert_alpha()
            orig_width = img.get_width()
            orig_height = img.get_height()

            img_scaled = pygame.transform.scale(img, (self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            self.scenes["room2"].objects_surfaces.append(img_scaled)

            # get coord from solid part of image
            rect = img.get_bounding_rect()
            if rect.width > 0 and rect.height > 0:
                orig_x = rect.x + rect.width // 2
                orig_y = rect.y + rect.height // 2
                scaled_x = int(orig_x * (self.SCREEN_WIDTH / orig_width))
                scaled_y = int(orig_y * (self.SCREEN_HEIGHT / orig_height))

                self.scenes["room2"].interaction_data.append({
                    "name": key_name,
                    "x": scaled_x,
                    "y": scaled_y,
                    "radius": 70,
                    "dialog": dialog
                })
                self.scenes["room2"].obstacle_mask = self.scenes["room2"].create_obstacle_mask()
        except FileNotFoundError:
            print(f" {filename} not found")

    def check_all_endings(self):
        # to check if all endings are checked --> unlock key 3
        if len(self.endings_seen) >= self.total_endings:
            if "key3" not in self.keys_spawned and "key3" not in self.keys_collected:
                self.spawn_key("key3", "Why is there so many keys tho??", (550, 350))
                self.keys_spawned.add("key3")
                print("all endings are checked. You found key3.")

    def change_scene(self, target_scene, spawn_pos):
        self.current_scene_name = target_scene
        self.scene = self.scenes[target_scene]
        self.x, self.y = spawn_pos

    def check_near_object(self):
        char_center_x = self.x + self.char_width // 2
        char_center_y = self.y + self.char_height // 2

        for obj in self.scene.interaction_data:
            dx = char_center_x - obj["x"]
            dy = char_center_y - obj["y"]
            distance = (dx ** 2 + dy ** 2) ** 0.5
            if distance < obj["radius"]:
                return obj
        return None

    def interact(self):
        if self.near_object:
            name = self.near_object["name"]

            # bookshelf --> show choices
            if name == "Book shelf":
                self.interact_text = self.near_object["dialog"]
                self.text_timer = 120
                self.dialogue_choices = ["Check", "Leave"]
                self.selected_choice = 0

            # collect key(s) (I wanna go to bed so bad ngl)
            elif "key" in name:
                self.inventory.append(name)
                self.keys_collected.add(name)
                self.interact_text = f"{name} is now in your bag."
                self.text_timer = 120
                print("Key1 is now in your inventory.")

                for i, obj in enumerate(self.scene.interaction_data):
                    if obj["name"] == name:
                        # delete interaction data so that u wont get it again and again
                        self.scene.interaction_data.pop(i)
                        # remove image
                        if i < len(self.scene.objects_surfaces):
                            self.scene.objects_surfaces.pop(i)
                        break

                self.scene.obstacle_mask = self.scene.create_obstacle_mask()

            else:
                self.interact_text = self.near_object["dialog"]
                self.text_timer = 120

    def confirm_choice(self):
        if not self.dialogue_choices:
            return

        choice = self.dialogue_choices[self.selected_choice]

        # === 使用鑰匙開門 ===
        if choice.startswith("Use "):
            if self.pending_portal:
                # 記住要前往的場景
                target = self.pending_portal["target"]
                spawn = self.pending_portal["spawn"]

                # 清除選項和待處理的門
                self.dialogue_choices = None
                self.pending_portal = None

                # 切換場景
                self.change_scene(target, spawn)
                return

        # === 離開 ===
        elif choice == "Leave":
            self.interact_text = ""
            self.text_timer = 0
            self.pending_portal = None

        # === bookshelf 的 Check ===
        elif choice == "Check":
            self.bookshelf_checked += 1

            if self.bookshelf_checked == 1:
                if "key1" not in self.keys_spawned:
                    self.spawn_key("key1", "I found a key!")
                    self.keys_spawned.add("key1")

            elif self.bookshelf_checked == 2:
                if "key2" not in self.keys_spawned:
                    self.spawn_key("key2", "Another key?")
                    self.keys_spawned.add("key2")

            else:
                self.interact_text = "Nothing else here."
                self.text_timer = 120

        self.dialogue_choices = None

    def can_move_to(self, new_x, new_y):
        if new_x < 0 or new_x + self.char_width > self.SCREEN_WIDTH:
            return False
        if new_y < 0 or new_y + self.char_height > self.SCREEN_HEIGHT:
            return False

        corners = [
            (new_x, new_y),
            (new_x + self.char_width - 1, new_y),
            (new_x, new_y + self.char_height - 1),
            (new_x + self.char_width - 1, new_y + self.char_height - 1)
        ]
        for (cx, cy) in corners:
            if not self.scene.is_walkable(cx, cy):
                return False

        char_mask = self.walk_masks[self.current_frame] if self.facing_right else self.walk_masks_flipped[self.current_frame]
        offset = (int(new_x), int(new_y))
        if self.scene.obstacle_mask.overlap(char_mask, offset):
            return False
        return True

    def update(self):
        self.near_object = self.check_near_object()
        char_rect = pygame.Rect(self.x, self.y, self.char_width, self.char_height)
        self.current_portal = self.scene.check_portal(char_rect)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.exit_requested = True

            if event.type == pygame.KEYDOWN:

                # press i open inventory
                if event.key == pygame.K_i:
                    self.show_inventory = not self.show_inventory

                # choice control
                if self.dialogue_choices:
                    if event.key == pygame.K_UP:
                        self.selected_choice = (self.selected_choice - 1) % len(self.dialogue_choices)
                    if event.key == pygame.K_DOWN:
                        self.selected_choice = (self.selected_choice + 1) % len(self.dialogue_choices)
                    if event.key == pygame.K_SPACE:
                        self.confirm_choice()
                    continue

                # common interact
                if event.key == pygame.K_SPACE:
                    if self.current_portal:
                        # check if key's needed
                        key_required = self.current_portal.get("key_required")

                        if key_required:
                            # no key 4u --> locked
                            if key_required not in self.keys_collected:
                                self.interact_text = f"Locked. I need {key_required}."
                                self.text_timer = 120
                            else:
                                # yo theres a key :0 --> show choice
                                self.dialogue_choices = [f"Use {key_required}", "Leave"]
                                self.selected_choice = 0
                                self.pending_portal = self.current_portal  # 記住這個門
                        else:
                            # no key needed --> spawn directly"
                            self.change_scene(
                                self.current_portal["target"],
                                self.current_portal["spawn"]
                            )
                            return
                    else:
                        self.interact()

                if event.key == pygame.K_ESCAPE:
                    self.exit_requested = True

        # no movement during interaction
        if self.dialogue_choices or self.show_inventory:
            return

        # character movement
        keys = pygame.key.get_pressed()
        dx, dy = 0, 0

        if keys[pygame.K_LEFT]:
            dx = -self.speed
            self.facing_right = False
        if keys[pygame.K_RIGHT]:
            dx = self.speed
            self.facing_right = True
        if keys[pygame.K_UP]:
            dy = -self.speed
        if keys[pygame.K_DOWN]:
            dy = self.speed

        self.is_moving = (dx != 0 or dy != 0)

        if dx != 0:
            new_x = self.x + dx
            if self.can_move_to(new_x, self.y):
                self.x = new_x
        if dy != 0:
            new_y = self.y + dy
            if self.can_move_to(self.x, new_y):
                self.y = new_y

        char_rect = pygame.Rect(self.x, self.y, self.char_width, self.char_height)
        self.current_portal = self.scene.check_portal(char_rect)
        self.near_object = self.check_near_object()

        if self.text_timer > 0:
            self.text_timer -= 1
            if self.text_timer == 0:
                self.interact_text = ""

        if self.is_moving:
            self.frame_counter += 1
            if self.frame_counter >= self.animation_speed:
                self.frame_counter = 0
                self.current_frame = (self.current_frame + 1) % len(self.walk_frames)
        else:
            self.current_frame = 0
            self.frame_counter = 0

    def draw(self):
        self.scene.draw()

        # coordination assist
        font = pygame.font.Font(None, 24)
        coord_text = font.render(f"Char: ({self.x}, {self.y})", True, (255, 255, 0))
        self.screen.blit(coord_text, (10, 10))

        mouse_x, mouse_y = pygame.mouse.get_pos()
        mouse_text = font.render(f"Mouse: ({mouse_x}, {mouse_y})", True, (0, 255, 0))
        self.screen.blit(mouse_text, (10, 35))

        # portal hint
        if self.current_portal and not self.dialogue_choices:
            font = pygame.font.Font(None, 28)
            target_name = self.current_portal.get("name", "next area")
            hint_text = font.render(f"[space] {target_name}", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 120))

            s = pygame.Surface((hint_rect.width + 20, hint_rect.height + 10))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.screen.blit(s, (hint_rect.x - 10, hint_rect.y - 5))
            self.screen.blit(hint_text, hint_rect)

        # interaction hint
        if self.near_object and not self.dialogue_choices:
            font = pygame.font.Font(None, 24)
            hint_text = font.render("[SPACE]", True, (255, 255, 255))
            hint_rect = hint_text.get_rect(center=(self.near_object["x"], self.near_object["y"] - 40))
            self.screen.blit(hint_text, hint_rect)

        # text
        if self.interact_text:
            font = pygame.font.Font(None, 28)
            dialog_text = font.render(self.interact_text, True, (255, 255, 200))
            text_rect = dialog_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 60))

            s = pygame.Surface((text_rect.width + 20, text_rect.height + 30))
            s.set_alpha(180)
            s.fill((0, 0, 0))
            self.screen.blit(s, (text_rect.x - 10, text_rect.y - 5))
            self.screen.blit(dialog_text, text_rect)

        # choices (dialogue)
        if self.dialogue_choices:
            choice_font = pygame.font.Font(None, 32)
            start_y = self.SCREEN_HEIGHT - 120

            for i, choice in enumerate(self.dialogue_choices):
                color = (255, 255, 0) if i == self.selected_choice else (200, 200, 200)
                prefix = "> " if i == self.selected_choice else "  "
                choice_text = choice_font.render(f"{prefix}{choice}", True, color)
                choice_rect = choice_text.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 35))
                self.screen.blit(choice_text, choice_rect)

        # character
        if self.facing_right:
            self.screen.blit(self.walk_frames[self.current_frame], (self.x, self.y))
        else:
            self.screen.blit(self.walk_frames_flipped[self.current_frame], (self.x, self.y))

        # item list (inventory)
        if self.show_inventory:
            inv_bg = pygame.Surface((400, 300))
            inv_bg.set_alpha(200)
            inv_bg.fill((0, 0, 0))
            self.screen.blit(inv_bg, (self.SCREEN_WIDTH // 2 - 200, self.SCREEN_HEIGHT // 2 - 150))

            title_font = pygame.font.Font(None, 36)
            title = title_font.render("Inventory", True, (255, 255, 200))
            title_rect = title.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 - 120))
            self.screen.blit(title, title_rect)

            item_font = pygame.font.Font(None, 28)
            if self.inventory:
                for i, item in enumerate(self.inventory):
                    item_text = item_font.render(f"- {item}", True, (255, 255, 255))
                    self.screen.blit(item_text, (self.SCREEN_WIDTH // 2 - 150, self.SCREEN_HEIGHT // 2 - 60 + i * 35))
            else:
                empty_text = item_font.render("(Empty)", True, (150, 150, 150))
                empty_rect = empty_text.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                self.screen.blit(empty_text, empty_rect)

            hint_font = pygame.font.Font(None, 22)
            hint = hint_font.render("Press I to close", True, (200, 200, 200))
            hint_rect = hint.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2 + 120))
            self.screen.blit(hint, hint_rect)

    def save(self):
        import json
        data = {
            "scene": self.current_scene_name,
            "x": self.x,
            "y": self.y,
            "facing_right": self.facing_right,
            "keys_spawned": list(self.keys_spawned),
            "keys_collected": list(self.keys_collected),
            "inventory": self.inventory,
            "bookshelf_checked": self.bookshelf_checked,
            "endings_seen": list(self.endings_seen),
        }
        with open("save.json", "w") as f:
            json.dump(data, f)
        print("Noted.")

    def load(self):
        import json
        import os
        if os.path.exists("save.json"):
            with open("save.json", "r") as f:
                data = json.load(f)
            self.current_scene_name = data.get("scene", "room1")
            self.scene = self.scenes[self.current_scene_name]
            self.x = data.get("x", self.SCREEN_WIDTH // 2)
            self.y = data.get("y", self.SCREEN_HEIGHT // 2)
            self.facing_right = data.get("facing_right", True)
            self.keys_spawned = set(data.get("keys_spawned", []))
            self.keys_collected = set(data.get("keys_collected", []))
            self.inventory = data.get("inventory", [])
            self.bookshelf_checked = data.get("bookshelf_checked", 0)
            self.endings_seen = set(data.get("endings_seen", []))
            print("you start reading your diary...")
        else:
            print("you have not write anything on your diary yet.")

    def check_all_endings(self):
        #to see if all endings collected--> unlock key 3 to room 4
        if len(self.endings_seen) >= self.total_endings:
            if "key3" not in self.keys_spawned and "key3" not in self.keys_collected:
                self.spawn_key("key3", "He hid that much keys here??")
                self.keys_spawned.add("key3")
                print("a new key has been found in your inventory.")

    def should_exit(self):
        return self.exit_requested