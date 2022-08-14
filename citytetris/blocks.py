import pygame
from typing import Iterator

from citytetris.constants import BS
from citytetris.colors import (
    ColorShade,
    OrangeShade,
    RedShade,
    GreenShade,
    BlueShade,
    YellowShade,
    CyanShade,
    PurpleShade,
)

Coord = tuple[int, int]
Coord4Cells = tuple[Coord, Coord, Coord, Coord]
Variants = tuple[Coord4Cells, Coord4Cells, Coord4Cells, Coord4Cells]


class Block:
    def __init__(self) -> None:
        self.x: int = 0
        self.y: int = 0
        self.rotation: int = 0
        self.block_variants: Variants = (
            ((0, 0), (0, 1), (0, 2), (0, 3)),
            ((0, 0), (1, 0), (2, 0), (3, 0)),
            ((0, 0), (0, 1), (0, 2), (0, 3)),
            ((0, 0), (1, 0), (2, 0), (3, 0)),
        )
        self.shades: ColorShade = RedShade()
        self.symbol: str = "x"
        self.highlight: bool = False

    def __hash__(self) -> int:
        return hash((self.x, self.y, self.rotation))

    @property
    def squares(self) -> Coord4Cells:
        return self.block_variants[self.rotation]

    def get_rects(self) -> list[pygame.Rect]:
        return [
            pygame.Rect(
                self.x + square_x * BS,
                self.y + square_y * BS,
                BS,
                BS,
            )
            for square_x, square_y in self.squares
        ]

    def yield_indices(self) -> Iterator[Coord]:
        for x, y in self.squares:
            offset_x, offset_y = self.x // BS, self.y // BS
            yield x + offset_x, y + offset_y

    def rotate(self) -> None:
        self.rotation = (self.rotation + 1) % 4

    def move_left(self, n: int = 1) -> None:
        for _ in range(n):
            self.x -= BS

    def move_right(self, n: int = 1) -> None:
        for _ in range(n):
            self.x += BS

    def move_down(self, n: int = 1) -> None:
        for _ in range(n):
            self.y += BS

    def get_rightmost_x(self) -> int:
        return (1 + max(self.squares, key=lambda x: x[0])[0]) * BS + self.x

    def get_bottommost_y(self) -> int:
        return (1 + max(self.squares, key=lambda x: x[1])[1]) * BS + self.y

    def draw(self, screen: pygame.surface.Surface) -> None:
        for block_x, block_y in self.squares:
            rect = pygame.draw.rect(
                screen,
                self.shades.fill,
                (
                    self.x + block_x * BS,
                    self.y + block_y * BS,
                    BS,
                    BS,
                ),
            )
            if self.highlight:
                # draw a smaller rect into the center of the rect
                pygame.draw.rect(
                    screen,
                    self.shades.light,
                    (
                        self.x + block_x * BS + BS // 2,
                        self.y + block_y * BS + BS // 2,
                        BS // 2,
                        BS // 2,
                    ),
                )

            # draw block borders
            width = 3  # line width
            pygame.draw.line(
                screen,
                self.shades.light,
                (self.x + block_x * BS, self.y + block_y * BS),
                (self.x + (1 + block_x) * BS, self.y + block_y * BS),
                width=width,
            )
            pygame.draw.line(
                screen,
                self.shades.light,
                (self.x + block_x * BS, self.y + block_y * BS),
                (self.x + block_x * BS, self.y + (1 + block_y) * BS),
                width=width,
            )
            pygame.draw.line(
                screen,
                self.shades.dark,
                (self.x + (1 + block_x) * BS, self.y + block_y * BS),
                (self.x + (1 + block_x) * BS, self.y + (1 + block_y) * BS),
                width=width,
            )
            pygame.draw.line(
                screen,
                self.shades.dark,
                (self.x + block_x * BS, self.y + (1 + block_y) * BS),
                (self.x + (1 + block_x) * BS, self.y + (1 + block_y) * BS),
                width=width,
            )

    def collides_bottom(self, rect_list: list[pygame.Rect]) -> bool:
        rects = self.get_rects()
        # move all rects down by 1 block
        for rect in rects:
            rect.y += BS
            if rect.collidelist(rect_list) != -1:
                return True
        return False

    def collides_left(self, rect_list: list[pygame.Rect]) -> bool:
        rects = self.get_rects()
        # move all rects left by 1 block
        for rect in rects:
            rect.x -= BS
            if rect.collidelist(rect_list) != -1:
                return True
        return False

    def collides_right(self, rect_list: list[pygame.Rect]) -> bool:
        rects = self.get_rects()
        # move all rects right by 1 block
        for rect in rects:
            rect.x += BS
            if rect.collidelist(rect_list) != -1:
                return True
        return False

    def collides(self, rect_list: list[pygame.Rect]) -> bool:
        return (
            self.collides_bottom(rect_list)
            or self.collides_left(rect_list)
            or self.collides_right(rect_list)
        )

    def __repr__(self) -> str:
        indices = tuple(self.yield_indices())
        name = self.__class__.__name__
        return f"{name}{indices}".replace(" ", "")


class IBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = GreenShade()
        self.symbol = "I"
        self.block_variants = (
            ((0, 0), (1, 0), (2, 0), (3, 0)),
            ((0, 0), (0, 1), (0, 2), (0, 3)),
            ((0, 0), (1, 0), (2, 0), (3, 0)),
            ((0, 0), (0, 1), (0, 2), (0, 3)),
        )


class LBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = BlueShade()
        self.symbol = "L"
        self.block_variants = (
            ((0, 0), (1, 0), (2, 0), (0, 1)),
            ((0, 0), (1, 0), (1, 1), (1, 2)),
            ((0, 1), (1, 1), (2, 1), (2, 0)),
            ((0, 0), (0, 1), (0, 2), (1, 2)),
        )


class JBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = CyanShade()
        self.symbol = "J"
        self.block_variants = (
            ((0, 0), (1, 0), (2, 0), (2, 1)),
            ((1, 0), (1, 1), (1, 2), (0, 2)),
            ((0, 0), (0, 1), (1, 1), (2, 1)),
            ((0, 0), (1, 0), (0, 1), (0, 2)),
        )


class OBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = OrangeShade()
        self.symbol = "O"
        self.block_variants = (
            ((0, 0), (0, 1), (1, 0), (1, 1)),
            ((0, 0), (0, 1), (1, 0), (1, 1)),
            ((0, 0), (0, 1), (1, 0), (1, 1)),
            ((0, 0), (0, 1), (1, 0), (1, 1)),
        )


class SBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = RedShade()
        self.symbol = "S"
        self.block_variants = (
            ((0, 1), (1, 1), (1, 0), (2, 0)),
            ((0, 0), (0, 1), (1, 1), (1, 2)),
            ((0, 1), (1, 1), (1, 0), (2, 0)),
            ((0, 0), (0, 1), (1, 1), (1, 2)),
        )


class ZBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = PurpleShade()
        self.symbol = "Z"
        self.block_variants = (
            ((0, 0), (1, 0), (1, 1), (2, 1)),
            ((1, 0), (1, 1), (0, 1), (0, 2)),
            ((0, 0), (1, 0), (1, 1), (2, 1)),
            ((1, 0), (1, 1), (0, 1), (0, 2)),
        )


class TBlock(Block):
    def __init__(self) -> None:
        super().__init__()
        self.shades = YellowShade()
        self.symbol = "T"
        self.block_variants = (
            ((0, 0), (1, 0), (2, 0), (1, 1)),
            ((0, 1), (1, 1), (1, 0), (1, 2)),
            ((0, 1), (1, 1), (2, 1), (1, 0)),
            ((0, 0), (0, 1), (0, 2), (1, 1)),
        )


BLOCKS_ALL = [
    IBlock,
    LBlock,
    JBlock,
    OBlock,
    SBlock,
    ZBlock,
    TBlock,
]
