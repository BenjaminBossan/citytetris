import datetime as dt

import pygame

from citytetris.colors import ColorShade, GrayShade
from citytetris.constants import (
    BOX_BORDER_X,
    BOX_BORDER_Y,
    FONT,
    SCREEN_WIDTH,
)
from citytetris.gui import InputDigitBox
from citytetris.replay import get_high_scores, load_tetris_last


def _draw_border(
    screen: pygame.surface.Surface,
    button: pygame.rect.Rect,
    color: ColorShade,
    width: int = 3,
) -> None:
    pygame.draw.line(
        screen,
        color.light,
        (button.x, button.y),
        (button.x + button.width, button.y),
        width=width,
    )
    pygame.draw.line(
        screen,
        color.light,
        (button.x, button.y),
        (button.x, button.y + button.height),
        width=width,
    )
    pygame.draw.line(
        screen,
        color.fill,
        (button.x + button.width, button.y),
        (button.x + button.width, button.y + button.height),
        width=width,
    )
    pygame.draw.line(
        screen,
        color.fill,
        (button.x, button.y + button.height),
        (button.x + button.width, button.y + button.height),
        width=width,
    )


class StartScreen:
    def __init__(self) -> None:
        self.color = GrayShade()

        distance_y = 50
        # title on left half of the screen
        y_offset = distance_y
        self.title_text = FONT.render("C I T Y  T E T R I S", True, self.color.fill)
        self.title_box = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.title_text.get_width() // 2),
            y_offset,
            self.title_text.get_width() + BOX_BORDER_X,
            self.title_text.get_height() + BOX_BORDER_Y,
        )

        # start button on left half of the screen
        y_offset = self.title_box.y + self.title_box.height + distance_y
        self.start_text = FONT.render("START", True, self.color.fill)
        self.start_button = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.start_text.get_width() // 2),
            y_offset,
            self.start_text.get_width() + BOX_BORDER_X,
            self.start_text.get_height() + BOX_BORDER_Y,
        )

        # digit input box for random seed
        y_offset = self.start_button.y + self.start_button.height + distance_y
        self.seed_text = FONT.render("RANDOM SEED", True, self.color.fill)
        self.seed_box = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.seed_text.get_width() // 2),
            y_offset,
            self.seed_text.get_width() + BOX_BORDER_X,
            self.seed_text.get_height() + BOX_BORDER_Y,
        )
        y_offset = self.seed_box.y + self.seed_box.height + 10
        self.seed_input_box = InputDigitBox(
            (SCREEN_WIDTH // 4) - (self.seed_text.get_width() // 2),
            y_offset,
            self.seed_text.get_width() + BOX_BORDER_X,
            self.seed_text.get_height() + BOX_BORDER_Y,
        )

        # highscore button on left half of the screen
        y_offset = (
            self.seed_input_box.rect.y + self.seed_input_box.rect.height + distance_y
        )
        self.highscore_text = FONT.render("HIGHSCORE", True, self.color.fill)
        self.highscore_button = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.highscore_text.get_width() // 2),
            y_offset,
            self.highscore_text.get_width() + BOX_BORDER_X,
            self.highscore_text.get_height() + BOX_BORDER_Y,
        )

        # quit button on left half of the screen
        y_offset = self.highscore_button.y + self.highscore_button.height + distance_y
        self.quit_text = FONT.render("QUIT", True, self.color.fill)
        self.quit_button = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.quit_text.get_width() // 2),
            y_offset,
            self.quit_text.get_width() + BOX_BORDER_X,
            self.quit_text.get_height() + BOX_BORDER_Y,
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        screen.fill(self.color.dark)
        self.draw_title(screen)
        self.draw_start(screen)
        self.draw_seed_input(screen)
        self.draw_highscore(screen)
        self.draw_quit(screen)

    def draw_title(self, screen: pygame.surface.Surface) -> None:
        # draw title
        screen.blit(
            self.title_text,
            (
                self.title_box.x + BOX_BORDER_X // 2,
                self.title_box.y + BOX_BORDER_Y // 2,
            ),
        )

    def draw_start(self, screen: pygame.surface.Surface) -> None:
        # draw start button border
        _draw_border(screen, self.start_button, self.color)

        # draw start button text
        screen.blit(
            self.start_text,
            (
                self.start_button.x
                + (self.start_button.width - self.start_text.get_width()) / 2,
                self.start_button.y
                + (self.start_button.height - self.start_text.get_height()) / 2,
            ),
        )

    def draw_seed_input(self, screen: pygame.surface.Surface) -> None:
        # draw seed input box border
        _draw_border(screen, self.seed_input_box.rect, self.color)
        screen.blit(
            self.seed_text,
            (
                self.seed_box.x + BOX_BORDER_X // 2,
                self.seed_box.y + BOX_BORDER_Y // 2,
            ),
        )
        # draw seed input box input
        _draw_border(
            screen,
            self.seed_input_box.rect,
            self.seed_input_box.get_color(),
        )
        self.seed_input_box.draw(screen)

    def draw_highscore(self, screen: pygame.surface.Surface) -> None:
        # draw highscore button border
        _draw_border(screen, self.highscore_button, self.color)

        # draw highscore button text
        screen.blit(
            self.highscore_text,
            (
                self.highscore_button.x
                + (self.highscore_button.width - self.highscore_text.get_width()) / 2,
                self.highscore_button.y
                + (self.highscore_button.height - self.highscore_text.get_height()) / 2,
            ),
        )

    def draw_quit(self, screen: pygame.surface.Surface) -> None:
        # draw quit button border
        _draw_border(screen, self.quit_button, self.color)

        # draw quit button text
        screen.blit(
            self.quit_text,
            (
                self.quit_button.x
                + (self.quit_button.width - self.quit_text.get_width()) / 2,
                self.quit_button.y
                + (self.quit_button.height - self.quit_text.get_height()) / 2,
            ),
        )


