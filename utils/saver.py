import chess.pgn
import copy

available_games = {
    'chess': 'chess',
    'tic_tac_toe': 'tic_tac_toe',
    'tic tac toe': 'tic_tac_toe',
    'connect4': 'connect4'
}

def check_game(game):
    if not game in available_games.keys():
        raise NotImplementedError(f'The game {game} is not implemented yet. The available games are {" ".join(available_games.keys())}')


class GameSaver():
    def __init__(self, game) -> None:
        check_game(game)

        self.headers = chess.pgn.Headers()
        if game == 'chess':
            self.game = chess.pgn.Game()
            self.history = self.game
        else:
            self.game = None
            self.history = []

    def add_action(self, action, board, elapsed):
        if self.game:
            self.history = self.history.add_variation(action)
            self.history.comment = str(elapsed)
        else:
            self.history.append((action, copy.deepcopy(board), elapsed))

    def save(self, filename):
        if self.game:
            self.game.headers = self.headers
            print(self.game, file=open(f"{filename}.pgn", "w"), end="\n\n")
        else:
            with open(f"{filename}.pgn", "w") as f:
                f.write(f'{self.headers}\n')
                f.flush()
                for (action, board, elapsed) in self.history:
                    f.write(f'Action: {action}, required time: {elapsed}\n')
                    f.flush()
                    f.write(board.__str__())
                    f.flush()
                f.close()


