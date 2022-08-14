import datetime as dt
import json
import os
from dataclasses import asdict, dataclass, field
from pathlib import Path
from typing import Any, Callable, Type

import pygame

import citytetris
from citytetris.blocks import (
    Block,
    IBlock,
    JBlock,
    LBlock,
    OBlock,
    SBlock,
    TBlock,
    ZBlock,
)
from citytetris.board import Board
from citytetris.constants import (
    BLOCKS_WIDTH,
    BLOCKS_HEIGHT,
    BS,
    SCREEN_HEIGHT,
    SCREEN_WIDTH,
)
from citytetris.score import Score
from citytetris.tetris import Tetris

PATH_REPLAYS = dir_replays = Path(citytetris.__file__).parent.parent / 'replays'


@dataclass
class MetaInfo:
    date: str
    version: str = citytetris.__version__
    system: str = os.uname().version


@dataclass
class GameInfo:
    size: str = "normal"
    speed: str = "normal"
    seed: int | str | None = None


@dataclass
class Replay:
    meta_info: MetaInfo
    game_info: GameInfo
    score: Score | None = None
    moves: list[str] = field(default_factory=list)

    def add_move(self, move: str, new_line: bool = False) -> None:
        if new_line:
            self.moves.append("")
        self.moves[-1] += move

    def add_score(self, score: Score) -> None:
        self.score = score

    def to_json(self) -> dict[str, Any]:
        return {
            'meta_info': asdict(self.meta_info),
            'game_info': asdict(self.game_info),
            'score': asdict(self.score) if self.score else None,
            'moves': self.moves,
        }

    @classmethod
    def from_json(cls, data: dict[str, Any]) -> 'Replay':
        meta_info = MetaInfo(**data['meta_info'])
        game_info = GameInfo(**data['game_info'])
        score = Score(**data['score']) if data['score'] else None
        moves = data['moves']
        return cls(meta_info=meta_info, game_info=game_info, score=score, moves=moves)

    def get_filename(self) -> str:
        return f'citytetris_{self.meta_info.date}.json'


def make_replay(tetris: Tetris) -> Replay:
    moves = tetris.replay
    meta_info = MetaInfo(date=dt.datetime.now().isoformat())
    game_info = GameInfo(size=tetris.size, speed=tetris.speed, seed=tetris.seed)
    replay = Replay(
        meta_info=meta_info,
        game_info=game_info,
        moves=moves,
        score=tetris.calculate_score(),
    )
    return replay


def load_replay(filename: str | Path) -> Replay:
    with open(filename) as f:
        data = json.load(f)
    return Replay.from_json(data)


BLOCK_MAPPING: dict[str, Type[Block]] = {
    'I': IBlock,
    'J': JBlock,
    'L': LBlock,
    'O': OBlock,
    'S': SBlock,
    'T': TBlock,
    'Z': ZBlock,
}


def move_left(board: Board) -> None:
    assert board.block_active is not None
    board.block_active.move_left()


def move_right(board: Board) -> None:
    assert board.block_active is not None
    board.block_active.move_right()


def move_down(board: Board) -> None:
    assert board.block_active is not None
    board.block_active.move_down()


def rotate(board: Board) -> None:
    assert board.block_active is not None
    board.block_active.rotate()


def move_to_bottom(board: Board) -> None:
    block = board.block_active
    assert block is not None
    while True:
        hits_bottom = block.get_bottommost_y() >= (board.height * BS)
        hits_block = block.collides_bottom(board.rect_list)
        if hits_bottom or hits_block:
            break
        move_down(board)


MOVE_MAPPING: dict[str, Callable[[Board], None]] = {
    'l': move_left,
    'r': move_right,
    'd': move_down,
    'R': rotate,
}


def create_board_from_script(
    moves: list[str],
    centered: bool = False,
    width: int = 10,
    height: int = 10,
) -> Board:
    board = Board(width=width, height=height, centered=centered)
    if not moves:
        return board

    # need to set it to None because otherwise, we will start with a random block
    board.block_active = None  # type: ignore
    for move in moves:
        block_type, *moves = list(move)
        block = BLOCK_MAPPING[block_type]()
        assert block_type == block.symbol

        board.spawn_block(block)
        for move in moves:
            MOVE_MAPPING[move](board)
        move_to_bottom(board)
    board.add_block(board.block_active)
    return board


def load_tetris(filename: str | Path) -> Tetris:
    replay = load_replay(filename)
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    tetris = Tetris(
        screen=screen,
        size=replay.game_info.size,
        seed=replay.game_info.seed,
    )
    if tetris.size == "small":
        width, height = 10, 10
    elif tetris.size == "normal":
        width, height = BLOCKS_WIDTH, BLOCKS_HEIGHT
    else:
        raise ValueError(f"size {tetris.size} not supported")

    board = create_board_from_script(
        replay.moves,
        width=width,
        height=height,
        centered=True,
    )
    tetris.board = board
    return tetris


def load_tetris_last() -> Tetris | None:
    """If there are replays, load the most recent game"""
    filenames_replay = sorted(PATH_REPLAYS.glob('*.json'))
    if not filenames_replay:
        return None

    filename_latest = filenames_replay[-1]
    return load_tetris(filename_latest)


def load_replays_all() -> list[Replay]:
    filenames_replay = PATH_REPLAYS.glob('*.json')
    return [load_replay(filename) for filename in filenames_replay]


def get_high_scores(
    *,
    topk: int = 10,
    replays: list[Replay] | None = None,
) -> list[tuple[int, dt.datetime]]:
    if replays is None:
        replays = load_replays_all()

    high_scores: list[tuple[int, dt.datetime]] = []
    for replay in replays:
        if replay.score is None:
            continue

        score = replay.score.get_total_score()
        date = dt.datetime.strptime(replay.meta_info.date[:16], "%Y-%m-%dT%H:%M")
        high_scores.append((score, date))

    high_scores = sorted(high_scores, reverse=True)[:topk]
    return high_scores
