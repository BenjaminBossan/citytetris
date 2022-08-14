import string

import pygame

from citytetris.constants import FONT
from citytetris.colors import ColorShade, GrayShade, YellowShade

chars_allowed = set(string.digits) | set(string.ascii_lowercase)


# modified from https://stackoverflow.com/a/46390412
class InputDigitBox:
    def __init__(
        self, x: int, y: int, w: int, h: int, text: str = "", max_len: int = 6
    ) -> None:
        self.rect = pygame.Rect(x, y, w, h)
        self.text = text
        self.max_len = max_len

        self.active = False

    def get_color(self) -> ColorShade:
        color = YellowShade() if self.active else GrayShade()
        return color  # type: ignore

    def get_text_surface(self) -> pygame.surface.Surface:
        return FONT.render(self.text, True, self.get_color().light)

    def get_seed(self) -> int | str | None:
        if self.text:
            return self.text
        return None

    def handle_event(self, event: pygame.event.Event) -> None:
        if event.type == pygame.MOUSEBUTTONDOWN:
            # If the user clicked on the input_box rect.
            if self.rect.collidepoint(event.pos):
                # Toggle the active variable.
                self.active = True
            else:
                self.active = False
        if (event.type == pygame.KEYDOWN) and self.active:
            char = event.unicode.lower()
            if event.key == pygame.K_BACKSPACE:
                self.text = self.text[:-1]
            elif (char in chars_allowed) and len(self.text) < self.max_len:
                self.text += char

    def draw(self, screen: pygame.surface.Surface) -> None:
        text = self.get_text_surface()
        # print text into middle of input box
        screen.blit(
            text,
            (
                self.rect.x + self.rect.w / 2 - text.get_width() / 2,
                self.rect.y + self.rect.h / 2 - text.get_height() / 2,
            ),
        )
        pygame.draw.rect(screen, self.get_color().light, self.rect, 2)
