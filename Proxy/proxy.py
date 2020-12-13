"""
Usually, whether it is a one-dimensional or two-dimensional implementation of Tetris,
there needs to be a way to store the current board state.

Our AI is designed for one-dimensional board,
so we need a way to convert your board to one-dimensional.

StandardDataFormat:
	orientation:
		In the current direction, the VALUE of each row of a piece from top to bottom, stored them in a list
	width: width of this piece
	height: height of this piece

VALUE:
	we use X BIT BINARY to store the state of current row
	X is the COLUMNS of the AI board

	e.g.
		X = 10, state is 1000011110
		This means that there are blocks in the 0,5,6,7,8 columns, and the 1,2,3,4,9 columns are empty
		and we store it as a decimal number 542

"""
import AI.StandardType as StandardType


# for detail, see AI/StandardType
class Proxy:
	@staticmethod
	def piece_parse(piece_data) -> StandardType.StandardPiece:
		# implement this to parse your piece_data to our standard data format
		...

	@staticmethod
	def orientation(orientation_data) -> StandardType.StandardOrientation:
		...

	@staticmethod
	def board_parse(board_data) -> StandardType.StandardBoard:
		# implement this to parse your board_data to our standard board fomat
		...
