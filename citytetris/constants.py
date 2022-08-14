import pygame


# initialize font
pygame.font.init()

# graphical constants
BS = 30
CLOCKTICK = 15
CLOCK_BLOCK_MOVE = 50
BLOCKS_WIDTH = 10
BLOCKS_HEIGHT = 20
FONTSIZE = 20
FONT = pygame.font.SysFont("monospace", FONTSIZE, bold=True)
SCREEN_WIDTH = max(600, 2 * BS * (2 + BLOCKS_WIDTH))
SCREEN_HEIGHT = max(600, BS * (2 + BLOCKS_HEIGHT))
# boxes
BOX_BORDER_X = 8
BOX_BORDER_Y = 5

# gameplay constants
TIME_BETWEEN_BLOCKS = 50
TIME_BEFORE_GAME_OVER = 500
TIME_BEFORE_NEW_SPAWN = 150

# paths
PATH_REPLAYS = 'replays'

# scores
class SCORES:
    full_rows = 3
    longest_road = 1
    l_j_communities = 4
    t_community = 6
