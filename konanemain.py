#!/bin/env python3
#
# Konane main program: human vs. computer or computer vs. computer.
#
# Usage:  ./konanemain player.py               # you vs. machine player
#    or   ./konanemain player1.py player2.py  # two machine players
#
#
#  It will load the player modules and play them against each other.
#
#  The module for you the human player is named you.py
#
import sys
import os.path
import konaneutils as U

#------------------------------------------------------------------------
#  Utility Functions for printing moves (and verifying legality first)
#------------------------------------------------------------------------
# 
#  encode_move  Turns a 4-tuple (4 numbers) into printable move 
#  
def encode_move(from_row, from_col, to_row, to_col):
    if not (0 <= from_row and from_row <= 7 and
            0 <= to_row and to_row <= 7 and
            0 <= from_col and from_col <= 7 and
            0 <= to_col and to_col <= 7):
        print("Illegal move from=(%d,%d) to=(%d,%d)" % \
               (from_row, from_col, to_row, to_col))
        sys.exit(1)
    else:
        return str(from_row) + 'abcdefgh'[from_col] + ' ' + \
               str(to_row)  + 'abcdefgh'[to_col]

#  Place the move on the board.  Return None if move is not possible.
#  If the move is possible, the board is modified.
#
#  Inputs are:
#     board
#     sq       the player in question, 'x' or 'o'
#     othersq  the player being jumped over
#     from_row
#     from_col
#     to_row
#     to_col
#
#  make_move leaves . (dot) in place of the removed pieces, and
#  capitalizes the moved piece for emphasis.  cleanup_move() is
#  called to clean this stuff up after printing.
#
def make_move(board, sq, othersq, from_row, from_col, to_row, to_col):
    if not board[from_row][from_col] == sq: return None
    if not board[to_row][to_col] == ' ': return None
    (jump_over, jump_land) = jumppath(from_row, from_col, to_row, to_col)
    if not jump_over: return None
    for i,j in jump_over:
        if not board[i][j] == othersq: return None
    for i,j in jump_land:
        if not board[i][j] == ' ': return None
    for i,j in jump_over:
        board[i][j] = '.'
    for i,j in jump_land:
        board[i][j] = '.'
    board[to_row][to_col] = sq.capitalize()
    board[from_row][from_col] = '.'
    return 1

#  Cleanup_move cleans out the emphasis characters left by make_move
#
def cleanup_move(b):
    for i in range(len(b)):
        for j in range(len(b[i])):
            char = b[i][j]
            if char == '.' or char == '*':
                b[i][j] = ' '
            else:
                b[i][j] = b[i][j].lower()

#  Compute the squares being jumped over in a proposed move.
#  Returns two lists:
#    (i,j) tuples of the jumped-over positions.
#    (i,j) tuples of the intermediate landing positions
#
def jumppath(from_row, from_col, to_row, to_col):
    if from_row == to_row:
        jump_over = [(to_row, j) for j \
            in range(min(from_col, to_col)+1, max(from_col, to_col), 2)]
        jump_land = [(to_row, j) for j \
            in range(min(from_col, to_col)+2, max(from_col, to_col), 2)]
        return (jump_over, jump_land)
    elif from_col == to_col:
        jump_over = [(i, to_col) for i \
            in range(min(from_row, to_row)+1, max(from_row, to_row), 2)]
        jump_land = [(i, to_col) for i \
            in range(min(from_row, to_row)+2, max(from_row, to_row), 2)]
        return (jump_over, jump_land)

    else:
        return (None, None)


#  A simple function to print the board
#
def print_board(b):
    print('  a b c d e f g h')
    
    for i in range(len(b)):
        r = ' '.join(b[i])
        print(str(i) + ' ' + r)

#---------------------------------------------------------------------
# Utility functions for starting the game.
#---------------------------------------------------------------------

#  Populate the board before the start of the game
#
def populate_board():
    pieces = ['x', 'o']
    board = []
    polarity = 0
    for i in range(8):
        onerow = []
        for j in range(4):
            onerow.append(pieces[polarity])
            onerow.append(pieces[1-polarity])
        board.append(onerow)
        polarity = 1-polarity

    board[3][3] = ' '
    board[3][4] = ' '
    return board

# Load player module
#  
def getmodule(filename):
    modname, ext = os.path.splitext(filename)
    try:
        modul = __import__(modname)
    except ImportError:
        print("Cannot import", modname)
        sys.exit(0) 
    return modul

# ----------- MAIN PROGRAM STARTS HERE -------------------------------------
#
# load player module(s) from command line.
#
# If there was only one, the other player is 'you.py' human player.
#
nargs = len(sys.argv)
if nargs < 2 or nargs > 3:
    print("usage: ./konanemain playermodule.py [anotherplayer.py]")
    sys.exit(0)

mod2 = getmodule(sys.argv[1])
if nargs == 3:
    mod1 = getmodule(sys.argv[2])
else:
    mod1 = getmodule('you.py')

# Initialize board
board = populate_board()
O = mod2.Konane(board, 'o')
X = mod1.Konane(board, 'x')

# *** HERE WE PLAY, loop alternately x and o

player, other = ('o', 'x')          # Symbols
PLAYER, OTHER = (O, X)              # Modules
nmoves = 0
while 1:
    # Switch players
    player, other = other, player
    PLAYER, OTHER = OTHER, PLAYER
    
    U.print_board(board)
    cleanup_move(board)
    if U.gameDone(board, player): 
        break
    from_row, from_col, to_row, to_col = PLAYER.move()
    nmoves += 1
    print(player, "moves", encode_move(from_row, from_col, to_row, to_col))
    if not make_move(board, player, other, from_row, from_col, to_row, to_col):
        if X.human:
            print("Illegal Move, try again")
            continue
        else:
            print("Illegal move. Forfeit.")
            break


# When we break out of the loop the current player is the loser, because
# -- the current player had no moves (signaled by gameDdone(player)
# -- or the current player made an illegal move and forfeit
print("Winner after", nmoves, " moves is:", other)

