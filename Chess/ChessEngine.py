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

        self.move_functions = {
            'P': self.get_pawn_moves,
            'R': self.get_rook_moves,
            'N': self.get_knight_moves,
            'K': self.get_king_moves,
            'Q': self.get_queen_moves,
            'B': self.get_bishop_moves,
        }

        self.move_log = []
        self.white_turn = True

        self.white_king = (7, 4)
        self.black_king = (0, 4)

        self.check_mate = False
        self.stale_mate = False

    def make_move(self, move):
        self.board[move.start_row][move.start_column] = "--"
        self.board[move.end_row][move.end_column] = move.piece_moved
        self.move_log.append(move)
        self.white_turn = not self.white_turn

        # Update kings location
        if move.piece_moved == "wK":
            self.white_king = (move.end_row, move.end_column)
        elif move.piece_moved == "bK":
            self.black_king = (move.end_row, move.end_column)

    def rollback_move(self):
        if len(self.move_log) != 0:
            last_move = self.move_log.pop()
            self.board[last_move.end_row][last_move.end_column] = last_move.piece_captured
            self.board[last_move.start_row][last_move.start_column] = last_move.piece_moved
            self.white_turn = not self.white_turn

            # Updates kings position
            if last_move.piece_moved == "wK":
                self.white_king = (last_move.start_row, last_move.start_column)
            elif last_move.piece_moved == "bK":
                self.black_king = (last_move.start_row, last_move.start_column)

    def get_valid_moves(self):
        # generate all possible moves
        moves = self.get_all_possible_moves()
        # for each move make move
        for move in moves[::-1]:
            self.make_move(move)
            self.white_turn = not self.white_turn
            if self.in_check():
                moves.remove(move)

            # Undo stuff
            self.white_turn = not self.white_turn
            self.rollback_move()

        if len(moves) == 0:
            if self.in_check():
                self.check_mate = True
            else:
                self.stale_mate = True
        else:
            self.check_mate = self.stale_mate = False
        return moves

    def in_check(self):
        """
        Determine if the current player is in check
        :return: boolean
        """
        if self.white_turn:
            return self.square_under_attack(self.white_king[0], self.white_king[1])
        else:
            return self.square_under_attack(self.black_king[0], self.black_king[1])


    def square_under_attack(self, row, column):
        """
        Determine if the enemy can attack square (row, column)
        :param row: int
        :param column: int
        :return: boolean
        """
        self.white_turn = not self.white_turn
        opponent_moves = self.get_all_possible_moves()
        self.white_turn = not self.white_turn
        for move in opponent_moves:
            if move.end_row == row and move.end_column == column:
                return True
        return False

    def get_all_possible_moves(self):
        possible_moves = []
        for row in range(len(self.board)):
            for column in range(len(self.board[row])):
                turn = self.board[row][column][0]
                if (turn == "w" and self.white_turn) or (turn == "b" and not self.white_turn):
                    piece = self.board[row][column][1]
                    self.move_functions[piece](row, column, possible_moves)

        return possible_moves

    def get_pawn_moves(self, row, column, moves):
        """
        Check for possible moves for a pawn
        :param row: int
        :param column: int
        :param moves: list of moves which will append possible moves
        :return: void
        """
        # White moves
        if self.white_turn:
            # Front + 1
            if row != 0:
                if self.board[row - 1][column] == "--":
                    moves.append(Move((row, column), (row - 1, column), self.board))
                    # Front + 2
                    if row == 6 and self.board[row - 2][column] == "--":
                        moves.append(Move((row, column), (row - 2, column), self.board))
                # Left capture
                if column - 1 >= 0:
                    # Check if other piece is from black
                    if self.board[row - 1][column - 1][0] == "b":
                        moves.append(Move((row, column), (row - 1, column - 1), self.board))
                # Right capture
                if column + 1 <= 7:
                    # Check if other piece is from black
                    if self.board[row - 1][column + 1][0] == "b":
                        moves.append(Move((row, column), (row - 1, column + 1), self.board))
        # Black moves
        else:
            # Front + 1
            if row != 7:
                if self.board[row + 1][column] == "--":
                    moves.append(Move((row, column), (row + 1, column), self.board))
                    # Front + 2
                    if row == 1 and self.board[row + 2][column] == "--":
                        moves.append(Move((row, column), (row + 2, column), self.board))
                # Left capture
                if column - 1 >= 0:
                    # Check if other piece is from black
                    if self.board[row + 1][column - 1][0] == "w":
                        moves.append(Move((row, column), (row + 1, column - 1), self.board))
                # Right capture
                if column + 1 <= 7:
                    # Check if other piece is from black
                    if self.board[row + 1][column + 1][0] == "w":
                        moves.append(Move((row, column), (row + 1, column + 1), self.board))

    def get_rook_moves(self, row, column, moves):
        """
        Get all possible rookies move
        :param row: int
        :param column: int
        :param moves: list of moves which will append possible moves
        :return: void
        """
        # Possible moves
        directions = ((-1, 0), (1, 0), (0, -1), (0, 1))
        enemy_color = "b" if self.white_turn else "w"

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == "--":
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    # Find an enemy piece end
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    # Find an ally piece end
                    else:
                        break
                # End of board
                else:
                    break

    def get_bishop_moves(self, row, column, moves):
        """
        Get all possible bishops moves
        :param row: int
        :param column: int
        :param moves: list of moves which will append possible moves
        :return: void
        """
        directions = ((-1, -1), (1, 1), (1, -1), (-1, 1))
        enemy_color = "b" if self.white_turn else "w"

        for direction in directions:
            for i in range(1, 8):
                end_row = row + direction[0] * i
                end_column = column + direction[1] * i
                if 0 <= end_row <= 7 and 0 <= end_column <= 7:
                    end_piece = self.board[end_row][end_column]
                    if end_piece == "--":
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                    # Find an enemy piece end
                    elif end_piece[0] == enemy_color:
                        moves.append(Move((row, column), (end_row, end_column), self.board))
                        break
                    # Find an ally piece end
                    else:
                        break
                # End of board
                else:
                    break

    def get_knight_moves(self, row, column, moves):
        x_move = [2, 1, -1, -2, -2, -1, 1, 2]
        y_move = [1, 2, 2, 1, -1, -2, -2, -1]

        color = self.board[row][column][0]

        for knight_move in range(8):
            new_column = column + x_move[knight_move]
            new_row = row + y_move[knight_move]

            if 0 <= new_column <= 7 and 0 <= new_row <= 7:
                if self.board[new_row][new_column][0] != color:
                    moves.append(Move((row, column), (new_row, new_column), self.board))

    def get_queen_moves(self, row, column, moves):
        """
        Get all possible moves for the queen
        :param row:
        :param column:
        :param moves:
        :return:
        """
        self.get_rook_moves(row, column, moves)
        self.get_bishop_moves(row, column, moves)

    def get_king_moves(self, row, column, moves):
        """
        Get all possible moves for kings
        :param row:
        :param column:
        :param moves:
        :return:
        """
        color = self.board[row][column][0]
        king_moves = ((1, 1), (1, 0), (0, 1), (-1, 1), (-1, -1), (1, -1), (0, -1), (-1, 0))
        for move in king_moves:
            new_row = row + move[0]
            new_column = column + move[1]

            if 0 <= new_row <= 7 and 0 <= new_column <= 7:
                if self.board[new_row][new_column][0] != color:
                    moves.append(Move((row, column), (new_row, new_column), self.board))


