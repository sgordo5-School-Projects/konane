# This is a Python3 class file, for a class named Konane.
#
# One Konane object contains one player's information in a Konane game.
#
# This is the human player. It gets its move from the keyboard. 
#
import sys

#  Prompt the user for a board location (e.g. '3d'), and
#  keep prompting until the user types a valid location.
#
#  Type a simple <enter> to bail out.
#
#  Inputs:  prompt     a prompt string
#           sqcontain  what the square should contain
#
#  Returns  row, col
#
def get_move_from_command_line(player, board):
    # Get the From position.
    while True:
        from_row, from_col, err = get_move_from_command_line1("From: ", player, board)
        if err=='q': sys.exit(0)
        if err:
            print('From: (q to quit) ')
            continue
        # Get the To position
        while True:
            to_row, to_col, err = get_move_from_command_line1("To: ", " ", board)
            if err=='z': break  # Break back to From-loop
            if err=='q': sys.exit(0)
            if err:
                print('To: (z=try again, q=quit) ')
                continue
            if not err: return (from_row, from_col, to_row, to_col)

def get_move_from_command_line1(prompt, sqcontain, board):
    while 1:
        s = input(prompt).strip().lower()
        if s in ('q', 'quit'): return (None, None, 'q')
        if s in ('z'): return (None, None, 'z')
        if not len(s) == 2: return (None, None, 'lenerr')
        s1 = s[0]
        s2 = s[1]
        if s1.isalpha() and s2.isdigit():
            s2, s1 = s1, s2
        elif not s1.isdigit() and s2.isalpha():
            continue
        if not ('0' <= s1 and s1 <= '7'):
            continue
        if not ('a' <= s2 and s2 <= 'h'):
            continue
        row = int(s1)
        col = 'abcdefgh'.index(s2)
        if not board[row][col] == sqcontain:    
            print("Square should contain ",
                  'blank' if sqcontain==' ' else sqcontain)
            continue
        return (row, col, False)
    

#------------------------------------------------------------------------
#  Constructor:  K = Konane(board, who)
#
#  At initialization, save the initial state of the game, plus
#  some other useful information.  The class variables are:
#
#    board = game board, a list of lists. See the documentation.
#    who = the current player 'o' or 'x'
#    other = the other player 'x' or 'o'
#    human = boolean indicating this is a human player.
#
#  Notice that "self.vbl" is the Python way of creating and accessing
#  a class variable.
#
import random
import konaneutils as U

class Konane:
    def __init__(self, board, who):
        self.board = board   # Pointer to the board (in the main program)
        self.who = who
        self.other = {'x':'o', 'o':'x'}[who]
        self.human = True
  
    #---------------end of constructor------------------


    #--------method move() makes one move for this player.
    #
    #
    def move(self):
       mymove =  get_move_from_command_line(self.who, self.board)
       return mymove

 
