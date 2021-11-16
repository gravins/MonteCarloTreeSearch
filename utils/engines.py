import chess
import random
from . import check_game, available_games

class Engine():
    def __init__(self, name) -> None:
        self.name = name

    def play(self, board, **kargs):
        pass

    def quit(self):
        pass


class ChessEngine(Engine):
    def __init__(self, path, limit=chess.engine.Limit(time=0.1)) -> None:
        super().__init__(path)
        self.engine = chess.engine.SimpleEngine.popen_uci(path)
        self.limit = limit

    def play(self, board):
        return self.engine.play(board, self.limit).move

    def quit(self):
        self.engine.quit()


class RandomEngine(Engine):
    def __init__(self) -> None:
        super().__init__('Random')

    def play(self, board):
        moves = list(board.legal_moves)
        random.shuffle(moves)
        return moves[0]


class HumanEngine(Engine):
    def __init__(self, game) -> None:
        super().__init__('Human')
        check_game(game)
        self.game = game

    def play(self, board):
        good_value = False
        while not good_value:
            if self.game == available_games['chess']:
                move = input('move:')
                try:
                    move = board.parse_san(move)
                    good_value = True
                except ValueError:
                    print(f'{move} is not a valid move.')
                    continue
            elif self.game == available_games['tic tac toe']:
                try:
                    row = int(input("row:"))
                    col = int(input("column:"))

                    board.push((row,col), simulate=True)
                    good_value = True
                    move = (row, col)
                    continue

                except Exception as e:
                    print(e)
                print('Insert the values again')
            else:
                try:
                    col = int(input("column:"))

                    board.push(col, simulate=True)
                    good_value = True
                    move = col
                    continue

                except Exception as e:
                    print(e)
                    print('Insert the values again')

        return move
