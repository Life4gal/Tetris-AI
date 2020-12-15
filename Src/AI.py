"""
This file is about the implementation of the AI
"""

import typing
from .Game import Tetris, Info
from .Piece import Piece


class AI:
	def __init__(self, columns: int, rows: int):
		"""
		:param columns: Total columns in board
		:param rows: Total rows in board
		"""
		self.tetris = Tetris(columns, rows)
		self.current_piece: Piece = ...
		self.total_row_removed: int = 0

	def play(self) -> Info:
		"""
		Get a random piece, find how and where to place it
		:return: A Sign contained all information we need
		"""
		self.current_piece = Piece.get_random_piece()
		move: Info = self.pick_move(self.current_piece)

		last_move: Info = \
			self.play_move(self.tetris.board, move.orientation, move.column)

		if not last_move.game_over:
			self.total_row_removed += last_move.row_removed

		return last_move

	def pick_move(self, piece: Piece) -> Info:
		"""
		Pick the best move possible (orientation and location) as determined by the evaluation function.
		Given a tetris piece, tries all possible orientations
		and locations and to calculate (what it thinks) is the best move.
		:param piece: A tetris piece
		:return: A Sign contained all information we need
		"""
		best_evaluation = -100000
		best_orientation: typing.List[int] = []
		best_column = 0

		# Evaluate all possible orientations
		for this_shape in piece.value:
			this_shape: Piece.DataFormat
			orientation = this_shape.orientation

			# Evaluate all possible columns
			for column in range(self.tetris.number_of_columns - this_shape.width + 1):
				# Copy current board
				board = self.tetris.board.copy()
				last_move: Info = AI.play_move(board, orientation, column)

				if not last_move.game_over:
					evaluation = self.evaluate_board(last_move, board, self.tetris.number_of_columns)

					if evaluation > best_evaluation:
						best_evaluation = evaluation
						best_orientation = orientation
						best_column = column

		return Info(
			best_orientation=piece.value[0] if len(best_orientation) == 0 else best_orientation,
			best_place_column=best_column
		)

	@staticmethod
	def play_move(board: typing.List[int], orientation: typing.List[int], which_column: int) -> Info:
		"""
		Do a move
		:param board: The AI board
		:param orientation: All orientation info about this piece
		:param which_column: Which column this action place
		:return: A Sign contained all information we need
		"""
		orientation = AI.move_piece(orientation, which_column)
		placement_row = AI.get_placement_row(board, orientation)

		if placement_row + len(orientation) > len(board):
			return Info(game_over=True)

		for i in range(len(orientation)):
			board[placement_row + i] |= orientation[i]

		# Remove all full rows
		i = 0
		row_removed = 0
		while i < len(orientation):
			if board[placement_row + i] == Tetris.FULL_ROW_VALUE:
				board.pop(placement_row + i)
				# Add an empty row on top
				board.append(0)
				# Since we have decreased the number of rows by one, we need to adjust the index accordingly
				i -= 1
				row_removed += 1
			i += 1
		return \
			Info(landing_height=placement_row, best_orientation=orientation, row_removed=row_removed, game_over=False)

	@staticmethod
	def move_piece(orientations: typing.List[int], which_column: int) -> typing.List[int]:
		"""
		Move piece to the specified column
		Just need left shift it
		:param orientations: All orientation info about this piece
		:param which_column: Which column to place
		:return: New orientations after move
		"""
		return [(i << which_column) for i in orientations]

	@staticmethod
	def get_placement_row(board: typing.List[int], orientations: typing.List[int]) -> int:
		"""
		Find which row current piece could place
		:param board: The AI board
		:param orientations: All orientation info about this piece
		:return: The row we could place
		"""
		# Descend from top to find the highest row that will collide with the our piece.
		for row in range(len(board) - len(orientations), -1, -1):
			# Check if piece collides with the cells of the current row.
			for i in range(len(orientations)):
				if (board[row + i] & orientations[i]) != 0:
					# Found collision - place piece on row above.
					return row + 1

		return 0  # No collision found, piece should be placed on first row.

	@staticmethod
	def evaluate_board(last_move: Info, board: typing.List[int], total_columns: int) -> float:
		"""
		Evaluate the board, giving a higher score to boards that "look" better.
		:param last_move: see Game.Info
		:param board: The AI board
		:param total_columns: Number of columns in the board
		:return: A number indicating how "good" a board is, the higher the number, the better the board.
		"""
		return \
			last_move.row_removed * 3.4181268101392694 + \
			AI.__get_landing_height(last_move) * -4.500158825082766 + \
			AI.__get_row_transitions(board, total_columns) * -3.2178882868487753 + \
			AI.__get_column_transitions(board, total_columns) * -9.348695305445199 + \
			AI.__get_number_of_holes(board, total_columns) * -7.899265427351652 + \
			AI.__get_well_sums(board, total_columns) * -3.3855972247263626

	@staticmethod
	def __get_landing_height(last_move: Info) -> int:
		return last_move.landing_height + (len(last_move.orientation) - 1) // 2

	@staticmethod
	def __get_row_transitions(board: typing.List[int], columns: int) -> int:
		"""
		A row transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.
		:param board: The AI board
		:param columns: Number of columns in the board
		:return: The total number of row transitions
		"""
		transition = 0
		last_bit = 1

		for row in board:
			bit = 0
			for i in range(columns):
				bit = (row >> i) & 1

				if bit != last_bit:
					transition += 1

				last_bit = bit

			if bit == 0:
				transition += 1

			last_bit = 1

		return transition

	@staticmethod
	def __get_column_transitions(board: typing.List[int], columns: int) -> int:
		"""
		A column transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.
		:param board: The AI board
		:param columns: Number of columns in the board
		:return: The total number of column transitions
		"""
		transition = 0
		last_bit = 1

		for i in range(columns):
			for row in board:
				bit = (row >> i) & 1

				if bit != last_bit:
					transition += 1

				last_bit = bit

			last_bit = 1

		return transition

	@staticmethod
	def __get_number_of_holes(board: typing.List[int], total_columns: int) -> int:
		"""
		:param board: The AI board
		:param total_columns: Number of columns in the board
		:return: The total number of holes
		"""
		holes = 0
		row_holes = 0
		previous_row = board[-1]

		# traverse from top to bottom
		for row in board[-2::-1]:
			row_holes = ~row & (previous_row | row_holes)

			for i in range(total_columns):
				holes += (row_holes >> i) & 1

			previous_row = row

		return holes

	@staticmethod
	def __get_well_sums(board: typing.List[int], columns: int) -> int:
		"""
		A well is a sequence of empty cells above the top piece in a column such
		that the top cell in the sequence is surrounded (left and right) by occupied
		cells or a boundary of the board.
		:param board: The AI board
		:param columns: Number of columns in the board
		:return:
			The well sums. For a well of length n, we define the well sums as
			1 + 2 + 3 + ... + n. This gives more significance to deeper holes.
		"""
		well_sums = 0
		# reverse the board, because we travel it from top to bottom
		# use a copy, do not change the origin board
		board_copy = board[::-1]

		# Check for well cells in the "inner columns" of the board.
		# "inner columns" are the columns that aren't touching the edge of the board.
		for i in range(1, columns):
			for index, row in enumerate(board_copy):
				if ((row >> i) & 1) == 0 and ((row >> (i - 1)) & 1) == 1 and ((row >> (i + 1)) & 1) == 1:
					# Found well cell, count it + the number of empty cells below it.
					well_sums += 1

					for r in board_copy[index + 1:]:
						if ((r >> i) & 1) == 0:
							well_sums += 1
						else:
							break

		# Check for well cells in the leftmost column of the board.
		for index, row in enumerate(board_copy):
			if ((row >> 0) & 1) == 0 and ((row >> (0 + 1)) & 1) == 1:
				# Found well cell, count it + the number of empty cells below it.
				well_sums += 1

				for r in board_copy[index + 1:]:
					if ((r >> 0) & 1) == 0:
						well_sums += 1
					else:
						break

		# Check for well cells in the rightmost column of the board.
		for index, row in enumerate(board_copy):
			if ((row >> (columns - 1)) & 1) == 0 and ((row >> (columns - 2)) & 1) == 1:
				# Found well cell, count it + the number of empty cells below it.
				well_sums += 1

				for r in board_copy[index + 1:]:
					if ((r >> (columns - 1)) & 1) == 0:
						well_sums += 1
					else:
						break

		return well_sums
