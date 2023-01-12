import chess
import importlib
import math
import random
from stockfish import Stockfish
stockfish = Stockfish(r"C:\Users\deepp\Desktop\stockfish_15_win_x64_avx2\stockfish_15_win_x64_avx2\stockfish_15_x64_avx2.exe")
# stockfish.set_elo_rating(200)
# stockfish.set_depth(1)
stockfish.set_skill_level(1)
white_depth = 2
black_depth = 2
matches = int(input("Number of matches: "))
white = input("White AI: ")
black = input("Black AI: ")
white_ai_wins = 0
black_ai_wins = 0
draws = 0
if white == "Stockfish":
    black_ai = importlib.import_module(black)
    for i in range(matches):
        stockfish.set_position([])
        board = chess.Board()
        transposition = {}
        transposition[str(board)] = 1
        white_to_move = True
        while (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()) == False:
            if(white_to_move==True):
                next_move = stockfish.get_best_move(500)
                stockfish.make_moves_from_current_position([next_move])
                print(next_move)
                print("\n")
                black_ai.make_move(board, str(next_move))
                print(board)
                transposition[str(board)]=1
                white_to_move = False
            else:
                next_move = black_ai.search(board, black_depth)
                print(next_move)
                print("\n")
                black_ai.make_move(board, str(next_move))
                print(board)
                if str(board) in transposition:
                    board.pop()
                    moves = list(board.legal_moves)
                    rand_idx = random.randrange(len(moves))
                    next_move = moves[rand_idx]
                    black_ai.make_move(board, str(next_move))
                transposition[str(board)]=1
                stockfish.make_moves_from_current_position([str(next_move)])
                white_to_move = True
        if(board.is_checkmate()):
            if(white_to_move):
                black_ai_wins+=1
                print("Black Wins")
            else:
                white_ai_wins+=1
                print("White Wins")
        else:
            draws+=1
            print("Draw")
        #do
elif black == "Stockfish":
    white_ai = importlib.import_module(white)
    for i in range(matches):
        stockfish.set_position([])
        board = chess.Board()
        transposition = {}
        transposition[str(board)]=1
        white_to_move = True
        while (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()) == False:
            if(white_to_move==False):
                next_move = stockfish.get_best_move(500)
                stockfish.make_moves_from_current_position([next_move])
                print(next_move)
                print("\n")
                white_ai.make_move(board, str(next_move))
                print(board)
                transposition[str(board)]=1
                white_to_move = True
            else:
                next_move = white_ai.search(board, white_depth)
                print(next_move)
                print("\n")
                white_ai.make_move(board, str(next_move))
                print(board)
                if str(board) in transposition:
                    board.pop()
                    moves = list(board.legal_moves)
                    rand_idx = random.randrange(len(moves))
                    next_move = moves[rand_idx]
                    white_ai.make_move(board, str(next_move))
                transposition[str(board)]=1
                stockfish.make_moves_from_current_position([str(next_move)])
                white_to_move = False
        if(board.is_checkmate()):
            if(white_to_move):
                black_ai_wins+=1
                print("Black Wins")
            else:
                white_ai_wins+=1
                print("White Wins")
        else:
            draws+=1
            print("Draw")
    #rem
else:
    white_ai = importlib.import_module(white)
    black_ai = importlib.import_module(black)
    for i in range(matches):
        board = chess.Board()
        transposition = {}
        transposition[str(board)] = 1
        white_to_move = True
        while (board.is_checkmate() or board.is_stalemate() or board.is_insufficient_material()) == False:
            if(white_to_move==True):
                next_move = white_ai.search(board, white_depth)
                print(next_move)
                print("\n")
                white_ai.make_move(board, str(next_move))
                print(board)
                if str(board) in transposition:
                    board.pop()
                    moves = list(board.legal_moves)
                    rand_idx = random.randrange(len(moves))
                    white_ai.make_move(board, str(moves[rand_idx]))
                transposition[str(board)]=1
                white_to_move = False
            else:
                # print("****************************************************")
                next_move = black_ai.search(board, black_depth)
                print(next_move)
                print("\n")
                black_ai.make_move(board, str(next_move))
                print(board)
                if str(board) in transposition:
                    board.pop()
                    moves = list(board.legal_moves)
                    rand_idx = random.randrange(len(moves))
                    black_ai.make_move(board, str(moves[rand_idx]))
                transposition[str(board)]=1
                white_to_move = True
        if(board.is_checkmate()):
            if(white_to_move):
                black_ai_wins+=1
                print("Black Wins")
            else:
                white_ai_wins+=1
                print("White Wins")
        else:
            draws+=1
            print("Draw")
print("White wins: " + str(white_ai_wins))
print("Black wins: " + str(black_ai_wins))
print("Draws: " + str(draws))
