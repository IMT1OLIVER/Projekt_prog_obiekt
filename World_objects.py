import pygame
import random
import math
from Settings import *

class Platform(pygame.sprite.Sprite):
    def __init__(self, game, x, y): # Dodaliśmy game, aby znać trudność
        super().__init__()
        self.game = game
        
        # Obliczamy szerokość na podstawie trudności gry
        base_width = random.randint(*PLATFORM_WIDTH_RANGE)
        width = max(PLATFORM_MIN_WIDTH, int(base_width / self.game.difficulty)) #im wyzsza trudnosc, tym mniejsza szerokosc platform
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
    def __init__(self, game): # Dodaliśmy game
        super().__init__()
        self.game = game

        try:
            # Ładujemy teksturę lawy
            lava_tile = pygame.image.load(LAVA_IMAGE_PATH).convert_alpha()
            tile_w, tile_h = lava_tile.get_size()

            # Tworzymy powierzchnię znacznie szerszą niż ekran
            self.image = pygame.Surface((SCREEN_WIDTH + 200, 1000), pygame.SRCALPHA)

            # Wypełniamy kafelkami
            for x in range(0, self.image.get_width(), tile_w):
                for y in range(0, self.image.get_height(), tile_h):
                    self.image.blit(lava_tile, (x, y))
        except:
            # Fallback
            self.image = pygame.Surface((SCREEN_WIDTH + 200, 1000))
            self.image.fill(LAVA_COLOR)
            self.image.set_alpha(180)

        self.rect = self.image.get_rect()
        # Startowa pozycja - wyśrodkowana szerokość z zapasem na ruch
        self.rect.x = -100
        self.rect.y = SCREEN_HEIGHT + 100

        self.angle = 0  # Potrzebne do obliczania falowania

    def update(self):
        # 1. Obliczanie dynamicznej prędkości (pogoń + trudność)
        #Jeśli gracz ucieknie bardzo wysoko, lawa dostaje ogromny bonus do prędkości by go dogonic
        #zwalnia, gdy jest blisko, dając szansę na ucieczkę.
        distance = self.rect.top - self.game.player.rect.bottom
        current_base_speed = LAVA_START_SPEED * self.game.difficulty #predkosc lawy mnozona przez trudnosc
        
        current_speed = current_base_speed + (max(0, distance) * LAVA_CHASE_FACTOR)
        current_speed = min(current_speed, LAVA_MAX_SPEED)

        # Ruch w górę
        self.rect.y -= current_speed

        # 2. Efekt płynności (falowanie na boki)
        self.angle += 0.05  # Prędkość falowania
        # Sinus zwraca wartość od -1 do 1, mnożymy przez amplitudę (np. 15 pikseli)
        wave_offset = math.sin(self.angle) * 15

        # Ustawiamy pozycję X bazując na stałym offsecie i wyniku sinusa
        self.rect.x = -100 + wave_offset
        self.rect.x = -100 + wave_offset
