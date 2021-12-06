"""
Display
Handle user input
"""

import pygame as p
from Chess import ChessEngine


WIDTH = HEIGHT = 512
DIMENSION = 8  # board dimension
SQ_SIZE = HEIGHT // DIMENSION
MAX_FPS = 15
IMAGES = {}


def load_images():
    """
    :return: void
    Set string values for images path
    """
    pieces = ["wR", "wN", "wB", "wQ", "wK", "wP", "bR", "bN", "bB", "bQ", "bK", "bP"]
    for piece in pieces:
        IMAGES[piece] = p.transform.scale(p.image.load("images/" + piece + ".png"), (SQ_SIZE, SQ_SIZE))


def main():
    """
    Main Loop in game, initialize all variables and gameState
     :return: void
    """
    p.init()
    screen = p.display.set_mode((HEIGHT, WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
    valid_moves = game_state.get_valid_moves()
    move_made = True

    load_images()
    running = True

    square_selected = ()
    player_clicks = []

    while running:
        for e in p.event.get():
            if e.type == p.QUIT:
                running = False
            elif e.type == p.MOUSEBUTTONDOWN:
                location = p.mouse.get_pos()
                column = location[0] // SQ_SIZE
                row = location[1] // SQ_SIZE

                if square_selected == (row, column) or (not player_clicks and game_state.board[row][column] == "--"):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, column)
                    player_clicks.append(square_selected)

                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        if move in valid_moves:
                            game_state.make_move(move)
                            move_made = True
                            square_selected = ()
                            player_clicks = []
                        else:
                            player_clicks = [square_selected]
            elif e.type == p.KEYDOWN and e.key == p.K_LEFT:
                game_state.rollback_move()
                move_made = True

        if move_made:
            valid_moves = game_state.get_valid_moves()
            move_made = False

        draw_game_state(screen, game_state, square_selected, valid_moves)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, game_state, square_selected, valid_moves):
    """
    :param screen: p.screen
    :param game_state: GameState()
    :param square_selected: tuple of square
    :return:
    """
    draw_board(screen)
    if square_selected:
        draw_selected(screen, square_selected, p.Color(200, 0, 0, 1))
        draw_possible_moves(screen, square_selected, valid_moves)
    draw_pieces(screen, game_state.board)


def draw_board(screen):
    """
    :param screen: p.screen
    :return: void
    """
    colors = [p.Color("white"), p.Color("grey")]

    for row in range(DIMENSION):
        for column in range(DIMENSION):
            color = colors[((row + column) % 2)]
            p.draw.rect(screen, color, p.Rect(column * SQ_SIZE, row * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_pieces(screen, board):
    """
    :param screen: p.screen
    :param board: bidimensional list of strings which represent board
    :return:
    """
    for row in range(DIMENSION):
        for column in range(DIMENSION):
            piece = board[row][column]

            if piece != "--":
                screen.blit(IMAGES[piece], (column * SQ_SIZE, row * SQ_SIZE))


def draw_selected(screen, square, color):
    p.draw.rect(screen, color, p.Rect(square[1] * SQ_SIZE, square[0] * SQ_SIZE, SQ_SIZE, SQ_SIZE))


def draw_possible_move(screen, square, color):
    p.draw.circle(screen, color, (SQ_SIZE // 2 + square[1] * SQ_SIZE, SQ_SIZE // 2 + square[0] * SQ_SIZE), SQ_SIZE // 2)


def draw_possible_moves(screen, square, moves):
    for move in moves:
        if (move.start_row, move.start_column) == square:
            draw_possible_move(screen, (move.end_row, move.end_column), p.Color(130, 130, 130))


if __name__ == '__main__':
    main()
