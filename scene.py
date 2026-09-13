import pygame
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