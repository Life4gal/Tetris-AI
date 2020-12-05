"""
This file is about the implementation of the Tetris Piece

DataFormat:
    orientation:
        In the current direction, the VALUE of each row of a piece from top to bottom, stored them in a list
    width: width of this piece
    height: height of this piece

VALUE:
    we use X BIT BINARY to store the state of current row
    X is the COLUMNS of the game board

    e.g.
        X = 10, state is 1000011110
        This means that there are blocks in the 0,5,6,7,8 columns, and the 1,2,3,4,9 columns are empty
        and we store it as a decimal number 542
"""

import enum
import typing
import random


def bin_to_dec(binary: str) -> int:
    return int(binary, 2)


class DataFormat:
    def __init__(
            self,
            orientation: typing.List[int],
            width: int,
            height: int):
        self.orientation = orientation
        self.width = width
        self.height = height
        self.__validation()

    def __validation(self) -> None:
        assert len(self.orientation) == self.height, \
            f"Error: size must be {self.height}, but got {len(self.orientation)}"
        for i in self.orientation:
            assert i <= (1 << self.width) - 1, \
                f"Error: invalid number in {self.orientation}, " \
                f"the max should less than {(1 << self.width) - 1} (bit length is {self.width}) "


# Each block has its own unique shape, we use a list to store various shapes
class Piece(enum.Enum):
    TOTAL_PIECE = 7

    I = [
        #   O
        #   O
        #   O
        #   O
        DataFormat([1, 1, 1, 1], 1, 4),
        # OOOO
        DataFormat([bin_to_dec('1111')], 4, 1)
    ]
    T = [
        #  O
        # OOO
        DataFormat([bin_to_dec('010'), bin_to_dec('111')], 3, 2),
        # O
        # OO
        # O
        DataFormat([bin_to_dec('10'), bin_to_dec('11'), bin_to_dec('10')], 2, 3),
        #  O
        # OO
        #  O
        DataFormat([bin_to_dec('01'), bin_to_dec('11'), bin_to_dec('01')], 2, 3),
        # OOO
        #  O
        DataFormat([bin_to_dec('111'), bin_to_dec('010')], 3, 2)
    ]
    O = [
        # OO
        # OO
        DataFormat([bin_to_dec('11'), bin_to_dec('11')], 2, 2)
    ]
    J = [
        # O
        # OOO
        DataFormat([bin_to_dec('100'), bin_to_dec('111')], 3, 2),
        # OO
        # O
        # O
        DataFormat([bin_to_dec('11'), bin_to_dec('10'), bin_to_dec('10')], 2, 3),
        # OOO
        #   O
        DataFormat([bin_to_dec('111'), bin_to_dec('001')], 3, 2),
        #  O
        #  O
        # OO
        DataFormat([bin_to_dec('01'), bin_to_dec('01'), bin_to_dec('11')], 2, 3)
    ]
    L = [
        #   O
        # OOO
        DataFormat([bin_to_dec('001'), bin_to_dec('111')], 3, 2),
        # O
        # O
        # OO
        DataFormat([bin_to_dec('10'), bin_to_dec('10'), bin_to_dec('11')], 2, 3),
        # OOO
        # O
        DataFormat([bin_to_dec('111'), bin_to_dec('100')], 3, 2),
        # OO
        #  O
        #  O
        DataFormat([bin_to_dec('11'), bin_to_dec('01'), bin_to_dec('01')], 2, 3)
    ]
    S = [
        #  OO
        # OO
        DataFormat([bin_to_dec('011'), bin_to_dec('110')], 3, 2),
        # O
        # OO
        #  O
        DataFormat([bin_to_dec('10'), bin_to_dec('11'), bin_to_dec('01')], 2, 3)
    ]
    Z = [
        # OO
        #  OO
        DataFormat([bin_to_dec('110'), bin_to_dec('011')], 3, 2),
        #  O
        # OO
        # O
        DataFormat([bin_to_dec('01'), bin_to_dec('11'), bin_to_dec('10')], 2, 3)
    ]

    @staticmethod
    def get_random_piece():
        index = random.randint(0, Piece.TOTAL_PIECE.value - 1)

        if index == 0:
            return Piece.I
        elif index == 1:
            return Piece.T
        elif index == 2:
            return Piece.O
        elif index == 3:
            return Piece.J
        elif index == 4:
            return Piece.L
        elif index == 5:
            return Piece.S
        elif index == 6:
            return Piece.Z
