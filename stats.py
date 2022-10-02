#from operator import mod
import argparse
import chess
import chess.pgn
import chess.engine
import json
import sys


# init chessboard
board = chess.Board()

# init array for storing games
ChessGames = []



def OutputAsJson(chessgame,WhitePoints,BlackPoints,WhiteMoves,BlackMoves):
    Event = chessgame.headers["Event"]
    Site = chessgame.headers["Site"]
    Date = chessgame.headers["Date"]
    EventRound = int(chessgame.headers["Round"])
    WhitePlayer = chessgame.headers["White"]
    BlackPlayer = chessgame.headers["Black"]
    WhiteElo = int(chessgame.headers["WhiteElo"])
    BlackElo = int(chessgame.headers["BlackElo"])
    PlyCount = int(chessgame.headers["PlyCount"])
    WhitePrecision = round((WhitePoints/WhiteMoves)*100,2)
    BlackPrecision = round((BlackPoints/BlackMoves)*100,2)


    # We create the dictionnary
    GameRecord = {
        "Event": Event,
        "Site": Site,
        "Date": Date,
        "Round": EventRound,
        "White": WhitePlayer,
        "Black": BlackPlayer,
        "WhiteElo": WhiteElo,
        "BlackElo": BlackElo,
        "PlyCount": PlyCount,
        "WhitePrecision": WhitePrecision,
        "BlackPrecision": BlackPrecision,
        "StockFishDepth": depth }
    # Serializing json
    json_game = json.dumps(GameRecord, indent=4)    

    print(json_game)

def OutputAsTxt(chessgame,WhitePoints,BlackPoints,WhiteMoves,BlackMoves):
    Event = chessgame.headers["Event"]
    Site = chessgame.headers["Site"]
    Date = chessgame.headers["Date"]
    EventRound = int(chessgame.headers["Round"])
    WhitePlayer = chessgame.headers["White"]
    BlackPlayer = chessgame.headers["Black"]
    WhiteElo = int(chessgame.headers["WhiteElo"])
    BlackElo = int(chessgame.headers["BlackElo"])
    PlyCount = int(chessgame.headers["PlyCount"])
    WhitePrecision = round((WhitePoints/WhiteMoves)*100,2)
    BlackPrecision = round((BlackPoints/BlackMoves)*100,2)

    if (WhiteMoves+BlackMoves)==PlyCount:
        print("Game Informations")
        print("-----------------------")
        print("Event:",Event)
        print("Site:",Site)
        print("Date:",Date)
        print("Round:",EventRound)
        print("White:",WhitePlayer)
        print("Black:",chessgame.headers["Black"])
        print("Date:",chessgame.headers["Date"])
        print("White ELO:",WhiteElo)
        print("Black ELO:",BlackElo)
        print("Moved Played:",PlyCount)
        print("Whitepoints=",WhitePoints)
        print("Blackpoints=",BlackPoints)
        print("Statistics of the game:")
        print("Stockfish depth: ",depth)
        print("White precision:",WhitePrecision,"%")
        print("Black precision:",BlackPrecision,"%")
        print("-----------------------")
        print(" ")
    else:
        print("Error, the number of calculated moves is not good!")





parser = argparse.ArgumentParser(description='Analyze pgn file with stockfish.')
parser.add_argument('--depth',default=12,type=int, help='Stockfish depth to use.')
# to implement : parser.add_argument('--log',default='analyze.log',type=str, help='Reporting file path.')
parser.add_argument('--file',type=str, help='PGN file path to analyze.')
parser.add_argument('--format',type=str, help='format for output: txt,json.')
parser.add_argument('--debug',action='store_true', help='active debug mode.')

args = parser.parse_args()


if not (args.file): parser.error("Please give a pgn file with --file.")

depth = args.depth
pgnfile = args.file
debug = args.debug
format = args.format


# Load Stockfish
engine = chess.engine.SimpleEngine.popen_uci("stockfish")

if debug:
    print("Analyzing game with stockfish depth=",depth)

try:
    with open(pgnfile) as pgn:
        while True:
            Round = chess.pgn.read_game(pgn)
            ChessGames.append(Round)
            if Round is None:
                # We are at the end of the file and we delete the last list element which is None
                del ChessGames[-1]
                break
except:
    print("Cannot open pgn file:",pgnfile)
    sys.exit()

for game in ChessGames:

    # Reset board
    board.reset()

    # init counter
    counter = 1
    WhiteMoves = 0
    BlackMoves = 0
    WhitePoints = 0
    BlackPoints = 0


    for move in game.mainline_moves():
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
    if "txt" in format:
        OutputAsTxt(game,WhitePoints,BlackPoints,WhiteMoves,BlackMoves)
    if "json" in format:
        OutputAsJson(game,WhitePoints,BlackPoints,WhiteMoves,BlackMoves)

engine.quit()

