"""
Classe responsável por guardar as informações do estado atual do jogo
Responsável por determinar os movimentos válidos.
Vai guardar os movimentos
"""


class GameState():
    def __init__(self):
        # board lista bidimensional 8x8,
        # primeira letra a cor "b" ou "w"
        # segunda o tipo da peça "R", "N", "B", "Q", "K" ou "P"
        # "--" lugar vazio
        self.board = [
            ["bR", "bN", "bB", "bQ", "bK", "bB", "bN", "bR"],
            ["bP", "bP", "bP", "bP", "bP", "bP", "bP", "bP"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--"],
            ["wP", "wP", "wP", "wP", "wP", "wP", "wP", "wP"],
            ["wR", "wN", "wB", "wQ", "wK", "wB", "wN", "wR"],
        ]

        self.white_to_move = True
