"""
Classe responsável por guardar as informações do estado atual do jogo
Responsável por determinar os movimentos válidos.
Vai guardar os movimentos
"""


class GameState:
    """
    Class responsable for keeping up informations about the actual gameState
    Determine the valid moves
    Keep info about old moves
    """
    def __init__(self):
        """
        board: bidimensional list of strings which represent the board
        """
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
