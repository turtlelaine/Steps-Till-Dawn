import pygame
from pygame import mask
from story import STORY
from scene import Scene

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
                ("assets/objects/room1/Bed_desk.png", "Clock", "A small desk near the bed."),
                ("assets/objects/room1/Closet.png", "Closet", "Just some clothes inside"),
                ("assets/objects/room1/Desk.png", "Desk", "There's a diary on it"),
                ("assets/objects/room1/Diary.png", "Diary", "Do you want to read the diary?"),
                ("assets/objects/room1/Clock.png", "Frame", "It's not working."),
            ],
            portals=[
                {"rect": pygame.Rect(560, 265, 30, 115), "target": "room2", "spawn": (125, 250),
                 "name": "Corridor"}
            ]
        )

        # scene 2 : corridor
        self.first_rooftop = False
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
                {"rect": pygame.Rect(555, 215, 70, 30), "target": "room5",
                 "spawn": (270, 258), "name": "Seren's room", "key_required": "key3"},
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

        # scene 5 : room2 (Seren's room)
        self.scenes["room5"] = Scene(
            screen,
            "assets/backgrounds/room3bg.png",
            "assets/objects/room2/Collision5.png",
            [
                ("assets/objects/room2/Bed2.png", "Bed", "Seren's bed. Still comfy."),
                ("assets/objects/room2/Books.png", "Books", "A stack of books. Some are half-read."),
                ("assets/objects/room2/Chair2.png", "Chair", "Best chair."),
                ("assets/objects/room2/Closet2.png", "Closet", "It's a mess inside."),
                ("assets/objects/room2/Desk2.png", "Desk", "Neatly tidied."),
                ("assets/objects/room2/Diary2.png", "Diary2", "One glance won't hurt..."),
                ("assets/objects/room2/Music.png", "Music", "Plays Seren's favorite album."),
            ],
            portals=[
                {"rect": pygame.Rect(250, 268, 48, 30), "target": "room2",
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
        self.kitchen_unlocked = False
        self.endings_seen = self.load_endings()          # endings check
        self.total_endings = 5             # total endings to checc

        # dialogue system
        self.dialogue_choices = None
        self.selected_choice = 0

        # Zyrou animation
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

        # Seren animation
        self.seren_frames = []
        self.seren_frames_flipped = []
        self.seren_frame_index = 0
        self.seren_frame_counter = 0
        self.seren_animation_speed = 8

        for i in range(1, 5):
            frame = pygame.image.load(f"assets/characters/Seren/seren{i}.PNG").convert_alpha()
            frame = pygame.transform.scale(frame, (self.CHAR_WIDTH, self.CHAR_HEIGHT))
            self.seren_frames.append(frame)

            flipped = pygame.transform.flip(frame, True, False)
            self.seren_frames_flipped.append(flipped)

        self.seren_facing_right = False
        self.seren_scene = None

        self.seren_x = 600
        self.seren_y = 250
        self.seren_visible = False
        self.seren_reached = False
        self.seren_attempts = 0

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

        # story setting
        self.story_active = False
        self.story_id = None
        self.story_line_index = 0
        self.story_lines = []
        self.story_choices = None
        self.sleep_count = 0             # ending 1
        self.triggered_stories = set()   # ending count
        self.story_alpha = 0             # fade in intro
        self.story_fade_speed = 4
        self.fade_state = None
        self.fade_alpha = 0
        self.fade_speed = 3
        self.books_checked = False

        self.start_story("intro")

        # scene settings
        self.timer_active = False
        self.timer_start = 0
        self.timer_duration = 2.5
        self.loop_count = 0
        self.fade_next_story = None

        self.rooftop_triggered = False

        self.story_position = "center"
        self.tv_disabled = False
        self.true_ending_unlocked = False

        #timer in kitchen scene
        self.kitchen_timer_active = False
        self.kitchen_timer_start = 0
        self.kitchen_timer_duration = 180
        self.tv_opened = False

        # for ending test
        #self.endings_seen = {"ending1", "ending2", "ending3", "ending4", "ending5"}
        #self.check_all_endings()

    def load_endings(self):
        import json
        import os
        if os.path.exists("endings.json"):
            with open("endings.json", "r") as f:
                return set(json.load(f))
        return set()

    def save_endings(self):
        import json
        with open("endings.json", "w") as f:
            json.dump(list(self.endings_seen), f)

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

    def start_story(self, story_id):

        self.story_active = True
        self.story_id = story_id
        self.story_line_index = 0
        self.story_lines = STORY[story_id]["lines"]
        self.story_choices = None
        self.story_alpha = 0
        self.story_position = STORY[story_id].get("position", "center")

    def next_story_line(self):
        if not self.story_active or self.story_id is None:
            self.story_active = False
            return

        if self.story_line_index < len(self.story_lines) - 1:
            self.story_line_index += 1
        else:
            # to check if there's next dialogue
            story = STORY[self.story_id]

            if story.get("choices"):
                self.dialogue_choices = [c[0] for c in story["choices"]]
                self.selected_choice = 0
                self.story_choices = story["choices"]
            else:
                self.end_story()

    def end_story(self):
        story = STORY[self.story_id]

        on_end = story.get("on_end")
        if on_end:
            self.handle_story_action(on_end)
            return

        next_story = story.get("next")
        if next_story:
            self.start_story(next_story)
            return

        self.clear_story()

    def clear_story(self):
        self.story_active = False
        self.story_id = None
        self.story_lines = []
        self.story_line_index = 0
        self.story_choices = None
        self.dialogue_choices = None

    def handle_story_action(self, action):
        if action == "go_to_rooftop":
            self.change_scene("rooftop", (400, 248))
            self.rooftop_triggered = False
            self.facing_right = True
            self.seren_scene = "rooftop"
            self.seren_facing_right = True
            self.seren_visible = True
            self.seren_reached = False
            self.first_rooftop = True
            self.start_story("rooftop_arrival")
            return

        elif action == "hide_seren_and_fade":
            self.seren_visible = False
            self.seren_reached = True

            self.clear_story()

            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "rooftop_black"
            return

        elif action == "hide_seren_and_back":
            self.seren_visible = False

            self.change_scene("room1", (400, 250))
            self.facing_right = True

            self.clear_story()

            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "wake_up"
            return

        elif action == "hide_seren_and_start_timer":
            self.seren_visible = False

            self.timer_active = True
            self.timer_start = pygame.time.get_ticks()

            self.clear_story()
            return

        elif action == "fade_to_black":
            self.clear_story()

            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "rooftop_black"
            return

        elif action == "back_to_room1":
            self.change_scene("room1", (400, 250))
            self.facing_right = True

            self.clear_story()

            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "wake_up"
            return

        elif action == "back_to_room1_fail_action":
            self.change_scene("room1", (400, 250))
            self.facing_right = True

            self.clear_story()

            self.fade_state = "fade_in"
            self.fade_alpha = 255
            return

        elif action == "loop_count":
            self.loop_count += 1
            print(f"Loop count: {self.loop_count}")

            self.change_scene("rooftop", (100, 248))
            self.facing_right = True
            self.seren_scene = "rooftop"
            self.seren_facing_right = True
            self.seren_visible = True
            self.seren_reached = False
            self.first_rooftop = False
            self.clear_story()

            if self.loop_count >= 3:
                self.seren_attempts = 3
            else:
                self.seren_attempts = self.loop_count

            return

        elif action == "final_loop":
            self.change_scene("room1", (400, 248))
            self.facing_right = True
            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "ending2"
            return

        elif action == "back_to_room1_fail":
            self.change_scene("room1", (400, 250))
            self.facing_right = True

            self.clear_story()

            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "wake_up"
            return

        elif action == "start_timer":
            self.timer_active = True
            self.timer_start = pygame.time.get_ticks()
            return

        elif action == "wake_up_kitchen":
            self.change_scene("room3", (325, 220))
            self.facing_right = True
            self.seren_facing_right = False

            self.seren_x = 385
            self.seren_y = 220
            self.seren_scene = "room3"
            self.seren_visible = True
            self.seren_reached = True
            self.kitchen_unlocked = True

            if not any(obj["name"] == "Seren" for obj in self.scenes["room3"].interaction_data):
                self.scenes["room3"].interaction_data.append({
                    "name": "Seren",
                    "x": 385,
                    "y": 220,
                    "radius": 70,
                    "dialog": '"?"'
                })

            self.clear_story()
            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "wake_up_kitchen"
            return

        elif action == "start_kitchen_timer":
            self.kitchen_timer_active = True
            self.kitchen_timer_start = pygame.time.get_ticks()
            self.clear_story()
            return

        elif action == "tv_on":
            self.clear_story()
            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "after_tv"
            return

        elif action == "back_to_kitchen":
            self.clear_story()
            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "seren_confront"
            return

        elif action == "leave_kitchen":
            self.clear_story()
            self.seren_visible = True
            self.seren_scene = "room3"
            self.seren_facing_right = False
            self.true_ending_unlocked = True
            self.tv_disabled = True

            for obj in self.scenes["room3"].interaction_data[:]:
                if obj["name"] == "Seren":
                    self.scenes["room3"].interaction_data.remove(obj)
            return

        elif action == "back_to_room1_true":
            self.change_scene("room1", (400, 250))
            self.facing_right = True
            self.seren_visible = False
            self.seren_scene = None

            self.clear_story()
            self.fade_state = "fade_in"
            self.fade_alpha = 255
            self.fade_next_story = "true_ending_1"
            return

        elif action == "sleep_count":
            self.sleep_count += 1
            print(f"Sleep count: {self.sleep_count}")

            self.clear_story()

            if self.sleep_count >= 3:
                self.start_story("ending1")
            else:
                self.fade_state = "fade_in"
                self.fade_alpha = 255
            return

        elif action == "ending":
            self.endings_seen.add(self.story_id)
            self.save_endings()
            print(f"You get: {self.story_id}")
            self.check_all_endings()
            self.exit_requested = True

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

            # trigger clock
            if name == "Clock":
                if self.true_ending_unlocked:
                    self.start_story("before_true_ending")
                elif "clock_found" not in self.triggered_stories:
                    self.triggered_stories.add("clock_found")
                    self.start_story("clock_found")
                elif self.loop_count >= 3:
                    self.interact_text = "The clock is still stopped."
                    self.text_timer = 120
                else:
                    self.start_story("rewind_again")

            # trigger sleep
            elif name == "Bed":
                self.start_story("go_sleep")

            # book shelf
            elif name == "Book shelf":
                self.interact_text = self.near_object["dialog"]
                self.text_timer = 120
                self.dialogue_choices = ["Check", "Leave"]
                self.selected_choice = 0

            # key
            elif "key" in name:
                self.inventory.append(name)
                self.keys_collected.add(name)
                self.interact_text = f"{name} is now in your bag."
                self.text_timer = 120
                print(f"{name} is now in your inventory.")

                for i, obj in enumerate(self.scene.interaction_data):
                    if obj["name"] == name:
                        self.scene.interaction_data.pop(i)
                        if i < len(self.scene.objects_surfaces):
                            self.scene.objects_surfaces.pop(i)
                        break

                self.scene.obstacle_mask = self.scene.create_obstacle_mask()

            # Seren (scene kithen)
            elif name == "Seren":
                if self.kitchen_unlocked:
                    self.start_story("seren_talk")
                else:
                    self.interact_text = "..."
                    self.text_timer = 120

            # TV (scene kitchen)
            elif name == "TV":
                if self.tv_disabled:
                    self.interact_text = "..."
                    self.text_timer = 120
                elif not self.kitchen_unlocked:
                    self.interact_text = "The TV is off. You don't feel like watching anything."
                    self.text_timer = 120
                elif not self.tv_opened:
                    self.start_story("tv_interact")
                else:
                    self.interact_text = "The TV is already on."
                    self.text_timer = 120

            # Seren's diary (room2)
            elif name == "Diary2":
                self.start_story("seren_diary_1")

            elif name == "Books":
                if not self.books_checked:
                    self.books_checked = True
                    self.start_story("books_secret")
                else:
                    self.interact_text = "Just some books."
                    self.text_timer = 120

            # blabla
            else:
                self.interact_text = self.near_object["dialog"]
                self.text_timer = 120

    def confirm_choice(self):
        if not self.dialogue_choices:
            return

        choice = self.dialogue_choices[self.selected_choice]

        # open door 1 and rooftop by key 1 2
        if choice.startswith("Use "):
            if self.pending_portal:
                target = self.pending_portal["target"]
                spawn = self.pending_portal["spawn"]

                self.dialogue_choices = None
                self.pending_portal = None

                self.change_scene(target, spawn)
                return

        elif choice == "Leave":
            self.interact_text = ""
            self.text_timer = 0
            self.pending_portal = None

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

        elif choice == "Turn on":
            self.kitchen_timer_active = False
            self.tv_opened = True
            self.start_story("tv_on_story")
            return

        elif choice == "Never mind":
            self.interact_text = "You wanted to do something else."
            self.text_timer = 0
            self.dialogue_choices = None
            return

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
        # timer for scene rooftop
        if self.timer_active:
            elapsed = (pygame.time.get_ticks() - self.timer_start) / 1000
            remaining = self.timer_duration - elapsed

            if remaining <= 0:
                self.timer_active = False
                self.start_story("ending2")
                return

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_requested = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.timer_active = False
                        self.start_story("rewind_final")
                        return


        # timer for scene kitchen
        if self.kitchen_timer_active:
            elapsed = (pygame.time.get_ticks() - self.kitchen_timer_start) / 1000
            remaining = self.kitchen_timer_duration - elapsed
            if remaining <= 0:
                self.kitchen_timer_active = False
                self.start_story("ending3")
                return

        # fade in scene
        if self.fade_state == "fade_in":
            self.fade_alpha -= self.fade_speed
            if self.fade_alpha <= 0:
                self.fade_alpha = 0
                self.fade_state = None
            return

        if self.fade_next_story:
            next_story = self.fade_next_story
            self.fade_next_story = None
            self.start_story(next_story)

        if self.story_active:
            if self.story_alpha < 255:
                self.story_alpha += self.story_fade_speed
                if self.story_alpha > 255:
                    self.story_alpha = 255

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.exit_requested = True
                if event.type == pygame.KEYDOWN:
                    if self.dialogue_choices:
                        if event.key == pygame.K_UP:
                            self.selected_choice = (self.selected_choice - 1) % len(self.dialogue_choices)
                        if event.key == pygame.K_DOWN:
                            self.selected_choice = (self.selected_choice + 1) % len(self.dialogue_choices)
                        if event.key == pygame.K_SPACE:
                            chosen = self.story_choices[self.selected_choice]
                            next_story_id = chosen[1]
                            self.dialogue_choices = None
                            self.story_choices = None

                            if next_story_id:
                                self.start_story(next_story_id)
                            else:
                                self.end_story()
                    else:
                        if event.key == pygame.K_SPACE:
                            self.next_story_line()
            return  # stop interaction during story

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

                # press s to save
                if event.key == pygame.K_s:
                    self.save_slot()

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
                                self.pending_portal = self.current_portal
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
        # rooftop scene story
        keys = pygame.key.get_pressed()
        if (self.current_scene_name == "rooftop"
                and self.first_rooftop
                and not self.rooftop_triggered
                and keys[pygame.K_RIGHT]):
            self.rooftop_triggered = True
            self.start_story("rooftop_trigger")
            return

        if (self.current_scene_name == "rooftop"
                and not self.first_rooftop
                and self.seren_visible
                and not self.seren_reached):

            char_rect = pygame.Rect(self.x, self.y, self.char_width, self.char_height)
            seren_rect = pygame.Rect(self.seren_x, self.seren_y, 40, 60)

            if char_rect.colliderect(seren_rect):
                self.seren_reached = True
                self.seren_visible = False

                if self.loop_count >= 3:
                    self.start_story("reach_seren")
                else:
                    self.start_story("rooftop_fail")
                return
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

        if self.seren_visible and self.current_scene_name == self.seren_scene:
            self.seren_frame_counter += 1
            if self.seren_frame_counter >= self.seren_animation_speed:
                self.seren_frame_counter = 0
                self.seren_frame_index = (self.seren_frame_index + 1) % len(self.seren_frames)

    def draw(self):
        if self.story_active:
            self.draw_story()
            return

        self.scene.draw()

        if self.seren_visible and self.current_scene_name == self.seren_scene:
            if self.seren_facing_right:
                self.screen.blit(self.seren_frames[self.seren_frame_index],
                                 (self.seren_x, self.seren_y))
            else:
                self.screen.blit(self.seren_frames_flipped[self.seren_frame_index],
                                 (self.seren_x, self.seren_y))

        # timer
        if self.timer_active:
            elapsed = (pygame.time.get_ticks() - self.timer_start) / 1000
            remaining = max(0, self.timer_duration - elapsed)

            timer_font = pygame.font.Font(None, 72)
            timer_text = timer_font.render(f"{remaining:.1f}", True, (255, 50, 50))
            timer_rect = timer_text.get_rect(center=(self.SCREEN_WIDTH // 2, 80))
            self.screen.blit(timer_text, timer_rect)

            hint_font = pygame.font.Font(None, 28)
            hint = hint_font.render("[SPACE] Rewind time!", True, (255, 255, 255))
            hint_rect = hint.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 60))
            self.screen.blit(hint, hint_rect)

        if self.fade_state == "fade_in" and self.fade_alpha > 0:
            fade_surface = pygame.Surface((self.SCREEN_WIDTH, self.SCREEN_HEIGHT))
            fade_surface.fill((0, 0, 0))
            fade_surface.set_alpha(self.fade_alpha)
            self.screen.blit(fade_surface, (0, 0))

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
            font = pygame.font.Font(None, 20)
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

    def draw_story(self):
        if self.story_position == "bottom":
            self.scene.draw()

            # character
            if self.facing_right:
                self.screen.blit(self.walk_frames[self.current_frame], (self.x, self.y))
            else:
                self.screen.blit(self.walk_frames_flipped[self.current_frame], (self.x, self.y))

            # Seren
            if self.seren_visible and self.current_scene_name == self.seren_scene:
                if self.seren_facing_right:
                    self.screen.blit(self.seren_frames[self.seren_frame_index],
                                     (self.seren_x, self.seren_y))
                else:
                    self.screen.blit(self.seren_frames_flipped[self.seren_frame_index],
                                     (self.seren_x, self.seren_y))
        else:
            self.screen.fill((0, 0, 0))

        # show convo
        if self.story_lines and self.story_line_index < len(self.story_lines):
            font = pygame.font.Font(None, 32)
            line_text = self.story_lines[self.story_line_index]
            text_surface = font.render(line_text, True, (255, 255, 255))
            text_surface.set_alpha(self.story_alpha)

            if self.story_position == "bottom":
                # dialog bubble position: bottom
                dialog_height = 120
                dialog_y = self.SCREEN_HEIGHT - dialog_height

                dialog_bg = pygame.Surface((self.SCREEN_WIDTH, dialog_height))
                dialog_bg.set_alpha(200)
                dialog_bg.fill((0, 0, 0))
                self.screen.blit(dialog_bg, (0, dialog_y))

                pygame.draw.rect(self.screen, (255, 255, 255),
                                 (10, dialog_y + 10, self.SCREEN_WIDTH - 20, dialog_height - 20), 2)

                text_rect = text_surface.get_rect(topleft=(40, dialog_y + 30))
                self.screen.blit(text_surface, text_rect)

                if self.dialogue_choices:
                    choice_font = pygame.font.Font(None, 28)
                    start_y = dialog_y + 54
                    for i, choice in enumerate(self.dialogue_choices):
                        color = (255, 255, 0) if i == self.selected_choice else (180, 180, 180)
                        prefix = "> " if i == self.selected_choice else "  "
                        choice_text = choice_font.render(f"{prefix}{choice}", True, color)
                        choice_text.set_alpha(self.story_alpha)
                        self.screen.blit(choice_text, (60, start_y + i * 20))

                if not self.dialogue_choices and self.story_alpha >= 255:
                    hint_font = pygame.font.Font(None, 20)
                    hint = hint_font.render("[SPACE] ▼", True, (150, 150, 150))
                    hint_rect = hint.get_rect(bottomright=(self.SCREEN_WIDTH - 30, self.SCREEN_HEIGHT - 20))
                    self.screen.blit(hint, hint_rect)

            else:
                text_rect = text_surface.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT // 2))
                self.screen.blit(text_surface, text_rect)

                if self.dialogue_choices:
                    choice_font = pygame.font.Font(None, 32)
                    start_y = self.SCREEN_HEIGHT // 2 + 60
                    for i, choice in enumerate(self.dialogue_choices):
                        color = (255, 255, 0) if i == self.selected_choice else (180, 180, 180)
                        prefix = "> " if i == self.selected_choice else "  "
                        choice_text = choice_font.render(f"{prefix}{choice}", True, color)
                        choice_text.set_alpha(self.story_alpha)
                        choice_rect = choice_text.get_rect(center=(self.SCREEN_WIDTH // 2, start_y + i * 40))
                        self.screen.blit(choice_text, choice_rect)

                if not self.dialogue_choices and self.story_alpha >= 255:
                    hint_font = pygame.font.Font(None, 24)
                    hint = hint_font.render("Press [SPACE] to continue", True, (120, 120, 120))
                    hint_rect = hint.get_rect(center=(self.SCREEN_WIDTH // 2, self.SCREEN_HEIGHT - 40))
                    self.screen.blit(hint, hint_rect)

    def load_slot(self, slot_num):
        import json
        import os
        filename = f"save_slot_{slot_num}.json"
        if os.path.exists(filename):
            with open(filename, "r") as f:
                data = json.load(f)

            # load location
            self.current_scene_name = data.get("scene", "room1")
            self.scene = self.scenes[self.current_scene_name]
            self.x = data.get("x", self.SCREEN_WIDTH // 2)
            self.y = data.get("y", self.SCREEN_HEIGHT // 2)
            self.facing_right = data.get("facing_right", True)

            # load key status
            self.keys_spawned = set(data.get("keys_spawned", []))
            self.keys_collected = set(data.get("keys_collected", []))
            self.inventory = data.get("inventory", [])
            self.bookshelf_checked = data.get("bookshelf_checked", 0)

            # load stories process
            self.triggered_stories = set(data.get("triggered_stories", []))
            self.loop_count = data.get("loop_count", 0)
            self.sleep_count = data.get("sleep_count", 0)

            # load kitchen
            self.kitchen_unlocked = data.get("kitchen_unlocked", False)
            self.tv_opened = data.get("tv_opened", False)
            self.tv_disabled = data.get("tv_disabled", False)

            # load endings
            self.endings_seen = set(data.get("endings_seen", []))
            self.true_ending_unlocked = data.get("true_ending_unlocked", False)

            # 彩蛋：D
            self.books_checked = data.get("books_checked", False)

            # restart status
            self.clear_story()
            self.fade_state = None
            self.fade_alpha = 0
            self.fade_next_story = None
            self.timer_active = False
            self.kitchen_timer_active = False

            # reset seren status
            self.seren_visible = data.get("seren_visible", False)
            self.seren_scene = data.get("seren_scene", None)
            self.seren_x = data.get("seren_x", 600)
            self.seren_y = data.get("seren_y", 250)
            self.seren_facing_right = data.get("seren_facing_right", False)
            self.seren_reached = data.get("seren_reached", False)
            self.first_rooftop = data.get("first_rooftop", False)
            self.rooftop_triggered = data.get("rooftop_triggered", False)

            print(f"loaded slot {slot_num}")
            return True
        return False

    def save_slot(self):
        import json
        import os
        from datetime import datetime

        # read current save
        slots = []
        for i in range(1, 4):
            filename = f"save_slot_{i}.json"
            if os.path.exists(filename):
                with open(filename, "r") as f:
                    slots.append(json.load(f))
            else:
                slots.append(None)

        # wheres walley(check for empty slot)
        empty_slot = None
        for i, slot in enumerate(slots):
            if slot is None:
                empty_slot = i + 1
                break

        # cover oldest slot if no empty
        if empty_slot is None:
            oldest_time = None
            oldest_slot = 1
            for i, slot in enumerate(slots):
                if slot:
                    slot_time = slot.get("time", "")
                    if oldest_time is None or slot_time < oldest_time:
                        oldest_time = slot_time
                        oldest_slot = i + 1
            empty_slot = oldest_slot

        # save all process
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
            "loop_count": self.loop_count,
            "sleep_count": self.sleep_count,
            "kitchen_unlocked": self.kitchen_unlocked,
            "tv_opened": self.tv_opened,
            "triggered_stories": list(self.triggered_stories),
            "books_checked": self.books_checked,
            "tv_disabled": self.tv_disabled,
            "true_ending_unlocked": self.true_ending_unlocked,
            "time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "name": f"Slot {empty_slot}",
            "seren_visible": self.seren_visible,
            "seren_scene": self.seren_scene,
            "seren_x": self.seren_x,
            "seren_y": self.seren_y,
            "seren_facing_right": self.seren_facing_right,
            "seren_reached": self.seren_reached,
            "first_rooftop": self.first_rooftop,
            "rooftop_triggered": self.rooftop_triggered,
        }

        filename = f"save_slot_{empty_slot}.json"
        with open(filename, "w") as f:
            json.dump(data, f)

        print(f"saved to slot {empty_slot}")
        self.interact_text = f"You wrote your diary at page {empty_slot}"
        self.text_timer = 120

    def check_all_endings(self):
        #to see if all endings collected--> unlock key 3 to room 4
        if len(self.endings_seen) >= self.total_endings:
            if "key3" not in self.keys_spawned and "key3" not in self.keys_collected:
                self.spawn_key("key3", "He hid that much keys here??")
                self.keys_spawned.add("key3")
                print("a new key has been found in your inventory.")

    def should_exit(self):
        return self.exit_requested