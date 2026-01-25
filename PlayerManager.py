import pygame


class PlayerManager:
    def __init__(self):
        self.current_player = None
        self.font_large = pygame.font.SysFont("Arial", 32, bold=True)
        self.font_medium = pygame.font.SysFont("Arial", 24)
        self.font_small = pygame.font.SysFont("Arial", 18)

    def get_nickname_input(self, screen, screen_width, screen_height):
        """Wyświetla ekran do wprowadzenia nicku gracza"""
        nickname = ""
        input_active = True
        clock = pygame.time.Clock()

        while input_active:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return None
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        if len(nickname) > 0:
                            input_active = False
                    elif event.key == pygame.K_BACKSPACE:
                        nickname = nickname[:-1]
                    else:
                        if event.unicode.isprintable() and len(nickname) < 20:
                            nickname += event.unicode

            # Rysowanie ekranu
            screen.fill((135, 206, 235))  # SKY_BLUE

            title_surf = self.font_large.render("INFINITE JUMPER", True, (255, 255, 255))
            screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 100))

            prompt_surf = self.font_medium.render("Wprowadź swój nick:", True, (255, 255, 255))
            screen.blit(prompt_surf, (screen_width // 2 - prompt_surf.get_width() // 2, 250))

            # Pole wprowadzania
            input_rect = pygame.Rect(screen_width // 2 - 150, 320, 300, 50)
            pygame.draw.rect(screen, (255, 255, 255), input_rect)
            pygame.draw.rect(screen, (0, 0, 0), input_rect, 2)

            nickname_surf = self.font_medium.render(nickname, True, (0, 0, 0))
            screen.blit(nickname_surf, (input_rect.x + 10, input_rect.y + 10))

            hint_surf = self.font_small.render("Naciśnij ENTER aby potwierdzić", True, (255, 255, 255))
            screen.blit(hint_surf, (screen_width // 2 - hint_surf.get_width() // 2, 400))

            pygame.display.flip()

        return nickname

    def display_game_over_menu(self, screen, screen_width, screen_height, current_player, score):
        """Wyświetla menu po zakonczeniu gry"""
        menu_active = True
        clock = pygame.time.Clock()

        while menu_active:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return "quit"
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        return "restart"
                    elif event.key == pygame.K_c:
                        return "change_player"
                    elif event.key == pygame.K_ESCAPE:
                        return "quit"

            # Rysowanie menu
            screen.fill((135, 206, 235))

            game_over_surf = self.font_large.render("GAME OVER!", True, (220, 50, 50))
            screen.blit(game_over_surf, (screen_width // 2 - game_over_surf.get_width() // 2, 80))

            player_surf = self.font_medium.render(f"Gracz: {current_player}", True, (255, 255, 255))
            screen.blit(player_surf, (screen_width // 2 - player_surf.get_width() // 2, 180))

            score_surf = self.font_medium.render(f"Wynik: {score}", True, (255, 255, 255))
            screen.blit(score_surf, (screen_width // 2 - score_surf.get_width() // 2, 240))

            restart_surf = self.font_small.render("SPACE - Graj dalej", True, (50, 200, 50))
            screen.blit(restart_surf, (screen_width // 2 - restart_surf.get_width() // 2, 320))

            change_surf = self.font_small.render("C - Zmień gracza", True, (50, 200, 50))
            screen.blit(change_surf, (screen_width // 2 - change_surf.get_width() // 2, 370))

            quit_surf = self.font_small.render("ESC - Wyjdź", True, (220, 50, 50))
            screen.blit(quit_surf, (screen_width // 2 - quit_surf.get_width() // 2, 420))

            pygame.display.flip()

    def display_first_place_message(self, screen, screen_width, screen_height):
        """Wyświetla komunikat gratulacyjny za 1 miejsce"""
        display_time = 0
        clock = pygame.time.Clock()

        while display_time < 3000:  # 3 sekundy
            clock.tick(60)
            display_time += clock.get_time()

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return False

            screen.fill((135, 206, 235))

            congrats_surf = self.font_large.render("🎉 GRATULACJE! 🎉", True, (255, 215, 0))
            screen.blit(congrats_surf, (screen_width // 2 - congrats_surf.get_width() // 2, 150))

            first_surf = self.font_medium.render("Zajmujesz 1 miejsce w rankingu!", True, (255, 255, 255))
            screen.blit(first_surf, (screen_width // 2 - first_surf.get_width() // 2, 250))

            awesome_surf = self.font_small.render("Fantastycznie!", True, (255, 215, 0))
            screen.blit(awesome_surf, (screen_width // 2 - awesome_surf.get_width() // 2, 350))

            pygame.display.flip()

        return True

    def display_leaderboard(self, screen, screen_width, screen_height, leaderboard):
        """Wyświetla tabelę rekordów"""
        menu_active = True
        clock = pygame.time.Clock()

        while menu_active:
            clock.tick(30)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    return
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_ESCAPE or event.key == pygame.K_SPACE:
                        return

            # Rysowanie tabeli
            screen.fill((135, 206, 235))

            title_surf = self.font_large.render("TOP 10 RANKING", True, (255, 215, 0))
            screen.blit(title_surf, (screen_width // 2 - title_surf.get_width() // 2, 20))

            top_10 = leaderboard.get_top_10()

            y_offset = 80
            for i, entry in enumerate(top_10, 1):
                medal = "🥇" if i == 1 else "🥈" if i == 2 else "🥉" if i == 3 else f"{i}."
                ranking_text = f"{medal} {entry['nickname']} - {entry['score']}"
                ranking_surf = self.font_medium.render(ranking_text, True, (255, 255, 255))
                screen.blit(ranking_surf, (50, y_offset))
                y_offset += 40

            hint_surf = self.font_small.render("Naciśnij ESC lub SPACE aby wrócić", True, (255, 255, 255))
            screen.blit(hint_surf, (screen_width // 2 - hint_surf.get_width() // 2, screen_height - 50))

            pygame.display.flip()