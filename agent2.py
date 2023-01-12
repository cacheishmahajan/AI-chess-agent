import random
import math
import chess
from collections import OrderedDict

#Weights
PAWN_WEIGHT = 10
QUEEN_WEIGHT = 90
ROOK_WEIGHT = 50
KNIGHT_WEIGHT = 32
BISHOP_WEIGHT = 33
ENDGAME_MATERIAL_START = 2*ROOK_WEIGHT + BISHOP_WEIGHT + KNIGHT_WEIGHT

# Make move
def make_move(state, string):
    move = chess.Move.from_uci(string)
    state.push(move)
    return

# Check for checkmate
def checkmate(state):
    if(state.is_checkmate()):
        if(state.turn):
            return -1000
        else:
            return 1000
    return 0

# Attacks by pieceson opponent pieces
def attacks(state):
    #Number of black pieces attacking white
    whiteAttacks = 0
    for i in state.pieces(chess.PAWN, chess.WHITE):
        whiteAttacks += PAWN_WEIGHT * len(state.attackers(chess.BLACK, i))
    for i in state.pieces(chess.ROOK, chess.WHITE):
        whiteAttacks += ROOK_WEIGHT * len(state.attackers(chess.BLACK, i))
    for i in state.pieces(chess.BISHOP, chess.WHITE):
        whiteAttacks += BISHOP_WEIGHT * len(state.attackers(chess.BLACK, i))
    for i in state.pieces(chess.KNIGHT, chess.WHITE):
        whiteAttacks += KNIGHT_WEIGHT * len(state.attackers(chess.BLACK, i))
    for i in state.pieces(chess.QUEEN, chess.WHITE):
        whiteAttacks += QUEEN_WEIGHT * len(state.attackers(chess.BLACK, i))

    #Number of white piece attacking black
    blackAttacks = 0
    for i in state.pieces(chess.PAWN, chess.BLACK):
        blackAttacks += PAWN_WEIGHT * len(state.attackers(chess.WHITE, i))
    for i in state.pieces(chess.ROOK, chess.BLACK):
        blackAttacks += ROOK_WEIGHT * len(state.attackers(chess.WHITE, i))
    for i in state.pieces(chess.BISHOP, chess.BLACK):
        blackAttacks += BISHOP_WEIGHT * len(state.attackers(chess.WHITE, i))
    for i in state.pieces(chess.KNIGHT, chess.BLACK):
        blackAttacks += KNIGHT_WEIGHT * len(state.attackers(chess.WHITE, i))
    for i in state.pieces(chess.QUEEN, chess.BLACK):
        blackAttacks += QUEEN_WEIGHT * len(state.attackers(chess.WHITE, i))

    return  (blackAttacks - whiteAttacks)

def piece_count(state):
    wp = len(state.pieces(chess.PAWN, chess.WHITE))
    bp = len(state.pieces(chess.PAWN, chess.BLACK))
    wn = len(state.pieces(chess.KNIGHT, chess.WHITE))
    bn = len(state.pieces(chess.KNIGHT, chess.BLACK))
    wb = len(state.pieces(chess.BISHOP, chess.WHITE))
    bb = len(state.pieces(chess.BISHOP, chess.BLACK))
    wr = len(state.pieces(chess.ROOK, chess.WHITE))
    br = len(state.pieces(chess.ROOK, chess.BLACK))
    wq = len(state.pieces(chess.QUEEN, chess.WHITE))
    bq = len(state.pieces(chess.QUEEN, chess.BLACK))

    return wp+bp+wn+bn+wb+bb+wr+br+wq+bq

