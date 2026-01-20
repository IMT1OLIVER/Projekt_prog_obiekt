import pygame
import os

# Konfiguracja
ASSETS_DIR = "grafika"
if not os.path.exists(ASSETS_DIR):
    os.makedirs(ASSETS_DIR)

pygame.init()


def save_surface(surface, name):
    path = os.path.join(ASSETS_DIR, name)
    pygame.image.save(surface, path)
    print(f"Zapisano: {path}")


# --- 1. POSTAĆ (Hero) ---
# Tworzymy prostego rycerza/robota w Pixel Arcie
def draw_hero():
    surf = pygame.Surface((32, 48), pygame.SRCALPHA)

    # Ciało
    pygame.draw.rect(surf, (60, 60, 200), (4, 14, 24, 24))  # Tułów
    pygame.draw.rect(surf, (40, 40, 150), (4, 14, 24, 24), 2)  # Obrys

    # Głowa
    pygame.draw.rect(surf, (220, 200, 180), (6, 0, 20, 16))  # Skóra/Hełm

    # Opaska / Oczy
    pygame.draw.rect(surf, (200, 50, 50), (6, 4, 20, 4))  # Czerwona opaska
    pygame.draw.rect(surf, (255, 255, 255), (20, 5, 4, 2))  # Błysk w oku

    # Nogi
    pygame.draw.rect(surf, (30, 30, 80), (8, 38, 6, 10))  # Lewa noga
    pygame.draw.rect(surf, (30, 30, 80), (18, 38, 6, 10))  # Prawa noga

    save_surface(surf, "hero.png")


# --- 2. PLATFORMA ---
def draw_platform():
    # Platforma kafelkowana, zrobimy jeden segment środkowy
    surf = pygame.Surface((64, 32), pygame.SRCALPHA)

    # Kamień (szary spód)
    pygame.draw.rect(surf, (100, 100, 100), (0, 8, 64, 24))

    # Tekstura kamienia (kropki)
    for i in range(0, 64, 10):
        pygame.draw.circle(surf, (80, 80, 80), (i + 5, 20), 3)

    # Trawa (zielona góra)
    pygame.draw.rect(surf, (50, 180, 50), (0, 0, 64, 8))
    # "Zwisająca" trawa
    for i in range(0, 64, 8):
        pygame.draw.rect(surf, (50, 180, 50), (i + 2, 8, 4, 3))

    save_surface(surf, "platform.png")


# --- 3. TŁO (Background) ---
def draw_background():
    width, height = 800, 600
    surf = pygame.Surface((width, height))

    # Gradient nieba
    for y in range(height):
        # Od ciemnego niebieskiego do jasnego
        r = max(0, 20 - y // 40)
        g = min(200, 20 + y // 4)
        b = min(255, 80 + y // 3)
        pygame.draw.line(surf, (r, g, b), (0, y), (width, y))

    # Dodajmy kilka chmur (proste elipsy)
    clouds = [(100, 100), (400, 200), (650, 80)]
    for cx, cy in clouds:
        pygame.draw.ellipse(surf, (255, 255, 255), (cx, cy, 120, 60))
        pygame.draw.ellipse(surf, (240, 240, 255), (cx + 20, cy + 10, 120, 60))

    save_surface(surf, "background.png")


# Uruchomienie generowania
draw_hero()
draw_platform()
draw_background()

print("Gotowe! Pliki zapisane w folderze 'grafika'.")
pygame.quit()