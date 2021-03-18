# This is a Python3 class file, for a class named Konane.
#
# One Konane object contains one player's information in a Konane game.
#
# The 'move' method returns your move.  Put your code there!
#
# Notice the konaneutils module contains useful functions you can use.

import random
import konaneutils as U

#------------------------------------------------------------------------
#  Constructor:  K = Konane(board, who)
#
#  At initialization, save the initial state of the game, plus
#  some other useful information.  The class variables are:
#
#    board = game board, a list of lists. See the documentation.
#    who = the current player 'o' or 'x'
#    other = the other player 'x' or 'o'
#    human = boolean indicating this is not a human player.
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
        self.human = False  # Self-explanatory
        self.maxdepth = 1   # How deep can your tree search go
  
    #---------------end of constructor------------------


    #--------method move() makes one move for this player.
    #
    #  There are no arguments.
    #     The board variable contains the current state of the board
    #       (It was updated in the main program)
    #     The who variable contains which play we are
    #
    #  Example call from main program:
    #  fromrow, fromcol, torow, tocol = K.move()
    #
    #  This method returns a 4-tuple containing
    #  the move that it thinks is best for the 'who' player
    #
    def move(self):
        # For debugging
        print("Score when move is called:" , self.simple_score(self.board))

        # All possible moves I can make. U is the konaneutils module.
        # mymoves is a list of Node objects, each has a future board position 
        #    and the move which generated it. 
        mymoves = U.genmoves(self.board, self.who)

        # STARTER CODE so that the player does something.
        # This will pick one random move
        # YOUR CODE REPLACES THIS
        random.shuffle(mymoves)
        mymove = mymoves[-1].moved
        # COMMENT OUT THE ABOVE AND REPLACE IT WITH YOUR OWN 

        # ALTERNATE STARTER CODE: A single max layer.
        #bestmaxnode = self.maxlayer(self.board, self.who)
        #mymove = bestmaxnode.moved
        # COMMENT OUT THE ABOVE AND REPLACE IT WITH YOUR OWN 
        
        # Assume that the move you selected (a 4-tuple) is in variable mymove.   
        return mymove

    # Simple function for maximizing layer, no cutoffs
    # Returns best successor Node object (a board position and the move which generated it)
    #
    def maxlayer(self, brd, plyr):
        # Generate a list of Node objects, representing possible child nodes
        possmoves = U.genmoves(brd, plyr)
        
        # For each possible move, score it.  Remember best
        bestmaxnode = None
        bestmaxscore = -10000
        for possmove in possmoves:
           poss_score = self.simple_score(possmove.b)
           if poss_score > bestmaxscore:
               bestmaxscore = poss_score
               bestmaxnode = possmove
        return bestmaxnode


    # Simple scoring function
    #
    # Compute the number of moves available for the 'who' player, minus the
    # number of moves available for the 'other' player.
    # Exception: if this position is a win or a loss, return +/- 1000
    #
    # YOU MIGHT WANT TO WRITE YOUR OWN MORE SOPHISTICATED SCORING FUNCTION
    #
    def simple_score(self, board):
        return len(U.genmoves(board, self.who)) - len(U.genmoves(board, self.other))

    # A simple wrapper check gameDone on the current master board
    def gameDone(self, whomoves):
        return U.gameDone(self.board, whomoves)


