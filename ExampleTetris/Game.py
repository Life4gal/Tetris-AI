import pygame
import typing
import random

import AI.AI as AI
import AI.StandardType as StandardType
import ExampleTetris.Piece as Piece

"""
You can customize the display by changing the following 5 variables
(SCREEN_WIDTH, SCREEN_HEIGHT, BLOCK_SIZE, COLUMNS, ROWS), 
but pay attention to the values of COLUMNS and BLOCK_SIZE. 
If their product is greater than SCREEN_WIDTH, it will be out of bounds. 
The same is true for ROWS.
"""
SCREEN_WIDTH = 600
SCREEN_HEIGHT = 1200
BLOCK_SIZE = 50
COLUMNS = 10
ROWS = 20
# You should not need to change the following 2 values
GAME_FIELD_END_X = (SCREEN_WIDTH - BLOCK_SIZE * COLUMNS) // 2 - BLOCK_SIZE + BLOCK_SIZE * COLUMNS
GAME_FIELD_END_Y = (SCREEN_HEIGHT - BLOCK_SIZE * (ROWS + 1)) // 2 + BLOCK_SIZE * ROWS

# pygame init
pygame.init()
pygame.font.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Tetris-AI")
font = pygame.font.SysFont("Comic Sans MS", 60)

g_ai = AI.AI()
g_tetris = StandardType.StandardTetris(COLUMNS, ROWS)
g_ai.set_tetris(g_tetris)
g_piece: Piece.Piece = ...


def get_random_color() -> typing.Tuple[int, int, int]:
	"""
	Get a random color, it will affect performance, but just leave it alone, just make it looks good :).
	:return:
	"""
	return random.randint(1, 255), random.randint(1, 255), random.randint(1, 255)


def draw_board() -> None:
	"""
	Show the situation of the board
	:return: None
	"""
	screen.fill((0, 0, 0))
	for row in range(ROWS):
		column = 0
		row_value = g_ai.tetris.board[row]
		# after every action we replace all block, so if this row has no block
		# we think the row above also are blank
		if row_value == 0:
			return
		while column < COLUMNS:
			if row_value & 1:
				pygame.draw.rect(
					screen,
					get_random_color(),
					(
						GAME_FIELD_END_X - column * BLOCK_SIZE,
						GAME_FIELD_END_Y - row * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE
					),
					5, 5
				)
			row_value >>= 1
			column += 1


def draw_score() -> None:
	"""
	Show current score
	:return: None
	"""
	score = font.render(f"Score: {g_ai.scores}", True, get_random_color())
	rect = score.get_rect()
	rect.topleft = (SCREEN_WIDTH // 2 - rect.w // 2, (SCREEN_HEIGHT - BLOCK_SIZE * ROWS) // 2)
	screen.blit(score, rect)


def draw_current_piece():
	"""
	Show current piece

	Note:
		we set height to (SCREEN_HEIGHT - BLOCK_SIZE * ROWS) // 2 + BLOCK_SIZE，
		this means we are BLOCK_SIZE lower than the position where score is displayed,
		so do not make the font size too big
	:return: None
	"""
	height = (SCREEN_HEIGHT - BLOCK_SIZE * ROWS) // 2 + BLOCK_SIZE
	# we just need the last character of name
	name = font.render(f"Current Piece: {g_piece.name[-1]}", True, get_random_color())
	rect = name.get_rect()
	rect.topleft = (SCREEN_WIDTH // 2 - rect.w // 2, height)
	screen.blit(name, rect)

	# use the first data for show
	data: StandardType.StandardDataFormat = g_piece.value[0]
	height += rect.h
	sx = SCREEN_WIDTH // 2 - (BLOCK_SIZE * data.width) // 2
	for row in data.data:
		column = 0
		while column < data.width:
			if row & 1:
				pygame.draw.rect(
					screen,
					get_random_color(),
					(sx + BLOCK_SIZE * column, height, BLOCK_SIZE, BLOCK_SIZE),
					5, 5
				)
			row >>= 1
			column += 1
		height += BLOCK_SIZE


if __name__ == '__main__':
	while True:
		g_piece = Piece.Piece.get_random_piece()
		_ = g_ai.play(g_piece.value)
		draw_board()
		draw_score()
		draw_current_piece()
		pygame.display.update()
