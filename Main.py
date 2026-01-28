import pygame
import sys
import random
from Settings import *
from Player import Player
from World_objects import Platform, Lava
from LeaderBoard import LeaderBoard
from PlayerManager import PlayerManager

class Game:
    def __init__(self):
        pygame.init()
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        pygame.display.set_caption(TITLE)
        self.clock = pygame.time.Clock()
        self.running = True
        self.font = pygame.font.SysFont("Arial", 20)
        self.font_large = pygame.font.SysFont("Arial", 36, bold=True)

        # Inicjalizacja LeaderBoard i PlayerManager
        self.leaderboard = LeaderBoard("leaderboard.json")
        self.player_manager = PlayerManager()
        self.current_player = None

        try:
            bg_img = pygame.image.load(BG_IMAGE_PATH).convert()
            self.background = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
        except:
            print("Brak tła, używam koloru.")
            self.background = None

        self.show_main_menu()

    def show_main_menu(self):
        """Główne menu gry"""
        self.current_player = self.player_manager.get_nickname_input(
            self.screen, SCREEN_WIDTH, SCREEN_HEIGHT
        )
        if self.current_player is None:
            self.running = False
            return
        self.new_game()

    def new_game(self):
        """Inicjalizuje nową grę"""
        self.difficulty = 1.0  # Startowy mnożnik trudności
        self.score = 0
        
        # Grupy spritów
        self.all_sprites = pygame.sprite.Group()
        self.platforms = pygame.sprite.Group()
        self.danger_zone = pygame.sprite.Group()

        # Tworzenie obiektów
        self.player = Player(self)
        self.all_sprites.add(self.player)

        # Lawa (teraz przekazujemy self)
        self.lava = Lava(self)
        self.danger_zone.add(self.lava)
        self.all_sprites.add(self.lava)

        # Platforma startowa
        p1 = Platform(self, SCREEN_WIDTH / 2 - 50, SCREEN_HEIGHT - 60)
        self.all_sprites.add(p1)
        self.platforms.add(p1)

    def check_ground(self):
        """Sprawdza czy gracz stoi na ziemi"""
        if self.player.vel.y >= 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                lowest = hits[0]
                if self.player.pos.y < lowest.rect.bottom:
                    self.player.pos.y = lowest.rect.top + 1
                    self.player.vel.y = 0
                    self.player.last_ground_time = pygame.time.get_ticks()
                    return True
        return False

    def run(self):
        """Główna pętla gry"""
        while self.running:
            self.clock.tick(FPS)
            self.events()
            self.update()
            self.draw()

    def events(self):
        """Obsługa zdarzeń"""
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                self.running = False
            if event.type == pygame.KEYDOWN:
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.player.jump()
            if event.type == pygame.KEYUP:
                if event.key in [pygame.K_SPACE, pygame.K_w, pygame.K_UP]:
                    self.player.jump_cut()

    def update(self):
        """Aktualizacja gry"""
        # Zwiększanie trudności z każdą klatką
        self.difficulty += DIFFICULTY_INCREMENT
        
        self.all_sprites.update()

        # 1. KOLIZJE Z PLATFORMAMI
        if self.player.vel.y > 0:
            hits = pygame.sprite.spritecollide(self.player, self.platforms, False)
            if hits:
                if self.player.pos.y < hits[0].rect.bottom:
                    self.player.pos.y = hits[0].rect.top
                    self.player.vel.y = 0

        # 3. KAMERA (PRZESUWANIE EKRANU W GÓRĘ)
        scroll_threshold = SCREEN_HEIGHT / 2
        if self.player.rect.top <= scroll_threshold:
            self.player.pos.y += abs(self.player.vel.y)

            for plat in self.platforms:
                plat.rect.y += abs(self.player.vel.y)
                if plat.rect.top >= SCREEN_HEIGHT:
                    plat.kill()

            self.lava.rect.y += abs(self.player.vel.y)
            self.score += int(abs(self.player.vel.y))

        # 4. GENEROWANIE NOWYCH PLATFORM
        while len(self.platforms) < MAX_PLATFORMS:
            highest_plat = min(self.platforms, key=lambda p: p.rect.top)
            y = highest_plat.rect.top - random.randint(*PLATFORM_GAP_Y)
            x = random.randrange(0, SCREEN_WIDTH - 100)

            p = Platform(self, x, y) # Przekazujemy self (grę)
            self.platforms.add(p)
            self.all_sprites.add(p)

        # 5. ŚMIERĆ (DOTKNIĘCIE LAWY LUB SPADNIĘCIE)
        death_by_lava = pygame.sprite.spritecollide(self.player, self.danger_zone, False)
        fell_off = self.player.rect.top > SCREEN_HEIGHT + 200

        if death_by_lava or fell_off:
            self.handle_game_over()

    def handle_game_over(self):
        """Obsługuje koniec gry"""
        self.leaderboard.add_score(self.current_player, self.score)
        if self.leaderboard.is_first_place(self.current_player, self.score):
            self.player_manager.display_first_place_message(self.screen, SCREEN_WIDTH, SCREEN_HEIGHT)

        action = self.player_manager.display_game_over_menu(
            self.screen, SCREEN_WIDTH, SCREEN_HEIGHT,
            self.current_player, self.score
        )

        if action == "restart":
            self.new_game()
        elif action == "change_player":
            self.show_main_menu()
        elif action == "quit":
            self.running = False

    def draw(self):
        """Rysowanie gry"""
        if self.background:
            self.screen.blit(self.background, (0, 0))
        else:
            self.screen.fill(SKY_BLUE)

        self.all_sprites.draw(self.screen)

        # Rysowanie wyniku bieżącego i poziomu trudności
        score_text = f"Wysokość: {self.score} | Trudność: {round(self.difficulty, 2)}"
        score_surf = self.font.render(score_text, True, BLACK)
        self.screen.blit(score_surf, (10, 10))

        # Rysowanie nicku gracza
        player_surf = self.font.render(f"Gracz: {self.current_player}", True, BLACK)
        self.screen.blit(player_surf, (10, 35))

        # COMBO COUNTER
        if self.player.jump_count > 1:
            combo_font = pygame.font.SysFont("Arial", 36, bold=True)
            combo_text = f"COMBO x{self.player.jump_count}!"
            combo_surf = combo_font.render(combo_text, True, RED)
            combo_x = SCREEN_WIDTH // 2 - combo_surf.get_width() // 2
            self.screen.blit(combo_surf, (combo_x, 100))

        pygame.display.flip()


if __name__ == "__main__":
    g = Game()
    g.run()
    pygame.quit()
    sys.exit()
