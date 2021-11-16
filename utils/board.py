import chess
import numpy as np

class RunningGameError(Exception):
    def __init__(self, *args: object) -> None:
        super().__init__(*args)


class Board():
    def __init__(self) -> None:
        self.board = None
        self.white_turn = True
        self.winner = None

    @property
    def legal_moves(self):
        pass

    def push(self, action:tuple):
        pass

    def result(self):
        if not self.is_game_over():
            raise RunningGameError("The game is still running")

        return self.winner if self.winner else '1/2-1/2'

    def is_game_over(self):
        pass

    def outcome(self):
        color = chess.WHITE if self.winner == 'X' else chess.BLACK if self.winner == 'O' else None
        return chess.Outcome(termination='win' if color else 'draw', winner=color)



class TicTacToeBoard(Board):
    def __init__(self) -> None:
        super().__init__()
        self.board = np.asarray([['-','-','-'],
                                 ['-','-','-'],
                                 ['-','-','-']])
        self.columns = 3
        self.rows = 3

    @property
    def legal_moves(self):
        moves = []
        for i in range(self.rows):
            for j in range(self.columns):
                if self.board[i][j] == '-':
                    moves.append((i,j))
        return moves

    def push(self, action:tuple, simulate=False):
        (r, c) = action
        if r > self.rows or c > self.columns:
            raise ValueError(f'Row and column values mst be between 0 and {self.columns-1}, not {r, c}.')
        if not self.board[r][c] == '-':
            raise ValueError("The cell is not empty")

        if not simulate:
            self.board[r][c] = 'X' if self.white_turn else 'O'
            self.white_turn = not self.white_turn

    def __str__(self) -> str:
        return self.__repr__()

    def __repr__(self) -> str:
        repr = '  '
        for i in range(self.columns):
            repr += f'{i}'
            repr += '\n' if i == (self.columns - 1) else ' '

        for i in range(self.rows):
            repr += f'{i} '
            for j in range(self.columns):
                repr += self.board[i][j] + " "
            repr += '\n'
        return repr

    def is_game_over(self):
        tmp = self.board.T

        # Check columns and rows
        for i in range(3):
            if self.board[i][0] in ['X', 'O']:
                if all(tmp[i] == self.board[i][0]) or all(self.board[i] == self.board[i][0]):
                    self.winner = self.board[i][0]
                    return True

        # Check diagonals
        if all(self.board.diagonal() == self.board[0][0]) and self.board[0][0] in ['X', 'O']:
            self.winner = self.board[0][0]
            return True
        if all(np.fliplr(self.board).diagonal() == self.board[0][2]) and self.board[0][2] in ['X', 'O']:
            self.winner = self.board[0][2]
            return True

        if not '-' in self.board:
            self.winner = None
            return True
        return False


class Connect4Board(TicTacToeBoard):
    def __init__(self) -> None:
        super().__init__()
        self.rows = 6
        self.columns = 7
        self.board = np.asarray([["-"] * self.columns] * self.rows)

    @property
    def legal_moves(self):
        tmp = self.board.T
        moves = []
        for i, c in enumerate(tmp):
            if '-' in c:
                moves.append(i)
        return moves

    def push(self, action:int, simulate=False):
        if action > self.columns:
            raise ValueError(f'Row and column values mst be between 0 and {self.columns-1}, not {action}.')

        for r in range(self.rows-1, -1, -1):
            if self.board[r][action] == '-':
                if not simulate:
                    self.board[r][action] = 'X' if self.white_turn else 'O'
                    self.white_turn = not self.white_turn
                return

        raise ValueError("The cell is not empty")

    def __repr__(self) -> str:
        repr = ''
        for i in range(self.columns):
            repr += f'{i}'
            repr += '\n' if i == (self.columns - 1) else ' '

        for i in range(self.rows):
            for j in range(self.columns):
                repr += self.board[i][j] + " "
            repr += '\n'
        return repr

    def is_game_over(self):
        # Check horizontal locations for win
        for c in range(self.columns - 3):
            for r in range(self.rows):
                if (self.board[r][c] != '-' and
                    self.board[r][c] == self.board[r][c+1] and
                    self.board[r][c+1] == self.board[r][c+2] and
                    self.board[r][c+2] == self.board[r][c+3]):

                    self.winner = self.board[r][c]
                    return True

        # Check vertical locations for win
        for c in range(self.columns):
            for r in range(self.rows - 3):
                if (self.board[r][c] != '-' and
                    self.board[r][c] == self.board[r+1][c] and
                    self.board[r+1][c] == self.board[r+2][c] and
                    self.board[r+2][c] == self.board[r+3][c]):

                    self.winner = self.board[r][c]
                    return True

        # Check positively sloped diaganols
        for c in range(self.columns - 3):
            for r in range(self.rows - 3):
                if (self.board[r][c] != '-' and
                    self.board[r][c] == self.board[r+1][c+1] and
                    self.board[r+1][c+1] == self.board[r+2][c+2] and
                    self.board[r+2][c+2] == self.board[r+3][c+3]):

                    self.winner = self.board[r][c]
                    return True

        # Check negatively sloped diaganols
        for c in range(self.columns - 3):
            for r in range(3, self.rows):
                if (self.board[r][c] != '-' and
                    self.board[r][c] == self.board[r-1][c+1] and
                    self.board[r-1][c+1] == self.board[r-2][c+2] and
                    self.board[r-2][c+2] == self.board[r-3][c+3]):

                    self.winner = self.board[r][c]
                    return True

        # Check if the board is full
        if not '-' in self.board:
            self.winner = None
            return True

        return False
