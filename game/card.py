import pygame


class Card:

    def __init__(self, rank_str, suit_str, numeric_rank):
        self.rank_str = rank_str
        self.suit_str = suit_str
        self.numeric_rank = numeric_rank

        self.symbol = {"Hearts": "♥", "Diamonds": "♦", "Clubs": "♣", "Spades": "♠"}.get(suit_str, "")
        self.is_red = suit_str in ("Hearts", "Diamonds")
        self.color = (220, 40, 40) if self.is_red else (30, 30, 30)

    # FIX (rendering): pygame's default font has no ♥ ♦ ♣ ♠ glyphs, so the suit
    # showed up as an empty box. Suits are now drawn as shapes, so they look
    # the same on every computer.
    def _draw_suit(self, surface, cx, cy, size):
        c, s = self.color, size
        if self.suit_str == "Hearts":
            r = s * 0.27
            pygame.draw.circle(surface, c, (int(cx - r), int(cy - s * 0.15)), int(r))
            pygame.draw.circle(surface, c, (int(cx + r), int(cy - s * 0.15)), int(r))
            pygame.draw.polygon(surface, c, [
                (cx - s * 0.52, cy - s * 0.05), (cx + s * 0.52, cy - s * 0.05), (cx, cy + s * 0.5)])
        elif self.suit_str == "Diamonds":
            pygame.draw.polygon(surface, c, [
                (cx, cy - s * 0.5), (cx + s * 0.38, cy), (cx, cy + s * 0.5), (cx - s * 0.38, cy)])
        elif self.suit_str == "Spades":
            r = s * 0.27
            pygame.draw.circle(surface, c, (int(cx - r), int(cy + s * 0.05)), int(r))
            pygame.draw.circle(surface, c, (int(cx + r), int(cy + s * 0.05)), int(r))
            pygame.draw.polygon(surface, c, [
                (cx - s * 0.52, cy + s * 0.0), (cx + s * 0.52, cy + s * 0.0), (cx, cy - s * 0.5)])
            pygame.draw.polygon(surface, c, [
                (cx, cy + s * 0.05), (cx - s * 0.15, cy + s * 0.5), (cx + s * 0.15, cy + s * 0.5)])
        elif self.suit_str == "Clubs":
            r = int(s * 0.23)
            pygame.draw.circle(surface, c, (int(cx), int(cy - s * 0.25)), r)
            pygame.draw.circle(surface, c, (int(cx - s * 0.25), int(cy + s * 0.08)), r)
            pygame.draw.circle(surface, c, (int(cx + s * 0.25), int(cy + s * 0.08)), r)
            pygame.draw.polygon(surface, c, [
                (cx, cy), (cx - s * 0.15, cy + s * 0.5), (cx + s * 0.15, cy + s * 0.5)])

    def render(self, surface, x, y, width=130, height=180):
        card_rect = pygame.Rect(x, y, width, height)
        pygame.draw.rect(surface, (255, 255, 255), card_rect, border_radius=10)
        pygame.draw.rect(surface, (50, 50, 50), card_rect, width=3, border_radius=10)

        font_rank = pygame.font.SysFont(None, 36)
        rank_surf = font_rank.render(self.rank_str, True, self.color)

        # top-left: rank + small suit
        surface.blit(rank_surf, (x + 10, y + 8))
        self._draw_suit(surface, x + 10 + rank_surf.get_width() // 2, y + 8 + rank_surf.get_height() + 12, 18)

        # big suit in the middle
        self._draw_suit(surface, x + width // 2, y + height // 2, 56)

        # bottom-right: rank + small suit
        bx = x + width - rank_surf.get_width() - 10
        by = y + height - rank_surf.get_height() - 8
        surface.blit(rank_surf, (bx, by))
        self._draw_suit(surface, bx + rank_surf.get_width() // 2, by - 12, 18)