# Material of a side
def material(state, s):
    if s == "WHITE":
        wp = len(state.pieces(chess.PAWN, chess.WHITE))
        wn = len(state.pieces(chess.KNIGHT, chess.WHITE))
        wb = len(state.pieces(chess.BISHOP, chess.WHITE))
        wr = len(state.pieces(chess.ROOK, chess.WHITE))
        wq = len(state.pieces(chess.QUEEN, chess.WHITE))
        return PAWN_WEIGHT * (wp) + KNIGHT_WEIGHT * (wn) + BISHOP_WEIGHT * (wb) + ROOK_WEIGHT * (wr) + QUEEN_WEIGHT * (wq)
    else:
        bp = len(state.pieces(chess.PAWN, chess.BLACK))
        bn = len(state.pieces(chess.KNIGHT, chess.BLACK))
        bb = len(state.pieces(chess.BISHOP, chess.BLACK))
        br = len(state.pieces(chess.ROOK, chess.BLACK))
        bq = len(state.pieces(chess.QUEEN, chess.BLACK))
        return PAWN_WEIGHT * (bp) + KNIGHT_WEIGHT * (bn) + BISHOP_WEIGHT * (bb) + ROOK_WEIGHT * (br) + QUEEN_WEIGHT * (bq)

def materialscore(state):
    return material(state, "WHITE") - material(state, "BLACK")

#Piece mobility
def piece_mob(state):
    pt = [
    0, 0, 0, 0, 0, 0, 0, 0,
    5, 10, 10, -20, -20, 10, 10, 5,
    5, -5, -10, 0, 0, -10, -5, 5,
    0, 0, 0, 20, 20, 0, 0, 0,
    5, 5, 10, 25, 25, 10, 5, 5,
    10, 10, 20, 30, 30, 20, 10, 10,
    50, 50, 50, 50, 50, 50, 50, 50,
    0, 0, 0, 0, 0, 0, 0, 0]

    nt = [
    -50, -40, -30, -30, -30, -30, -40, -50,
    -40, -20, 0, 5, 5, 0, -20, -40,
    -30, 5, 10, 15, 15, 10, 5, -30,
    -30, 0, 15, 20, 20, 15, 0, -30,
    -30, 5, 15, 20, 20, 15, 5, -30,
    -30, 0, 10, 15, 15, 10, 0, -30,
    -40, -20, 0, 0, 0, 0, -20, -40,
    -50, -40, -30, -30, -30, -30, -40, -50]

    bt = [
    -20, -10, -10, -10, -10, -10, -10, -20,
    -10, 5, 0, 0, 0, 0, 5, -10,
    -10, 10, 10, 10, 10, 10, 10, -10,
    -10, 0, 10, 10, 10, 10, 0, -10,
    -10, 5, 5, 10, 10, 5, 5, -10,
    -10, 0, 5, 10, 10, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -10, -10, -10, -10, -20]

    rt = [
    0, 0, 0, 5, 5, 0, 0, 0,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    -5, 0, 0, 0, 0, 0, 0, -5,
    5, 10, 10, 10, 10, 10, 10, 5,
    0, 0, 0, 0, 0, 0, 0, 0]

    qt = [
    -20, -10, -10, -5, -5, -10, -10, -20,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -10, 5, 5, 5, 5, 5, 0, -10,
    0, 0, 5, 5, 5, 5, 0, -5,
    -5, 0, 5, 5, 5, 5, 0, -5,
    -10, 0, 5, 5, 5, 5, 0, -10,
    -10, 0, 0, 0, 0, 0, 0, -10,
    -20, -10, -10, -5, -5, -10, -10, -20]

    kt = [
    20, 30, 10, 0, 0, 10, 30, 20,
    20, 20, 0, 0, 0, 0, 20, 20,
    -10, -20, -20, -20, -20, -20, -20, -10,
    -20, -30, -30, -40, -40, -30, -30, -20,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30,
    -30, -40, -40, -50, -50, -40, -40, -30]

    pawnsq = sum([pt[i] for i in state.pieces(chess.PAWN, chess.WHITE)])
    pawnsq = pawnsq + sum([-pt[chess.square_mirror(i)]
                        for i in state.pieces(chess.PAWN, chess.BLACK)])
    knightsq = sum([nt[i] for i in state.pieces(chess.KNIGHT, chess.WHITE)])
    knightsq = knightsq + sum([-nt[chess.square_mirror(i)]
                            for i in state.pieces(chess.KNIGHT, chess.BLACK)])
    bishopsq = sum([bt[i] for i in state.pieces(chess.BISHOP, chess.WHITE)])
    bishopsq = bishopsq + sum([-bt[chess.square_mirror(i)]
                            for i in state.pieces(chess.BISHOP, chess.BLACK)])
    rooksq = sum([rt[i] for i in state.pieces(chess.ROOK, chess.WHITE)])
    rooksq = rooksq + sum([-rt[chess.square_mirror(i)]
                        for i in state.pieces(chess.ROOK, chess.BLACK)])
    queensq = sum([qt[i] for i in state.pieces(chess.QUEEN, chess.WHITE)])
    queensq = queensq + sum([-qt[chess.square_mirror(i)]
                            for i in state.pieces(chess.QUEEN, chess.BLACK)])
    kingsq = sum([kt[i] for i in state.pieces(chess.KING, chess.WHITE)])
    kingsq = kingsq + sum([-kt[chess.square_mirror(i)]
                        for i in state.pieces(chess.KING, chess.BLACK)])
    return pawnsq + knightsq + bishopsq + rooksq + queensq + kingsq