class PauseScreen:
    def __init__(self) -> None:
        self.color = GrayShade()

        distance_y = 50
        # pause text
        y_offset = distance_y
        self.pause_text = FONT.render("P A U S E", True, self.color.fill)
        self.pause_box = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.pause_text.get_width() // 2),
            y_offset,
            self.pause_text.get_width() + BOX_BORDER_X,
            self.pause_text.get_height() + BOX_BORDER_Y,
        )

        # resume button on left half of the screen
        y_offset = self.pause_box.y + self.pause_box.height + distance_y
        self.resume_text = FONT.render("RESUME", True, self.color.fill)
        self.resume_button = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.resume_text.get_width() // 2),
            y_offset,
            self.resume_text.get_width() + BOX_BORDER_X,
            self.resume_text.get_height() + BOX_BORDER_Y,
        )

        # home button on left half of the screen
        y_offset = self.resume_button.y + self.resume_button.height + distance_y
        self.home_text = FONT.render("HOME", True, self.color.fill)
        self.home_button = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.home_text.get_width() // 2),
            y_offset,
            self.home_text.get_width() + BOX_BORDER_X,
            self.home_text.get_height() + BOX_BORDER_Y,
        )

        # quit button on left half of the screen
        y_offset = self.home_button.y + self.home_button.height + distance_y
        self.quit_text = FONT.render("QUIT", True, self.color.fill)
        self.quit_button = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.quit_text.get_width() // 2),
            y_offset,
            self.quit_text.get_width() + BOX_BORDER_X,
            self.quit_text.get_height() + BOX_BORDER_Y,
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        # put transparent layer above the screen
        black_transparent = pygame.Color(0, 0, 0, 150)
        layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        layer.fill(black_transparent)
        screen.blit(layer, (0, 0))

        self.draw_pause(screen)
        self.draw_resume(screen)
        self.draw_home(screen)
        self.draw_quit(screen)

    def draw_pause(self, screen: pygame.surface.Surface) -> None:
        # draw pause text
        screen.blit(
            self.pause_text,
            (
                self.pause_box.x + BOX_BORDER_X // 2,
                self.pause_box.y + BOX_BORDER_Y // 2,
            ),
        )

    def draw_resume(self, screen: pygame.surface.Surface) -> None:
        # draw resume button border
        _draw_border(screen, self.resume_button, self.color)

        # draw resume button text
        screen.blit(
            self.resume_text,
            (
                self.resume_button.x
                + (self.resume_button.width - self.resume_text.get_width()) / 2,
                self.resume_button.y
                + (self.resume_button.height - self.resume_text.get_height()) / 2,
            ),
        )

    def draw_home(self, screen: pygame.surface.Surface) -> None:
        # draw home button border
        _draw_border(screen, self.home_button, self.color)

        # draw home button text
        screen.blit(
            self.home_text,
            (
                self.home_button.x
                + (self.home_button.width - self.home_text.get_width()) / 2,
                self.home_button.y
                + (self.home_button.height - self.home_text.get_height()) / 2,
            ),
        )

    def draw_quit(self, screen: pygame.surface.Surface) -> None:
        # draw quit button border
        _draw_border(screen, self.quit_button, self.color)

        # draw quit button text
        screen.blit(
            self.quit_text,
            (
                self.quit_button.x
                + (self.quit_button.width - self.quit_text.get_width()) / 2,
                self.quit_button.y
                + (self.quit_button.height - self.quit_text.get_height()) / 2,
            ),
        )


