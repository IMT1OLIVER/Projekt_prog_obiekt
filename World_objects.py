import pygame
import random
from Settings import *


import pygame
import random
from Settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, x, y):
        super().__init__()
        width = random.randint(*PLATFORM_WIDTH_RANGE)
        height = 20 # Wysokość wizualna

        # Ładowanie grafiki
        try:
            img = pygame.image.load(PLATFORM_IMAGE_PATH).convert_alpha()
            # Skalujemy grafikę do rozmiaru wylosowanej platformy
            self.image = pygame.transform.scale(img, (width, height))
        except:
            # Fallback (gdyby nie było pliku)
            self.image = pygame.Surface((width, height))
            self.image.fill(GREEN)
            pygame.draw.rect(self.image, (30, 100, 30), (0, 0, width, height), 3)

        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y

class Lava(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        # Lawa jest szersza niż ekran i wysoka
        self.image = pygame.Surface((SCREEN_WIDTH + 20, 1000))
        self.image.fill(LAVA_COLOR)
        self.image.set_alpha(200)  # Przezroczystość

        self.rect = self.image.get_rect()
        self.rect.x = -10
        self.rect.y = SCREEN_HEIGHT + 50  # Startuje pod ekranem

    def update(self):
        # Lawa ciągle idzie w górę
        self.rect.y -= LAVA_SPEED