import os
from functools import wraps

import pytest

from citytetris.network import blocks_touch
from citytetris.replay import create_board_from_script, load_tetris


def verify_board(func):
    doc = func.__doc__
    doc_normalized = "\n".join(line.strip() for line in doc.splitlines()).strip()

    @wraps(func)
    def wrapper(*args, **kwargs):
        board = func(*args, **kwargs)
        board_repr = repr(board)
        assert board_repr == doc_normalized
        return board

    return wrapper


class TestScoreFullLines:
    @verify_board
    def test_zero_full_lines_0(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #####################
        """
        instructions = []
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.full_rows == 0
        return board

    @verify_board
    def test_zero_full_lines_1(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                L  #
        #    I I I I L L L  #
        #O O     T T T Z Z  #
        #O O       T     Z Z#
        #####################
        """
        instructions = ["Trrrr", "O", "Irr", "Zrrrrrrr", "LRRrrrrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.full_rows == 0
        return board

    @verify_board
    def test_zero_full_lines_2(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #I                  #
        #I                  #
        #I                  #
        #I I I I I I I I I  #
        #####################
        """
        instructions = ["Irrrrr", "Ir", "IR"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.full_rows == 0
        return board

    @verify_board
    def test_zero_full_lines_3(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #I                  #
        #I                  #
        #I                  #
        #I I I I I   I I I I#
        #####################
        """
        instructions = ["Irrrrrr", "Ir", "IR"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.full_rows == 0
        return board

    @verify_board
    def test_zero_full_lines_4(self):
        """
        #####################
        #I I I I            #
        #J J J              #
        #    J              #
        #    J              #
        #    J              #
        #  J J              #
        #    I              #
        #    I              #
        #    I              #
        #    I              #
        #####################
        """
        instructions = ["IRrr", "JRr", "J", "I"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.full_rows == 0
        return board

    @verify_board
    def test_one_full_line(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #  S S           Z  #
        #S S O O J     Z Z  #
        #  T O O J J J Z T  #
        #T T T I I I I T T T#
        #####################
        """
        instructions = [
            'TlRllRl',
            'TlrRrRrr',
            'Il',
            'Oll',
            'ZrrRr',
            'JRR',
            'Sllll',
        ]
        board = create_board_from_script(instructions, centered=True)
        score = board.calculate_score()
        assert score.full_rows == 1
        return board

    @verify_board
    def test_two_full_lines(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                  I#
        #  S S     O O   Z I#
        #S S O O J O O Z Z I#
        #  T O O J J J Z T I#
        #T T T I I I I T T T#
        #####################
        """
        instructions = [
            'TlRllRl',
            'TlrRrRrr',
            'Il',
            'Oll',
            'ZrrRr',
            'JRR',
            'Sllll',
            'Or',
            'IRrrrrr',
        ]
        board = create_board_from_script(instructions, centered=True)
        score = board.calculate_score()
        assert score.full_rows == 2
        return board


class TestBlocksTouching:
    @verify_board
    def test_horizontal_touch(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #  T             T  #
        #T T T I I I I T T T#
        #####################
        """
        instructions = ['TlRllRl', 'TlrRrRrr', 'Il']
        board = create_board_from_script(instructions, centered=True)
        block0, block1, block2 = board.block_list

        assert not blocks_touch(block0, block1)
        assert not blocks_touch(block1, block0)
        assert blocks_touch(block0, block2)
        assert blocks_touch(block2, block0)
        assert blocks_touch(block1, block2)
        assert blocks_touch(block2, block1)

        return board

    @verify_board
    def test_vertical_touch(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #    L              #
        #L L L              #
        #O O   O O          #
        #O O   O O          #
        #####################
        """
        instructions = ['O', 'Orrr', 'LRR']
        board = create_board_from_script(instructions, centered=False)
        block0, block1, block2 = board.block_list

        assert not blocks_touch(block0, block1)
        assert not blocks_touch(block1, block0)
        assert blocks_touch(block0, block2)
        assert blocks_touch(block2, block0)
        assert not blocks_touch(block1, block2)
        assert not blocks_touch(block2, block1)

        return board

    @verify_board
    def test_multiple_touch(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #I                  #
        #I                  #
        #I I I I I I        #
        #I       J I        #
        #O O     J I        #
        #O O   J J I        #
        #####################
        """
        instructions = ['Ollll', 'JRl', 'IRllll', 'Illl', 'IRr']
        board = create_board_from_script(instructions, centered=True)
        block0, block1, block2, block3, block4 = board.block_list

        assert not blocks_touch(block0, block1)
        assert not blocks_touch(block1, block0)
        assert blocks_touch(block0, block2)
        assert blocks_touch(block2, block0)
        assert not blocks_touch(block0, block3)
        assert not blocks_touch(block3, block0)
        assert not blocks_touch(block0, block4)
        assert not blocks_touch(block4, block0)

        assert not blocks_touch(block1, block2)
        assert not blocks_touch(block2, block1)
        assert blocks_touch(block1, block3)
        assert blocks_touch(block3, block1)
        assert blocks_touch(block1, block4)
        assert blocks_touch(block4, block1)

        assert blocks_touch(block2, block3)
        assert blocks_touch(block3, block2)
        assert not blocks_touch(block2, block4)
        assert not blocks_touch(block4, block2)

        assert blocks_touch(block3, block4)
        assert blocks_touch(block4, block3)

        return board


class TestLongestRoad:
    def test_no_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #####################
        """
        instructions = []
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.longest_road == 0
        return board

    def test_no_I_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #      J            #
        #O O   J            #
        #O O J J            #
        #####################
        """
        instructions = ["O", "JRrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.longest_road == 0
        return board

    def test_no_two_touching_I_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #I                  #
        #I                  #
        #I   I I I I        #
        #I     J            #
        #O O   J            #
        #O O J J            #
        #####################
        """
        # a road needs at least 2 touching I blocks
        instructions = ["O", "JRrr", "Irr", "IR"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.longest_road == 0
        return board

    @verify_board
    def test_2_vertical_touching_I_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #I I                #
        #I I                #
        #I I                #
        #I I                #
        #####################
        """
        instructions = ['IR', 'IRr']
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.longest_road == 4
        return board

    @verify_board
    def test_2_perpendicular_touching_I_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #I                  #
        #I                  #
        #I                  #
        #I I I I I          #
        #####################
        """
        instructions = ['IR', 'Ir']
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.longest_road == 7
        return board

    @verify_board
    def test_3_touching_I_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #I                  #
        #I                  #
        #I I I I I I   I I  #
        #I       J I   I I  #
        #O O     J I   I I  #
        #O O   J J I   I I  #
        #####################
        """
        instructions = ['Ollll', 'JRl', 'IRllll', 'Illl', 'IRr', 'IRrrr', 'IRrrrr']
        board = create_board_from_script(instructions, centered=True)
        score = board.calculate_score()
        assert score.longest_road == 10
        return board

    @verify_board
    def test_2_I_blocks_higher_score_than_3(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #          I        #
        #I I I     I        #
        #I I I     I        #
        #I I I     I        #
        #I I I   I I I I    #
        #####################
        """
        # the block of 3 has max distance of 6, the block of 2 has max distance of 7
        instructions = ['IR', 'IRr', 'IRrr', 'Irrrr', 'IRrrrrr']
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.longest_road == 7
        return board


class TestLJCommunities:
    @verify_board
    def test_no_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #####################
        """
        instructions = []
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 0
        return board

    @verify_board
    def test_L_J_not_touching(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #L       J          #
        #L       J          #
        #L L   J J          #
        #####################
        """
        instructions = ["LRRR", "JRrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 0
        return board

    @verify_board
    def test_one_L_J_community(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #L     J            #
        #L     J            #
        #L L J J            #
        #####################
        """
        instructions = ["LRRR", "JRrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 1
        return board

    @verify_board
    def test_LL_JJ_dont_count(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #        J          #
        #        J          #
        #  L   J J          #
        #L L     J          #
        #L L L   J          #
        #L L   J J          #
        #####################
        """
        instructions = ["LRRR", "LRRRr", "JRrrr", "JRrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 0
        return board

    @verify_board
    def test_one_L_two_J_community(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #    J              #
        #L   J J            #
        #L J J J            #
        #L L J J            #
        #####################
        """
        instructions = ["LRRR", "JRrr", "JRr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 1
        return board

    @verify_board
    def test_two_L_two_J_community(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #L                  #
        #L                  #
        #L L J              #
        #L   J J            #
        #L J J J            #
        #L L J J            #
        #####################
        """
        instructions = ["LRRR", "JRrr", "JRr", "LRRR"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 1
        return board

    @verify_board
    def test_two_L_J_communities(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #L     J         L  #
        #L     J   J L L L  #
        #L L J J   J J J    #
        #####################
        """
        instructions = ["LRRR", "JRrr", "JRRrrrrr", "LRRrrrrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.l_j_communities == 2
        return board

    @verify_board
    def test_many_blocks(self):
        """
        #####################
        #    J              #
        #    J              #
        #  J J L J          #
        #  L L L J J J      #
        #    O O S J J J O O#
        #O O O O S S   J O O#
        #O O   Z Z S O O J  #
        #L O O J Z Z O O J  #
        #L O O J O O   J J L#
        #L L J J O O   L L L#
        #####################
        """
        instructions = [
            'LlRRRlll',
            'JRll',
            'LRrrRr',
            'O',
            'JRrrr',
            'Olll',
            'Ollll',
            'Zl',
            'Orr',
            'Olrll',
            'Orrrr',
            'SrRl',
            'Jr',
            'JRR',
            'LRRlll',
            'JlllR',
        ]
        board = create_board_from_script(instructions, centered=True)
        score = board.calculate_score()
        assert score.l_j_communities == 3
        return board


class TestTCommunity:
    @verify_board
    def test_no_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #####################
        """
        instructions = []
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.t_community == 0
        return board

    @verify_board
    def test_one_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #T T T              #
        #  T                #
        #####################
        """
        instructions = ["T"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.t_community == 0
        return board

    @verify_board
    def test_two_blocks_not_touching(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #T T T   T          #
        #  T   T T T        #
        #####################
        """
        instructions = ["T", "TRRrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.t_community == 0
        return board

    @verify_board
    def test_two_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #        T          #
        #T T T T T          #
        #  T     T          #
        #####################
        """
        instructions = ["T", "TRrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.t_community == 2
        return board

    @verify_board
    def test_two_times_two_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #                  T#
        #        T       T T#
        #T T T T T       T T#
        #  T     T     T T T#
        #####################
        """
        instructions = ["T", "TRrrr", "TRRrrrrrrr", "TRrrrrrrrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.t_community == 2
        return board

    @verify_board
    def test_two_blocks_and_four_blocks(self):
        """
        #####################
        #                   #
        #                   #
        #                   #
        #                   #
        #                   #
        #T     T            #
        #T T T T T         T#
        #T       T       T T#
        #T T T T T       T T#
        #  T     T     T T T#
        #####################
        """
        instructions = ["T", "TRrrr", "TRRrrrrrrr", "TRrrrrrrrr", "TRRR", "TRRrr"]
        board = create_board_from_script(instructions)
        score = board.calculate_score()
        assert score.t_community == 4
        return board

    @verify_board
    def test_many_blocks(self):
        """
        #####################
        #                   #
        #        L L L      #
        #        L     Z Z  #
        #J J J   S S     Z Z#
        #    J S S     Z Z  #
        #I I I I T   T   Z Z#
        #T T T T T T T Z Z  #
        #  T     T   T   Z Z#
        #  T     T Z Z Z Z  #
        #T T T T T T Z Z Z Z#
        #####################
        """
        instructions = [
            'TRRllll',
            'TRRl',
            'Zrrl',
            'Zrrr',
            'TRlRlRllR',
            'TRl',
            'Zrrrlr',
            'TrR',
            'Illll',
            'Zrrr',
            'Jllll',
            'Sl',
            'Zrrr',
            'L',
        ]
        board = create_board_from_script(instructions, centered=True)
        score = board.calculate_score()
        assert score.t_community == 5
        return board


class TestReplay:
    @pytest.fixture(scope='class')
    def tetris1(self):
        return load_tetris(os.path.join('tests', 'replay-01.json'))

    def test_tetris1(self, tetris1):
        board_expected = """
#####################
#                   #
#        T T T      #
#        I T        #
#    L L I          #
#      L I O O      #
#      L I O O S S  #
#      J J J S S    #
#          J Z      #
#          Z Z      #
#          Z I I I I#
#      I I I I     T#
#J J J   O O     T T#
#    J   O O T T T T#
#    L L L S S T    #
#    L   S S        #
#          Z        #
#        Z Z        #
#        Z          #
#        Z Z        #
#          Z Z      #
#####################""".strip()
        assert repr(tetris1.board) == board_expected

    @pytest.fixture(scope='class')
    def tetris2(self):
        return load_tetris(os.path.join('tests', 'replay-02.json'))

    def test_tetris2(self, tetris2):
        board_expected = """
#####################
#                   #
#          T        #
#        T T        #
#          T        #
#          T        #
#        T T        #
#      Z Z T        #
#        Z Z        #
#          J J J    #
#          S S J    #
#        S S L L    #
#              L    #
#              L    #
#              O O  #
#              O O  #
#        I I I I    #
#        I          #
#        I          #
#        I          #
#        I          #
#####################""".strip()
        assert repr(tetris2.board) == board_expected