def manhattanDist(i,j):
    return abs(i%8 - j%8) + abs(i/8 - j/8)

def centralManhattanDist(i):
    return min(manhattanDist(i,27), manhattanDist(i,28), manhattanDist(i,35),manhattanDist(i,36))

def endgamePhaseWeight(materialCountWithoutPawns):
    return 1 - min(1, materialCountWithoutPawns/ENDGAME_MATERIAL_START)

# k1 = MyKing
def endgameUtil(k1,k2,myMaterial, opponentMaterial, endgameWeight):
    mopUpScore = 0
    if(myMaterial > opponentMaterial + PAWN_WEIGHT*2 and endgameWeight > 0):
        # print("Please")
        mopUpScore += centralManhattanDist(k2)*10
        mopUpScore += (14 - manhattanDist(k1,k2))
    return mopUpScore

def utility(state):
    pieces = piece_count(state)
    whiteMaterial = material(state, "WHITE")
    blackMaterial = material(state, "BLACK")
    whiteMaterialWithoutPawns = whiteMaterial - len(state.pieces(chess.PAWN, chess.WHITE))*PAWN_WEIGHT
    blackMaterialWithoutPawns = blackMaterial - len(state.pieces(chess.PAWN, chess.BLACK))*PAWN_WEIGHT
    whiteEndgamePhaseWeight = endgamePhaseWeight(whiteMaterialWithoutPawns)
    blackEndgamePhaseWeight = endgamePhaseWeight(blackMaterialWithoutPawns)
    whiteKing = state.king(chess.WHITE)
    blackKing = state.king(chess.BLACK)
    whiteEndgameEval = endgameUtil(whiteKing, blackKing,whiteMaterial,blackMaterial,blackEndgamePhaseWeight)
    blackEndgameEval = endgameUtil(blackKing, whiteKing, blackMaterial, whiteMaterial, whiteEndgamePhaseWeight)
    weight = 1
    if pieces > 25:
        weight  = 1
    util = 1*(whiteMaterial - blackMaterial) + weight*piece_mob(state) + checkmate(state) + 1*attacks(state) + (whiteEndgameEval - blackEndgameEval)
    return util


def get_piece_value(piece):
    if piece == chess.PAWN:
        return PAWN_WEIGHT
    elif piece == chess.ROOK:
        return ROOK_WEIGHT
    elif piece == chess.KNIGHT:
        return KNIGHT_WEIGHT
    elif piece == chess.BISHOP:
        return BISHOP_WEIGHT
    elif piece == chess.QUEEN:
        return QUEEN_WEIGHT
    elif piece == chess.KING:
        return 1000
    elif piece == None:
        return 0

