#from operator import mod
import argparse
import chess
import chess.pgn
import chess.engine
import sys


# init chessboard
board = chess.Board()

# init array for storing games
ChessGames = []



parser = argparse.ArgumentParser(description='Analyze pgn file with stockfish.')
parser.add_argument('--depth',default=12,type=int, help='Stockfish depth to use.')
# to implement : arser.add_argument('--log',default='analyze.log',type=str, help='Reporting file path.')
parser.add_argument('--file',type=str, help='PGN file path to analyze.')
parser.add_argument('--debug',action='store_true', help='active debug mode.')

args = parser.parse_args()


if not (args.file): parser.error("Please give a pgn file with --file.")

depth = args.depth
pgnfile = args.file
debug = args.debug

# Load Stockfish
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

if debug:
    print("Analyzing game with stockfish depth=",depth)

try:
    with open(pgnfile) as pgn:
        while True:
            game = chess.pgn.read_game(pgn)
            ChessGames.append(game)
            if game is None:
                # We are at the end of the file and we delete the last list element which is None
                del ChessGames[-1]
                break
except:
    print("Cannot open pgn file:",pgnfile)
    sys.exit()

for games in ChessGames:

    # Reset board
    board.reset()

    # init counter
    counter = 1
    WhiteMoves = 0
    BlackMoves = 0
    WhitePoints = 0
    BlackPoints = 0


    for move in games.mainline_moves():
        # Set new position
        board.push(move)


        # if first move we assume it's the best move
        if counter==1:
            WhiteNextBestMove = engine.play(board, chess.engine.Limit(depth=depth))
    
        # Black is playing
        if counter%2==0:
            if debug:
                print("Black played",move)
                print("stockfish recommend:",BlackNextBestMove.move)
            if str(move) in str(BlackNextBestMove):
                BlackPoints = BlackPoints+1
            BlackMoves = BlackMoves+1
            WhiteNextBestMove = engine.play(board, chess.engine.Limit(depth=depth))
        # White is playing
        else:
            if debug:
                print("White played",move)
                print("stockfish recommend:",WhiteNextBestMove.move)
            if str(move) in str(WhiteNextBestMove):
                WhitePoints = WhitePoints+1
            WhiteMoves = WhiteMoves+1
            BlackNextBestMove = engine.play(board, chess.engine.Limit(depth=depth))
    
        counter=counter+1

    print("Game Informations")
    print("-----------------")
    print("Event:",games.headers["Event"])
    print("White:",games.headers["White"])
    print("Black:",games.headers["Black"])
    print("Date:",games.headers["Date"])
    print("Whitepoints=",WhitePoints)
    print("Blackpoints=",BlackPoints)
    print("Statistics of the game:")
    print("Stockfish depth: ",depth)
    print("White:",round((WhitePoints/WhiteMoves)*100,2),"%")
    print("Black:",round((BlackPoints/BlackMoves)*100,2),"%")

engine.quit()

