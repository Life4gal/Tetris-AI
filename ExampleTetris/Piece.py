import enum
import random

import AI.StandardType as StandardType


def bin_to_dec(binary: str) -> int:
	return int(binary, 2)


class Piece(enum.Enum):
	TOTAL_PIECES = 7

	I = [
		#   O
		#   O
		#   O
		#   O
		StandardType.StandardDataFormat([1, 1, 1, 1], 1, 4),
		# OOOO
		StandardType.StandardDataFormat([bin_to_dec('1111')], 4, 1)
	]
	T = [
		#  O
		# OOO
		StandardType.StandardDataFormat([bin_to_dec('010'), bin_to_dec('111')], 3, 2),
		# O
		# OO
		# O
		StandardType.StandardDataFormat([bin_to_dec('10'), bin_to_dec('11'), bin_to_dec('10')], 2, 3),
		#  O
		# OO
		#  O
		StandardType.StandardDataFormat([bin_to_dec('01'), bin_to_dec('11'), bin_to_dec('01')], 2, 3),
		# OOO
		#  O
		StandardType.StandardDataFormat([bin_to_dec('111'), bin_to_dec('010')], 3, 2)
	]
	O = [
		# OO
		# OO
		StandardType.StandardDataFormat([bin_to_dec('11'), bin_to_dec('11')], 2, 2)
	]
	J = [
		# O
		# OOO
		StandardType.StandardDataFormat([bin_to_dec('100'), bin_to_dec('111')], 3, 2),
		# OO
		# O
		# O
		StandardType.StandardDataFormat([bin_to_dec('11'), bin_to_dec('10'), bin_to_dec('10')], 2, 3),
		# OOO
		#   O
		StandardType.StandardDataFormat([bin_to_dec('111'), bin_to_dec('001')], 3, 2),
		#  O
		#  O
		# OO
		StandardType.StandardDataFormat([bin_to_dec('01'), bin_to_dec('01'), bin_to_dec('11')], 2, 3)
	]
	L = [
		#   O
		# OOO
		StandardType.StandardDataFormat([bin_to_dec('001'), bin_to_dec('111')], 3, 2),
		# O
		# O
		# OO
		StandardType.StandardDataFormat([bin_to_dec('10'), bin_to_dec('10'), bin_to_dec('11')], 2, 3),
		# OOO
		# O
		StandardType.StandardDataFormat([bin_to_dec('111'), bin_to_dec('100')], 3, 2),
		# OO
		#  O
		#  O
		StandardType.StandardDataFormat([bin_to_dec('11'), bin_to_dec('01'), bin_to_dec('01')], 2, 3)
	]
	S = [
		#  OO
		# OO
		StandardType.StandardDataFormat([bin_to_dec('011'), bin_to_dec('110')], 3, 2),
		# O
		# OO
		#  O
		StandardType.StandardDataFormat([bin_to_dec('10'), bin_to_dec('11'), bin_to_dec('01')], 2, 3)
	]
	Z = [
		# OO
		#  OO
		StandardType.StandardDataFormat([bin_to_dec('110'), bin_to_dec('011')], 3, 2),
		#  O
		# OO
		# O
		StandardType.StandardDataFormat([bin_to_dec('01'), bin_to_dec('11'), bin_to_dec('10')], 2, 3)
	]

	@staticmethod
	def get_random_piece():
		index = random.randint(0, Piece.TOTAL_PIECES.value - 1)

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