def evaluate_for_moveOrdering(state,move):
    eval = 0
    
    # capture opponent high value piece by our small value piece 
    # also promotion advantage taken care of
    
    initial_mat_score = materialscore(state)

    make_move(state,str(move))    
    eval = materialscore(state) - initial_mat_score
    state.pop()

    # If capture in the move, subtract piece value of the piece making capture
    if get_piece_value(state.piece_type_at(move.to_square)) > 0 :
        eval -= get_piece_value(state.piece_type_at(move.from_square))

    make_move(state,str(move))    
    eval += attacks(state)
    state.pop()

    return eval

def move_order(state,legalMoves):

    if(piece_count(state) > 25):
        return legalMoves
    legalMOvesDict = {}
   
    for move in legalMoves:
        # make evaluation
        evaluation = evaluate_for_moveOrdering(state,move)
        if evaluation not in legalMOvesDict:
            legalMOvesDict[evaluation] = list()
        legalMOvesDict[evaluation].extend([move])

    # Sort legalMovesDict in ascending order
    legalMOvesDict = OrderedDict(sorted(legalMOvesDict.items()))
    orderedMoves = []

    for move_list in legalMOvesDict.values():
        orderedMoves = orderedMoves + move_list

    if(state.turn == False):
        return orderedMoves
    #Return orderedMoves in reverse order
    return orderedMoves[::-1]

# Search

def search(state, depth):
    transposition = {}
    action = 0
    mini = -1 * math.inf
    maxi = math.inf
    # White to move
    if (state.turn):
        mx = -math.inf
        # Order Moves
        legal_moves_ordered = move_order(state,state.legal_moves)
        for move in legal_moves_ordered:
            make_move(state, str(move))
            min1 = minimum(state, depth - 1, mini, maxi, transposition)
            if (mx == -math.inf or min1 > mx):
                action = move
            elif(mini==mx):
                num = random.choice([0,1])
                if(num):
                    action = move
            mx = max(mx, min1)
            state.pop()

    # Black to move
    else:
        mn = math.inf
        # Order moves
        legal_moves_ordered = move_order(state,state.legal_moves)
        for move in legal_moves_ordered:
            make_move(state,str(move))
            max1 = maximum(state, depth - 1,mini,maxi, transposition)
            if (mn == math.inf or max1 < mn):
                action = move
            elif(max1 == mn):
                num = random.choice([0,1])
                if(num):
                    action = move
            mn = min(mn, max1)
            state.pop()

    return action


def maximum(state, depth,a,b, transposition):

    if state.is_stalemate():
        return 0

    if state.is_checkmate():
        return -math.inf

    if str(state) in transposition:
        return math.inf

    else:
        transposition[str(state)] = 1

    if (depth == 0):
        return utility(state)
    mx = -math.inf
    
    legal_moves_ordered = move_order(state,state.legal_moves)

    for move in legal_moves_ordered:
        make_move(state, str(move))
        mx = max(mx, minimum(state, depth - 1,a,b,transposition))
        if(mx>=b):
            state.pop()
            return mx
        a = max(a,mx)
        state.pop()
    return mx


def minimum(state, depth,a,b, transposition):

    if state.is_stalemate():
        return 0

    if state.is_checkmate():
        return math.inf

    if str(state) in transposition:
        return -math.inf

    else:
        transposition[str(state)] = 1

    if (depth == 0):
        return utility(state)
    mn = math.inf

    legal_moves_ordered = move_order(state,state.legal_moves)
    for move in legal_moves_ordered:
        make_move(state, str(move))

        mn = min(mn, maximum(state, depth - 1,a,b, transposition))
        if(mn <= a):
            state.pop()
            return mn
        b = min(b,mn)
        state.pop()
    return mn