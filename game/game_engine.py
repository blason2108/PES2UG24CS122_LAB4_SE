import pygame
from game.deck import Deck

REVEAL_MS = 1400  # how long both cards stay on screen after a guess


class GameEngine:
    def __init__(self, width, height):
        self.width = width
        self.height = height
        self.deck = Deck()

        self.current_card = self.deck.draw()
        self.next_card = None
        self.previous_card = None      # Task 4: card shown on the left during reveal
        self.revealing = False         # Task 4: True while both cards are shown
        self.reveal_start = 0

        self.score = 0
        self.streak = 0                # Task 2: consecutive correct guesses
        self.status_msg = "Will the next card be HIGHER or LOWER?"
        self.status_color = (220, 220, 220)

        btn_w, btn_h = 140, 48
        self.btn_higher = pygame.Rect(width // 2 - btn_w - 20, height - 90, btn_w, btn_h)
        self.btn_lower = pygame.Rect(width // 2 + 20, height - 90, btn_w, btn_h)

        self.font_title = pygame.font.SysFont(None, 40)
        self.font_medium = pygame.font.SysFont(None, 30)
        self.font_small = pygame.font.SysFont(None, 24)

    # Task 2: escalating points for streaks
    @staticmethod
    def multiplier_for(streak):
        if streak >= 5:
            return 3
        if streak >= 3:
            return 2
        return 1

    def evaluate_guess(self, guess):
        """Draws next card and evaluates prediction."""
        self.previous_card = self.current_card
        self.next_card = self.deck.draw()

        # FIX (Task 1): compare numeric ranks, not rank_str (strings compare
        # alphabetically, so "10" < "2" and "K" < "Q").
        cur = self.current_card.numeric_rank
        nxt = self.next_card.numeric_rank
        pair = f"{self.next_card.rank_str} vs {self.current_card.rank_str}"

        if nxt == cur:
            # Task 3: push / tie -> keep score and streak
            self.status_msg = "PUSH / TIE! Rank matched."
            self.status_color = (240, 210, 60)
        else:
            correct = nxt > cur if guess == "HIGHER" else nxt < cur
            if correct:
                self.streak += 1
                mult = self.multiplier_for(self.streak)
                self.score += mult
                bonus = f"  (x{mult} streak {self.streak})" if mult > 1 else ""
                self.status_msg = f"CORRECT! {pair}  +{mult}{bonus}"
                self.status_color = (80, 220, 80)
            else:
                self.streak = 0
                self.score = max(0, self.score - 1)
                self.status_msg = f"WRONG! {pair}  -1"
                self.status_color = (235, 75, 75)

        # Task 4: don't swap cards yet - show both first
        self.revealing = True
        self.reveal_start = pygame.time.get_ticks()

    def handle_event(self, event):
        if self.revealing:  # ignore clicks during the reveal pause
            return
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.btn_higher.collidepoint(event.pos):
                self.evaluate_guess("HIGHER")
            elif self.btn_lower.collidepoint(event.pos):
                self.evaluate_guess("LOWER")

    def update(self):
        # Task 4: after the pause, shift to the next round
        if self.revealing and pygame.time.get_ticks() - self.reveal_start >= REVEAL_MS:
            self.current_card = self.next_card
            self.revealing = False

    def render(self, screen):
        screen.fill((25, 80, 45))

        title_surf = self.font_title.render("High-Low Card Predictor", True, (245, 245, 245))
        screen.blit(title_surf, (self.width // 2 - title_surf.get_width() // 2, 25))

        score_surf = self.font_medium.render(f"Score: {self.score}", True, (255, 220, 80))
        screen.blit(score_surf, (30, 30))

        streak_surf = self.font_small.render(
            f"Streak: {self.streak}  (x{self.multiplier_for(self.streak)})", True, (255, 200, 120))
        screen.blit(streak_surf, (30, 62))

        rem_surf = self.font_small.render(f"Deck: {self.deck.remaining} left", True, (210, 210, 210))
        screen.blit(rem_surf, (self.width - rem_surf.get_width() - 30, 35))

        card_w, card_h = 130, 180
        if self.revealing:
            # Task 4: previous card on the left, newly revealed card on the right
            gap = 30
            left_x = self.width // 2 - card_w - gap // 2
            right_x = self.width // 2 + gap // 2
            self.previous_card.render(screen, left_x, 100, card_w, card_h)
            self.next_card.render(screen, right_x, 100, card_w, card_h)
            lbl_prev = self.font_small.render("Previous", True, (210, 210, 210))
            lbl_new = self.font_small.render("New", True, (255, 255, 255))
            screen.blit(lbl_prev, (left_x + card_w // 2 - lbl_prev.get_width() // 2, 80))
            screen.blit(lbl_new, (right_x + card_w // 2 - lbl_new.get_width() // 2, 80))
        else:
            self.current_card.render(screen, self.width // 2 - card_w // 2, 100, card_w, card_h)

        status_surf = self.font_small.render(self.status_msg, True, self.status_color)
        screen.blit(status_surf, (self.width // 2 - status_surf.get_width() // 2, 310))

        dim = self.revealing  # grey out buttons during the pause
        pygame.draw.rect(screen, (90, 110, 95) if dim else (40, 140, 60), self.btn_higher, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), self.btn_higher, width=2, border_radius=8)
        high_surf = self.font_medium.render("HIGHER", True, (255, 255, 255))
        screen.blit(
            high_surf,
            (self.btn_higher.centerx - high_surf.get_width() // 2, self.btn_higher.centery - high_surf.get_height() // 2),
        )

        pygame.draw.rect(screen, (110, 90, 90) if dim else (170, 50, 50), self.btn_lower, border_radius=8)
        pygame.draw.rect(screen, (220, 220, 220), self.btn_lower, width=2, border_radius=8)
        low_surf = self.font_medium.render("LOWER", True, (255, 255, 255))
        screen.blit(
            low_surf,
            (self.btn_lower.centerx - low_surf.get_width() // 2, self.btn_lower.centery - low_surf.get_height() // 2),
        )
