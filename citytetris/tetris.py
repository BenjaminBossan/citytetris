import logging
import random
import sys
from typing import Type

import pygame

from citytetris.board import Board
from citytetris.blocks import BLOCKS_ALL, Block
from citytetris.colors import GrayShade
from citytetris.constants import (
    BS,
    CLOCK_BLOCK_MOVE,
    CLOCKTICK,
    TIME_BEFORE_GAME_OVER,
    TIME_BEFORE_NEW_SPAWN,
    TIME_BETWEEN_BLOCKS,
)
from citytetris.score import Score


logger = logging.getLogger(__name__)


class Tetris:
    def __init__(
        self,
        screen: pygame.surface.Surface,
        size: str = "normal",
        seed: int | str | None = None,
    ) -> None:
        self.speed = "normal"
        self.size = size
        self.seed = seed

        random.seed(seed)
        if size == "small":
            self.board = Board(10, 10)
        else:
            self.board = Board()

        self.screen = self._make_game_screen(screen)
        self.screen_preview = self._make_preview_screen(screen)
        self.running: bool = True
        self.paused: bool = False
        self.game_over: bool = False
        self.time_since_last_block_move: int = 0
        self.clock_block_move: int = CLOCK_BLOCK_MOVE
        self.time_since_touching_bottom: int = 0
        self.gray_shade = GrayShade()

        self.block_queue: list[Block] = []
        self._fill_block_queue()
        self.replay: list[str] = []
        self.record(self.board.block_active.symbol, new_line=True)

    def _make_game_screen(
        self, screen: pygame.surface.Surface
    ) -> pygame.surface.Surface:
        screen_width = screen.get_width()
        screen_height = screen.get_height()
        board_width = self.board.width * BS
        board_height = self.board.height * BS
        x_offset = 3 * screen_width // 4 - board_width // 2
        y_offset = (screen_height - board_height) // 2
        return screen.subsurface((x_offset, y_offset, board_width, board_height))

    def _make_preview_screen(
        self, screen: pygame.surface.Surface
    ) -> pygame.surface.Surface:
        screen_width = BS * 4
        screen_height = BS * 4
        screen_prev = screen.subsurface((10, BS + 10, screen_width, screen_height))
        return screen_prev

    def record(self, move: str, new_line: bool = False) -> None:
        if new_line:
            self.replay.append("")
        self.replay[-1] += move

    def draw_grid(self) -> None:
        for x in range(0, self.board.width * BS, BS):
            pygame.draw.line(
                self.screen, self.gray_shade.fill, (x, 0), (x, self.board.height * BS)
            )
        for y in range(0, self.board.height * BS, BS):
            pygame.draw.line(
                self.screen, self.gray_shade.fill, (0, y), (self.board.width * BS, y)
            )

    def _fill_block_queue(self) -> None:
        if len(self.block_queue) > len(BLOCKS_ALL):
            return

        blocks = [block() for block in BLOCKS_ALL]
        random.shuffle(blocks)
        self.block_queue.extend(blocks)
        self._fill_block_queue()  # need 2nd call after __init__

    def get_random_block(self) -> Block:
        block = self.block_queue.pop(0)
        self._fill_block_queue()
        return block

    def spawn_block(self) -> None:
        block = self.get_random_block()
        self.board.spawn_block(block)
        self.record(block.symbol, new_line=True)
        self.time_since_last_block_move = 0
        # calculate score to highlight blocks
        self.board.calculate_score()

    def draw_blocks(self) -> None:
        self.board.block_active.draw(self.screen)
        for block in self.board.block_list:
            block.draw(self.screen)
        self.block_queue[0].draw(self.screen_preview)

    def player_input(self, block: Block, event: pygame.event.Event) -> None:
        # quitting the game
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

        # pause the game
        if not self.paused and (
            (event.type == pygame.KEYDOWN) and (event.key == pygame.K_ESCAPE)
        ):
            self.paused = True
            return

        # move block down
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_DOWN):
            self.clock_block_move = CLOCKTICK
            return
        if event.type == pygame.KEYUP:
            self.clock_block_move = CLOCK_BLOCK_MOVE
            return

        # move left
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_LEFT):
            # check left board border
            if (block.x > 0) and not block.collides_left(self.board.rect_list):
                block.move_left()
                self.record("l")
            return

        # move right
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_RIGHT):
            # check right board border
            if (
                block.get_rightmost_x() < self.board.width * BS
            ) and not block.collides_right(self.board.rect_list):
                block.move_right()
                self.record("r")
            return

        # rotate block
        if (event.type == pygame.KEYDOWN) and (event.key == pygame.K_SPACE):
            if not (
                block.collides_left(self.board.rect_list)
                or block.collides_right(self.board.rect_list)
                or block.collides_bottom(self.board.rect_list)
            ):
                block.rotate()
                self.record("R")

                # check if block is outside of the board
                right_outside = block.get_rightmost_x() - (self.board.width * BS)
                if right_outside > 0:
                    block.x -= right_outside
                bottom_outside = block.get_bottommost_y() - (self.board.height * BS)
                if bottom_outside > 0:
                    block.y -= bottom_outside
            return

    def touches_ceiling(self, block: Block) -> bool:
        return block.y == 0

    def block_progress(self, block: Block) -> None:
        # if block hits the bottom of the board, spawn a new block
        hits_bottom = block.get_bottommost_y() >= (self.board.height * BS)
        hits_block = block.collides_bottom(self.board.rect_list)
        if hits_bottom or hits_block:
            if self.touches_ceiling(block):
                # game over
                self.game_over = True
                pygame.time.wait(TIME_BEFORE_GAME_OVER)
                self.board.calculate_score()
                self.running = False
            else:
                # give the player a bit of time to move the block, then fix block and spawn a new one
                self.time_since_touching_bottom += CLOCKTICK
                if self.time_since_touching_bottom > TIME_BEFORE_NEW_SPAWN:
                    self.time_since_touching_bottom = 0
                    pygame.time.wait(TIME_BETWEEN_BLOCKS)
                    self.spawn_block()
                    logger.debug("\n" + repr(self.board))
        else:
            # move block down
            if self.time_since_last_block_move > self.clock_block_move:
                block.move_down()
                self.record("d")
                self.time_since_last_block_move = 0

    def calculate_score(self) -> Score:
        return self.board.calculate_score()

    def draw(self) -> None:
        self.screen.fill(self.gray_shade.dark)
        self.draw_grid()
        self.draw_blocks()

    def update(self, tick: int) -> tuple[bool, bool]:
        block = self.board.block_active
        if not self.paused:
            self.time_since_last_block_move += tick

        # player input
        for event in pygame.event.get():
            self.player_input(block, event)

        # move block down, spawn new if hits bottom, end game if hits top
        if not self.paused:
            self.block_progress(block)

        self.draw()
        return self.running, self.paused
