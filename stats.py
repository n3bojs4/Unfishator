from operator import mod
import chess
import chess.pgn
import chess.engine

# Load Stockfish
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

# init chessboard
board = chess.Board()

# init counter
counter = 1
WhiteMoves = 0
BlackMoves = 0
WhitePoints = 0
BlackPoints = 0
depth = 15


print("Analyzing game with stockfish depth=",depth)


with open("test.pgn") as pgn:
    first_game = chess.pgn.read_game(pgn)


for move in first_game.mainline_moves():
    
    # Set new position
    board.push(move)

    # if first move we assume it's the best move
    if counter==1:
        WhiteNextBestMove = engine.play(board, chess.engine.Limit(depth=depth))
    
    # Black is playing
    if counter%2==0:
        print("Black played",move)
        print("stockfish recommend:",BlackNextBestMove.move)
        if str(move) in str(BlackNextBestMove):
            BlackPoints = BlackPoints+1
        BlackMoves = BlackMoves+1
        WhiteNextBestMove = engine.play(board, chess.engine.Limit(depth=depth))
    # White is playing
    else:
        print("White played",move)
        print("stockfish recommend:",WhiteNextBestMove.move)
        if str(move) in str(WhiteNextBestMove):
            WhitePoints = WhitePoints+1
        WhiteMoves = WhiteMoves+1
        BlackNextBestMove = engine.play(board, chess.engine.Limit(depth=depth))
    
    counter=counter+1

print("Game Informations")
print("-----------------")
print("Event:",first_game.headers["Event"])
print("White:",first_game.headers["White"])
print("Black:",first_game.headers["Black"])
print("Date:",first_game.headers["Date"])
print("Whitepoints=",WhitePoints)
print("Blackpoints=",BlackPoints)
print("Statistics of the game:")
print("Stockfish depth: ",depth)
print("White:",(WhitePoints/WhiteMoves)*100,"%")
print("Black:",(BlackPoints/BlackMoves)*100,"%")

engine.quit()

