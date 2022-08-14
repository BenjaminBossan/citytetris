import json
import logging
import os
import sys

import pygame

from citytetris.colors import DARKGRAY, GrayShade
from citytetris.constants import (
    BS,
    CLOCKTICK,
    FONT,
    PATH_REPLAYS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
    SCORES,
)
from citytetris.replay import make_replay
from citytetris.score import Score
from citytetris.screens import (
    GameOverScreen,
    HighscoreScreen,
    LastGameScreen,
    PauseScreen,
    StartScreen,
)
from citytetris.tetris import Tetris


logger = logging.getLogger()
handler = logging.StreamHandler(sys.stdout)
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)


class Game:
    def __init__(self, size: str = "normal", debug: bool = True) -> None:
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.size = size
        self.gray_shade = GrayShade()
        self.screen_last_game = LastGameScreen()

        if debug:
            handler.setLevel(logging.DEBUG)
            logger.setLevel(logging.DEBUG)

    def display_preview_text(self, screen: pygame.surface.Surface) -> None:
        text_surface = FONT.render("PREVIEW", True, self.gray_shade.fill)
        screen.blit(text_surface, (10, 10))

    def display_score(self, screen: pygame.surface.Surface, score: Score) -> None:
        x, y = 10, BS * 5
        texts = [
            f"Full rows: {score.full_rows} (x{SCORES.full_rows})",
            f"Longest road: {score.longest_road} (x{SCORES.longest_road})",
            (
                f"L-J communities: {score.l_j_communities} "
                f"(x{SCORES.l_j_communities})"
            ),
            f"Largest T community: {score.t_community} (x{SCORES.t_community})",
        ]

        for text in texts:
            text_surface = FONT.render(text, True, self.gray_shade.fill)
            screen.blit(text_surface, (x, y))
            y += text_surface.get_height() + 10

        total_score = score.get_total_score()
        text_surface = FONT.render(
            f"TOTAL SCORE: {total_score}", True, self.gray_shade.fill
        )
        screen.blit(text_surface, (x, y))

    def get_screen_left(self) -> pygame.surface.Surface:
        width, height = self.screen.get_size()
        screen_left = self.screen.subsurface((0, 0, width // 2, height))
        return screen_left

    def get_screen_right(self) -> pygame.surface.Surface:
        width, height = self.screen.get_size()
        screen_right = self.screen.subsurface(
            (
                width // 2,
                0,
                width // 2,
                height,
            )
        )
        return screen_right

    def run(self) -> None:
        pygame.init()
        pygame.display.set_caption("City Tetris")
        self.screen.fill(self.gray_shade.dark)
        screen_start = StartScreen()
        self.screen_last_game.draw(self.screen)

        while True:
            screen_start.draw(self.get_screen_left())
            pygame.display.update()
            for event in pygame.event.get():
                # if player clicks on start button, start the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if screen_start.start_button.collidepoint(event.pos):
                        self.run_tetris(seed=screen_start.seed_input_box.get_seed())

                # if player presses ESC
                if (event.type == pygame.QUIT) or (
                    event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE
                ):
                    pygame.quit()
                    sys.exit()

                # if player clicks on high score button, show high score
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if screen_start.highscore_button.collidepoint(event.pos):
                        self.draw_highscore_screen(self.screen)

                # if player clicks on quit button, quit the game
                if event.type == pygame.MOUSEBUTTONDOWN:
                    if screen_start.quit_button.collidepoint(event.pos):
                        pygame.quit()
                        sys.exit()

                screen_start.seed_input_box.handle_event(event)

            self.screen_last_game.draw(self.screen)

    def pause_screen_interaction(
        self,
        tetris: Tetris,
        event: pygame.event.Event,
        x_offset: int = 0,
        y_offset: int = 0,
    ) -> None:
        # if player exits, quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        pause_screen = PauseScreen()
        # unpause game when player presses ESC
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
            tetris.paused = False
            return

        # pause screen mouse click interactions
        if event.type == pygame.MOUSEBUTTONDOWN:
            # determine real position of player click relative to left screen
            x = event.pos[0] - x_offset
            y = event.pos[1] - y_offset

            # if player clicks on resume, resume game
            if pause_screen.resume_button.collidepoint((x, y)):
                tetris.paused = False
                return

            # if player clicks on home, return to start screen
            if pause_screen.home_button.collidepoint((x, y)):
                tetris.running = False
                return

            # quit game when player presses quit
            if pause_screen.quit_button.collidepoint((x, y)):
                pygame.quit()
                sys.exit()

    def draw_pause_screen(
        self,
        tetris: Tetris,
        screen: pygame.surface.Surface,
    ) -> None:
        pause_screen = PauseScreen()
        # draw pause screen on right half of screen
        pause_screen.draw(screen)
        pygame.display.update()
        while tetris.paused and tetris.running:
            for event in pygame.event.get():
                self.pause_screen_interaction(tetris, event, *screen.get_offset())

    def highscore_screen_interactions(self, event: pygame.event.Event) -> bool:
        # if player exits, quit game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # if player presses ESC, return to start screen
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE):
            return False

        # if player clicks or presses any key, return to start screen
        if event.type in (pygame.MOUSEBUTTONDOWN, pygame.KEYDOWN):
            return False

        return True

    def draw_highscore_screen(self, screen: pygame.surface.Surface) -> None:
        highscore_screen = HighscoreScreen()
        highscore_screen.draw(screen)
        pygame.display.update()
        while True:
            for event in pygame.event.get():
                stay = self.highscore_screen_interactions(event)
                if not stay:
                    return

    def save_replay(self, tetris: Tetris) -> None:
        replay = make_replay(tetris)
        path = os.path.join(PATH_REPLAYS, replay.get_filename())
        try:
            with open(path, 'w') as f:
                json.dump(replay.to_json(), f, indent=2)
        except OSError as e:
            logger.error(f"Error saving replay: {e}")

    def draw_game_over_screen(self, screen: pygame.surface.Surface) -> None:
        # draw transparent screen over right screen
        game_over_screen = GameOverScreen()
        game_over_screen.draw(screen)
        pygame.display.update()

        # wait a bit so that player does not accidentally quit
        pygame.time.wait(2000)
        while True:
            # press ESC to quit game
            for event in pygame.event.get():
                if event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
                    pygame.quit()
                    sys.exit()
                # press any other button to return to home screen
                if (event.type == pygame.MOUSEBUTTONDOWN) or (
                    event.type == pygame.KEYDOWN
                ):
                    return

    def run_tetris(self, seed: int | str | None = None) -> None:
        # fill screen black
        self.screen.fill(DARKGRAY)

        tetris = Tetris(screen=self.screen, size=self.size, seed=seed)
        clock = pygame.time.Clock()
        screen_left = self.get_screen_left()
        screen_right = self.get_screen_right()
        running, paused = True, False
        while running:
            screen_left.fill(self.gray_shade.dark)
            if not paused:
                clock.tick(CLOCKTICK)

            running, paused = tetris.update(CLOCKTICK)

            score = tetris.calculate_score()
            self.display_preview_text(screen_left)
            self.display_score(screen_left, score)

            pygame.display.update()
            if running and paused:
                self.draw_pause_screen(tetris, screen_right)
                if not tetris.running:
                    break

        if tetris.game_over:
            logger.debug(tetris.replay)
            self.save_replay(tetris)
            self.draw_game_over_screen(screen_right)
            # refresh screen of last game
            self.screen_last_game = LastGameScreen()

        self.screen.fill(self.gray_shade.dark)
        pygame.display.update()
        return


if __name__ == "__main__":
    game = Game(debug=True)
    game.run()
