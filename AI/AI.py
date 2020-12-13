import StandardType


class AI:
	def __init__(self):
		self.__tetris: StandardType.StandardTetris = ...
		self.__scores: int = 0

		self.__inited: bool = False

	def set_tetris(self, tetris: StandardType.StandardTetris) -> None:
		self.__tetris = tetris
		self.__inited = True

	def get_scores(self) -> int:
		return self.__scores

	def play(self, current_piece: StandardType.StandardPiece) -> bool:
		assert self.__inited, f"Error: You should init the AI first!"

		pick: StandardType.StandardMoveEvaluatedInfo = self.pick_move(current_piece)
		do_it: StandardType.StandardGameStateInfo = \
			AI.do_move(self.__tetris.board, pick.best_orientation, pick.best_place_column)

		if not do_it.is_game_over:
			# if game not over, we can cast it to StandardMoveStateInfo safety
			do_it.__class__ = StandardType.StandardMoveStateInfo
			self.__scores += do_it.eliminated_rows
			return True
		else:
			return False

	def pick_move(self, current_piece: StandardType.StandardPiece) -> StandardType.StandardMoveEvaluatedInfo:
		"""
		Pick the best move possible (orientation and location) as determined by the evaluation function.
		Given a tetris piece, tries all possible orientations
		and locations and to calculate (what it thinks) is the best move.
		:param current_piece: A tetris piece
		:return: A Sign contained all information we need
		"""
		best_evaluation = -100000
		best_orientation: StandardType.StandardOrientation = []
		best_column = 0

		# Evaluate all possible orientations
		for this_shape in current_piece:
			orientation = this_shape.orientation

			# Evaluate all possible columns
			for column in range(self.__tetris.number_of_columns - this_shape.width + 1):
				# Copy current board
				board = self.__tetris.board.copy()
				move_info: StandardType.StandardGameStateInfo = AI.do_move(board, orientation, column)

				if not move_info.is_game_over:
					# if game not over, we can cast it to StandardMoveStateInfo safety
					move_info.__class__ = StandardType.StandardMoveStateInfo
					evaluation = AI.evaluate_board_coefficient(move_info, board, self.__tetris.number_of_columns)

					if evaluation > best_evaluation:
						best_evaluation = evaluation
						best_orientation = orientation
						best_column = column

			return StandardType.StandardMoveEvaluatedInfo(
				current_piece[0] if len(best_orientation) == 0 else best_orientation,
				best_column
			)

	@staticmethod
	def do_move(
			board: StandardType.StandardBoard,
			best_orientation: StandardType.StandardOrientation,
			which_column: int) -> StandardType.StandardGameStateInfo:
		"""
		Do a move
		:param board: The AI board
		:param best_orientation: All orientation info about this piece
		:param which_column: Which column this action place
		:return: A Sign contained all information we need
		"""
		best_orientation = AI.move_piece_horizontally(best_orientation, which_column)
		current_landing_height = AI.get_placeable_row(board, best_orientation)

		if current_landing_height + len(best_orientation) > len(board):
			return StandardType.StandardGameStateInfo()

		for i in range(len(best_orientation)):
			board[current_landing_height + i] |= best_orientation[i]

		# Remove all full rows
		i = 0
		eliminated_rows = 0
		while i < len(best_orientation):
			if board[current_landing_height + i] == StandardType.StandardTetris.FULL_ROW_VALUE:
				board.pop(current_landing_height + i)
				# Add an empty row on top
				board.append(0)
				# Since we have decreased the number of rows by one, we need to adjust the index accordingly
				i -= 1
				eliminated_rows += 1
			i += 1

		return \
			StandardType.StandardMoveStateInfo(current_landing_height, best_orientation, eliminated_rows)

	@staticmethod
	def move_piece_horizontally(
			orientation: StandardType.StandardOrientation,
			which_column: int) -> StandardType.StandardOrientation:
		"""
		Move piece to the specified column
		Just need left shift it
		:param orientation: All orientation info about this piece
		:param which_column: Which column to place
		:return: New orientations after move
		"""
		return [(i << which_column) for i in orientation]

	@staticmethod
	def get_placeable_row(board: StandardType.StandardBoard, orientation: StandardType.StandardOrientation) -> int:
		"""
		Find which row current piece could place
		:param board: The AI board
		:param orientation: All orientation info about this piece
		:return: The row we could place
		"""
		# Descend from top to find the highest row that will collide with the our piece.
		for row in range(len(board) - len(orientation), -1, -1):
			# Check if piece collides with the cells of the current row.
			for i in range(len(orientation)):
				if (board[row + i] & orientation[i]) != 0:
					# Found collision - place piece on row above.
					return row + 1

		return 0  # No collision found, piece should be placed on first row.

	@staticmethod
	def evaluate_board_coefficient(
			move_info: StandardType.StandardMoveStateInfo,
			board: StandardType.StandardBoard,
			total_columns: int) -> float:
		"""
		Evaluate the board, giving a higher score to boards that "look" better.
		:param move_info: see Game.Info
		:param board: The AI board
		:param total_columns: Number of columns in the board
		:return: A number indicating how "good" a board is, the higher the number, the better the board.
		"""
		return \
			move_info.eliminated_rows * 3.4181268101392694 + \
			AI.__get_landing_height(move_info) * -4.500158825082766 + \
			AI.__get_row_transitions(board, total_columns) * -3.2178882868487753 + \
			AI.__get_column_transitions(board, total_columns) * -9.348695305445199 + \
			AI.__get_number_of_holes(board, total_columns) * -7.899265427351652 + \
			AI.__get_well_sums(board, total_columns) * -3.3855972247263626

	@staticmethod
	def __get_landing_height(move_info: StandardType.StandardMoveStateInfo) -> int:
		return move_info.current_landing_height + (len(move_info.best_orientation) - 1) // 2

	@staticmethod
	def __get_row_transitions(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		A row transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.
		:param board: The AI board
		:param total_columns: Number of columns in the board
		:return: The total number of row transitions
		"""
		transition = 0
		last_bit = 1

		for row in board:
			bit = 0
			for i in range(total_columns):
				bit = (row >> i) & 1

				if bit != last_bit:
					transition += 1

				last_bit = bit

			if bit == 0:
				transition += 1

			last_bit = 1

		return transition

	@staticmethod
	def __get_column_transitions(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		A column transition occurs when an empty cell is adjacent to a filled cell on the same row and vice versa.
		:param board: The AI board
		:param total_columns: Number of columns in the board
		:return: The total number of column transitions
		"""
		transition = 0
		last_bit = 1

		for i in range(total_columns):
			for row in board:
				bit = (row >> i) & 1

				if bit != last_bit:
					transition += 1

				last_bit = bit

			last_bit = 1

		return transition

	@staticmethod
	def __get_number_of_holes(board: StandardType.StandardBoard, total_columns: int) -> int:
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
	def __get_well_sums(board: StandardType.StandardBoard, total_columns: int) -> int:
		"""
		A well is a sequence of empty cells above the top piece in a column such
		that the top cell in the sequence is surrounded (left and right) by occupied
		cells or a boundary of the board.
		:param board: The AI board
		:param total_columns: Number of columns in the board
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
		for i in range(1, total_columns):
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
			if ((row >> (total_columns - 1)) & 1) == 0 and ((row >> (total_columns - 2)) & 1) == 1:
				# Found well cell, count it + the number of empty cells below it.
				well_sums += 1

				for r in board_copy[index + 1:]:
					if ((r >> (total_columns - 1)) & 1) == 0:
						well_sums += 1
					else:
						break

		return well_sums
