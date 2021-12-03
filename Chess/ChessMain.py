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
    :return: void

    Main Loop in game, initialize all variables and gameState
    """
    p.init()
    screen = p.display.set_mode((HEIGHT, WIDTH))
    clock = p.time.Clock()
    screen.fill(p.Color("white"))
    game_state = ChessEngine.GameState()
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

                if square_selected == (row, column):
                    square_selected = ()
                    player_clicks = []
                else:
                    square_selected = (row, column)
                    player_clicks.append(square_selected)

                    if len(player_clicks) == 2:
                        move = ChessEngine.Move(player_clicks[0], player_clicks[1], game_state.board)
                        game_state.make_move(move)
                        square_selected = ()
                        player_clicks = []

        draw_game_state(screen, game_state)
        clock.tick(MAX_FPS)
        p.display.flip()


def draw_game_state(screen, game_state):
    """
    :param screen: p.screen
    :param game_state: GameState()
    :return:
    """
    draw_board(screen)
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


if __name__ == '__main__':
    main()
