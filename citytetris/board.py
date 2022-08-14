import random
from dataclasses import dataclass, field

import pygame

from citytetris.blocks import BLOCKS_ALL, Block
from citytetris.constants import BLOCKS_HEIGHT, BLOCKS_WIDTH
from citytetris.network import (
    get_largest_T_community,
    get_longest_I_block_distance,
    get_number_of_disconnected_L_J_graphs,
)
from citytetris.score import Score


def _rand_block() -> Block:
    return random.choice(BLOCKS_ALL)()


@dataclass
class Board:
    width: int = BLOCKS_WIDTH
    height: int = BLOCKS_HEIGHT
    block_list: list[Block] = field(default_factory=list)
    block_active: Block = field(default_factory=_rand_block)
    rect_list: list[pygame.Rect] = field(default_factory=list)
    centered: bool = True

    def __post_init__(self) -> None:
        if self.centered:
            self.block_active.move_right(self.width // 2 - 1)

    def add_block(self, block: Block) -> None:
        # the None check below is theoretically unnecessary, but for scripting/testing,
        # we set the active block to None in order to prevent the board from starting
        # with a random block
        if self.block_active is not None:
            self.block_list.append(block)
            self.rect_list.extend(block.get_rects())

    def spawn_block(self, block: Block) -> None:
        self.add_block(self.block_active)

        self.block_active = block
        if self.centered:
            # move block to the middle of the board
            self.block_active.move_right(self.width // 2 - 1)

    def remove_highlight_from_blocks(self) -> None:
        for block in self.block_list:
            block.highlight = False

    def add_highlight_to_blocks(self, blocks: set[Block]) -> None:
        for block in blocks:
            block.highlight = True

    def calculate_score(self) -> Score:
        self.remove_highlight_from_blocks()
        blocks_to_highlight = set()

        full_rows = self._calculate_full_rows()

        longest_road, blocks = self._calculate_longest_road()
        blocks_to_highlight.update(blocks)

        num_l_j_communities, blocks = self._calculate_L_J_communities()
        blocks_to_highlight.update(blocks)

        largest_T_community, blocks = self._calculate_largest_T_community()
        blocks_to_highlight.update(blocks)

        self.add_highlight_to_blocks(blocks_to_highlight)

        return Score(
            full_rows=full_rows,
            longest_road=longest_road,
            l_j_communities=num_l_j_communities,
            t_community=largest_T_community,
        )

    def _calculate_full_rows(self) -> int:
        # number of rows that are full of squares
        squares_per_row = [0 for _ in range(self.height)]
        for block in self.block_list:
            for _, y in block.yield_indices():
                squares_per_row[y] += 1
        full_rows = sum(num_squares == self.width for num_squares in squares_per_row)
        return full_rows

    def _calculate_longest_road(self) -> tuple[int, set[Block]]:
        return get_longest_I_block_distance(self.block_list)

    def _calculate_L_J_communities(self) -> tuple[int, set[Block]]:
        return get_number_of_disconnected_L_J_graphs(self.block_list)

    def _calculate_largest_T_community(self) -> tuple[int, set[Block]]:
        return get_largest_T_community(self.block_list)

    def __repr__(self) -> str:
        grid = [[" " for _ in range(self.width)] for _ in range(self.height)]
        for block in self.block_list:
            for x, y in block.yield_indices():
                grid[y][x] = block.symbol

        lines = ["#" * (2 * self.width + 1)]
        for row in grid:
            lines.append("#" + " ".join(row) + "#")
        lines.append("#" * (2 * self.width + 1))
        return "\n".join(lines)