class GameOverScreen:
    def __init__(self) -> None:
        self.color = GrayShade()

        distance_y = 50
        # game over text
        y_offset = distance_y
        self.game_over_text = FONT.render("G A M E  O V E R", True, self.color.fill)
        self.game_over_box = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.game_over_text.get_width() // 2),
            y_offset,
            self.game_over_text.get_width() + BOX_BORDER_X,
            self.game_over_text.get_height() + BOX_BORDER_Y,
        )

        # press any button to continue
        y_offset = self.game_over_box.y + self.game_over_box.height + distance_y
        self.press_any_key_text = FONT.render(
            "PRESS ANY KEY TO CONTINUE", True, self.color.fill
        )
        self.press_any_key_box = pygame.Rect(
            (SCREEN_WIDTH // 4) - (self.press_any_key_text.get_width() // 2),
            y_offset,
            self.press_any_key_text.get_width() + BOX_BORDER_X,
            self.press_any_key_text.get_height() + BOX_BORDER_Y,
        )

    def draw(self, screen: pygame.surface.Surface) -> None:
        # put transparent layer above the screen
        black_transparent = pygame.Color(0, 0, 0, 150)
        layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        layer.fill(black_transparent)
        screen.blit(layer, (0, 0))

        self.draw_game(screen)
        self.draw_press_any_button(screen)

    def draw_game(self, screen: pygame.surface.Surface) -> None:
        # draw game over text
        screen.blit(
            self.game_over_text,
            (
                self.game_over_box.x + BOX_BORDER_X // 2,
                self.game_over_box.y + BOX_BORDER_Y // 2,
            ),
        )

    def draw_press_any_button(self, screen: pygame.surface.Surface) -> None:
        # draw press any button text
        screen.blit(
            self.press_any_key_text,
            (
                self.press_any_key_box.x + BOX_BORDER_X // 2,
                self.press_any_key_box.y + BOX_BORDER_Y // 2,
            ),
        )


class LastGameScreen:
    def __init__(self) -> None:
        self.color = GrayShade()
        self.tetris = load_tetris_last()

        if self.tetris is not None:
            total_score = self.tetris.calculate_score().get_total_score()
            self.score_text = FONT.render(
                f"Last game score: {total_score}", True, self.color.fill
            )
        else:
            self.score_text = FONT.render("", True, self.color.fill)

    def draw_score(self, screen: pygame.surface.Surface) -> None:
        # draw score text into the middle of the screen
        width_screen = screen.get_width()
        height_screen = screen.get_height()
        width_text = self.score_text.get_width()
        height_text = self.score_text.get_height()
        screen.blit(
            self.score_text,
            (
                3 * width_screen / 4 - width_text / 2,
                (height_screen - height_text) / 2,
            ),
        )

    def draw_last_game(self, screen: pygame.surface.Surface) -> None:
        if self.tetris is None:
            return

        self.tetris.screen = self.tetris._make_game_screen(screen)
        self.tetris.draw()

        black_transparent = pygame.Color(0, 0, 0, 150)
        layer = pygame.Surface(screen.get_size(), pygame.SRCALPHA)
        layer.fill(black_transparent)
        screen.blit(layer, (0, 0))

    def draw(self, screen: pygame.surface.Surface) -> None:
        self.draw_last_game(screen)
        self.draw_score(screen)


class HighscoreScreen:
    def __init__(self, topk: int = 10) -> None:
        self.color = GrayShade()
        self.topk = topk

    def draw(self, screen: pygame.surface.Surface) -> None:
        # put dark layer on top of screen
        layer = pygame.Surface(screen.get_size())
        layer.fill(self.color.dark)
        screen.blit(layer, (0, 0))

        high_scores = get_high_scores(topk=self.topk)
        y_offset = 50
        for i, (score, date) in enumerate(high_scores, start=1):
            text = FONT.render(
                f"{i}. {score} points  -  date: {date}", True, self.color.fill
            )
            screen.blit(text, (50, y_offset))
            y_offset += text.get_height() + 20

        text = FONT.render("PRESS ANY KEY TO CONTINUE", True, self.color.fill)
        screen.blit(text, (50, y_offset))
