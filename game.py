from utils.board import Connect4Board, TicTacToeBoard
import chess.engine
from utils import *
import argparse
import datetime
import random
import chess
import math
import time


def game():

    parser = argparse.ArgumentParser()
    parser.add_argument('--game', help='type of game: chess, tic_tac_toe, or connect4', type=str, required=True)
    parser.add_argument('--engine', help='used engine: Human, Random, <executable chess engine path>', type=str, default='Random', required=True)
    parser.add_argument('--simul', help='number of simulations for the Monte Carlo Tree Search, default=200', type=int, default=200)
    parser.add_argument('--const', help='exploration parameter C of the Monte Carlo Tree Search, default=math.sqrt(2)', type=float, default=math.sqrt(2))
    parser.add_argument('--path', help='path used to save the game', type=str, default=None)
    parser.add_argument('--time', help="print time information, default=False", action='store_true')
    args = parser.parse_args()

    check_game(args.game)

    if args.game == available_games['chess'] and args.engine not in ['Human', 'Random']:
        engine = ChessEngine(args.engine)
    elif args.engine == 'Human':
        engine = HumanEngine(args.game)
    elif args.engine == 'Random':
        engine = RandomEngine()
    else:
        raise ValueError(f'The used engine must be Human, Random, or <chess engine path>, not {args.engine}')

    game = GameSaver(args.game)
    game.headers['Event'] = 'Example'
    game.headers['Date'] = datetime.datetime.today().strftime('%Y-%m-%d-%H:%M:%S')

    if random.random() > 0.5:
        white = Player('white', engine)
        game.headers['White'] = engine.name

        black = Player('black', n_simulations=args.simul, c=args.const)
        game.headers['Black'] = 'MCTS'

    else:
        white = Player('white', n_simulations=args.simul, c=args.const)
        game.headers['White'] = 'MCTS'
        black = Player('black', engine)
        game.headers['Black'] = engine.name

    if args.game == available_games['chess']:
        board = chess.Board()
    elif args.game == available_games['tic tac toe']:
        board = TicTacToeBoard()
    else:
        board = Connect4Board()

    white_turn = True

    print(f'{args.game}, MCTS param: c:{args.const}, simul:{args.simul}')
    p1 = 'White' if args.game == available_games['chess'] else 'X'
    p2 = 'Black' if args.game == available_games['chess'] else 'O'
    print(f"{p1}: {game.headers['White']}, {p2}: {game.headers['Black']}")
    print()
    print('-- Initial State --')
    print(board, '\n\n')

    start = time.time()
    while not board.is_game_over():
        elapsed = time.time()
        if white_turn:
            move = white.play(board)
        else:
            move = black.play(board)
        elapsed = time.time() - elapsed

        print(f"{game.headers['White'] if white_turn else game.headers['Black']}'s move: {move}")
        if args.time:
            print(f'Move computed in {datetime.timedelta(seconds=elapsed)} seconds')

        white_turn = not white_turn
        board.push(move)
        game.add_action(move, board, elapsed)

        print(board, '\n\n')
        print(f"{p1 if white_turn else p2}'s turn")

    game.headers["Result"] = board.result()

    if game.headers["Result"] == '1/2-1/2':
        print('Draw')
    else:
        print(f'The winner is {game.headers["Result"]}')

    if args.path is not None:
        game.save(args.path)

    engine.quit()

    seconds = time.time() - start
    if args.time:
        print(f'{args.game}, C:{args.const}, simul:{args.simul} - took {datetime.timedelta(seconds=seconds)}')



if __name__ == "__main__":
    game()
