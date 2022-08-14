import itertools
from typing import Sequence, Type

import networkx as nx  # type: ignore

from citytetris.blocks import Block, IBlock, JBlock, LBlock, TBlock

Coord = tuple[int, int]


def _is_neighbor(coord0: Coord, coord1: Coord) -> bool:
    (x0, y0), (x1, y1) = coord0, coord1
    dx = abs(x0 - x1)
    dy = abs(y0 - y1)
    return dx + dy == 1


def blocks_touch(block0: Block, block1: Block) -> bool:
    """Check if two blocks touch each other.

    If the two blocks are the same, they touch each other.

    """
    # possible optimization: check the first coordinate - if it's too far away, it's
    # impossble for the blocks to touch and the check can be ended early.
    for coord0, coord1 in itertools.product(
        block0.yield_indices(), block1.yield_indices()
    ):
        if _is_neighbor(coord0, coord1):
            return True
    return False


def get_graph(
    block_list: list[Block], block_types: tuple[Type[Block], ...] | None
) -> nx.Graph:
    """Get the graph of all blocks of a certain type

    If no block type is specified, all blocks are considered.

    """
    if not block_types:
        block_list = block_list[:]
    else:
        block_list = [bl for bl in block_list if isinstance(bl, block_types)]

    graph = nx.Graph()
    for block in block_list:
        graph.add_node(block)

    for block0, block1 in itertools.combinations(block_list, 2):
        if blocks_touch(block0, block1):
            graph.add_edge(block0, block1)
    return graph


def get_digraph(
    block_list: list[Block], block_types: tuple[Type[Block]] | None
) -> nx.DiGraph:
    """Get the directed graph of all blocks of a certain type

    If no block type is specified, all blocks are considered.

    """
    if not block_types:
        block_list = block_list[:]
    else:
        block_list = [bl for bl in block_list if isinstance(bl, block_types)]

    graph = nx.DiGraph()
    for block in block_list:
        graph.add_node(block)

    for block0, block1 in itertools.combinations(block_list, 2):
        if blocks_touch(block0, block1):
            graph.add_edge(block0, block1)
    return graph


def min_max_indices(blocks: Sequence[Block]) -> tuple[int, int, int, int]:
    """Get the minimum and maximum indices of a block"""
    x_min, y_min, x_max, y_max = 999, 999, 0, 0
    for block in blocks:
        for x, y in block.yield_indices():
            x_min = min(x_min, x)
            y_min = min(y_min, y)
            x_max = max(x_max, x)
            y_max = max(y_max, y)
    return x_min, y_min, x_max, y_max


def get_longest_I_block_distance(block_list: list[Block]) -> tuple[int, set[Block]]:
    """Get the longest distance of interconnected I-blocks"""
    graph = get_graph(block_list, (IBlock,))
    if len(graph) < 2:
        return 0, set()

    max_distance = 0
    blocks_to_hightlight = []
    for block in graph.nodes():
        # This is actuallly inefficient, because we test the same subgraph multiple
        # times. There is probably a more efficient algorithm in networkx for this
        # purpose.
        blocks_connected = nx.node_connected_component(graph, block)
        if len(blocks_connected) < 2:
            continue
        x_min, y_min, x_max, y_max = min_max_indices(blocks_connected)
        distance = x_max - x_min + y_max - y_min
        if distance > max_distance:
            max_distance = distance
            blocks_to_hightlight = blocks_connected

    return max_distance, set(blocks_to_hightlight)


def _first_L_J_pair(graph: nx.Graph, blocks: Sequence[Block]) -> tuple[Block, Block]:
    """Get the first L-J pair in a list of blocks"""
    blocks_l = [bl for bl in blocks if isinstance(bl, LBlock)]
    for block_l in blocks_l:
        neighbors = graph.neighbors(block_l)
        for neighbor in neighbors:
            if isinstance(neighbor, JBlock):
                return block_l, neighbor
    raise ValueError("No L-J pair found, this should not happen")


def get_number_of_disconnected_L_J_graphs(
    block_list: list[Block],
) -> tuple[int, set[Block]]:
    graph = get_graph(block_list, (LBlock, JBlock))
    if len(graph) < 2:
        return 0, set()

    blocks_to_hightlight: list[Block] = []
    n = 0
    # count disconnected L-J graphs that have at least one L-J connection
    for component in nx.connected_components(graph):
        unique_block_types = set(map(type, component))
        if len(unique_block_types) > 1:
            n += 1
            blocks_to_hightlight.extend(_first_L_J_pair(graph, component))

    return n, set(blocks_to_hightlight)


def get_largest_T_community(block_list: list[Block]) -> tuple[int, set[Block]]:
    graph = get_graph(block_list, (TBlock,))
    if len(graph) < 2:
        return 0, set()

    blocks_to_hightlight = []
    # among all distinct T communities, find the largest one
    n_largest = 0
    for component in nx.connected_components(graph):
        if len(component) > n_largest:
            n_largest = len(component)
            blocks_to_hightlight = component

    # don't count groups of 0
    if n_largest == 1:
        return 0, set()
    return n_largest, set(blocks_to_hightlight)