class Move:
    ranks_to_rows = {
        "1": 7,
        "2": 6,
        "3": 5,
        "4": 4,
        "5": 3,
        "6": 2,
        "7": 1,
        "8": 0,
    }

    rows_to_ranks = {v: k for k, v in ranks_to_rows.items()}

    files_to_columns = {
        "a": 0,
        "b": 1,
        "c": 2,
        "d": 3,
        "e": 4,
        "f": 5,
        "g": 6,
        "h": 7,
    }

    columns_to_files = {v: k for k, v in files_to_columns.items()}

    def __init__(self, start_square, end_square, board):
        self.start_row = start_square[0]
        self.start_column = start_square[1]
        self.end_row = end_square[0]
        self.end_column = end_square[1]
        self.piece_moved = board[self.start_row][self.start_column]
        self.piece_captured = board[self.end_row][self.end_column]
        self.move_ID = self.start_row * 1000 + self.start_column * 100 + self.end_row * 10 + self.end_column;

    def __eq__(self, other):
        if isinstance(other, Move):
            return self.move_ID == other.move_ID
        return False

    def get_chess_notation(self):
        return self.get_rank_file(self.start_row, self.start_column) + self.get_rank_file(self.end_row, self.end_column)

    def get_rank_file(self, row, column):
        return self.columns_to_files[column] + self.rows_to_ranks[row]
