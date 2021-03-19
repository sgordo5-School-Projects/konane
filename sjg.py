# This is a Python3 class file, for a class named Konane.
#
# One Konane object contains one player's information in a Konane game.
#
# The 'move' method returns your move.  Put your code there!
#
# Notice the konaneutils module contains useful functions you can use.

from sys import maxsize
import random
import konaneutils as U
import time

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

class Konane:
    def __init__(self, board, who):
        self.board = board   # Pointer to the board (in the main program)
        self.who = who
        self.other = {'x':'o', 'o':'x'}[who]
        self.human = False  # Self-explanatory

        # please also change line 154 if changing maxdepth
        self.maxdepth = 5   # How deep can your tree search go
        
        self.bestmove = None
  
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
        print("Score when move is called:" , self.score(self.board, 3))

        # All possible moves I can make. U is the konaneutils module.
        # mymoves is a list of Node objects, each has a future board position 
        #    and the move which generated it. 
        #mymoves = U.genmoves(self.board, self.who)

        # STARTER CODE so that the player does something.
        # This will pick one random move
        # YOUR CODE REPLACES THIS
        #random.shuffle(mymoves)
        #mymove = mymoves[-1].moved
        # COMMENT OUT THE ABOVE AND REPLACE IT WITH YOUR OWN 
        start = time.time()

        self.miniMax(self.board, self.maxdepth, -maxsize, maxsize, True)
        mymove = self.bestmove
        
        stop = time.time()

        print("Elapsed time was: " + str(stop - start) + "\n")
        # ALTERNATE STARTER CODE: A single max layer.
        #bestmaxnode = self.maxlayer(self.board, self.who)
        #mymove = bestmaxnode.moved
        # COMMENT OUT THE ABOVE AND REPLACE IT WITH YOUR OWN 
        
        # Assume that the move you selected (a 4-tuple) is in variable mymove.   
        return mymove

    # Simple function for maximizing layer, no cutoffs
    # Returns best successor Node object (a board position and the move which generated it)
    #
    #def maxlayer(self, brd, plyr):
        # Generate a list of Node objects, representing possible child nodes
        #possmoves = U.genmoves(brd, plyr)
        
        # For each possible move, score it.  Remember best
        #bestmaxnode = None
        #bestmaxscore = -10000
        #for possmove in possmoves:
           #poss_score = self.simple_score(possmove.b)
           #if poss_score > bestmaxscore:
               #bestmaxscore = poss_score
               #bestmaxnode = possmove
        #return bestmaxnode


    # Simple scoring function
    #
    # Compute the number of moves available for the 'who' player, minus the
    # number of moves available for the 'other' player.
    # Exception: if this position is a win or a loss, return +/- 1000
    #
    # YOU MIGHT WANT TO WRITE YOUR OWN MORE SOPHISTICATED SCORING FUNCTION
    #
    #def simple_score(self, board):
        #return len(U.genmoves(board, self.who)) - len(U.genmoves(board, self.other))

    # A simple wrapper check gameDone on the current master board
    def gameDone(self, whomoves):
        return U.gameDone(self.board, whomoves)

    # Minimax function that takes the possible moves, the depth of the tree
    # the alpha and beta cutoffs and a 1 for this AI's turn and 0 for other
    def miniMax(self, board, depth, alpha, beta, turn):       
        # Debugging print statements
            #U.print_board(board)
            #print("Score: " + str(self.score(board, depth)))
            #print("Depth: " + str(depth))
            #print(self.bestmove)
            #print("\n")
        
        # If very top of the node return the score of the board after the move
        if depth == 0:
            return self.score(board, depth)

        # If it is this player's turn
        if turn:
            # Generate moves from the current board for this player
            moves = U.genmoves(board, self.who)
            # Set worst max to negative infinity
            maxEval = -maxsize
            # For every move generated from that board
            for move in moves:
                # Evaluate all of its children up to the given depth
                eval = self.miniMax(move.b, depth - 1, alpha, beta, False)
                # If the score is better than the max score
                if eval >= maxEval:
                    # Set new max to this score
                    maxEval = eval
                    # A caveat here. I was having trouble finding a way to return the move
                    # that had the best score up the tree. Instead this should transfer the 
                    # shared score up the tree and if it is the depth 2 node that shares the
                    # best score that should also be the move that leads to that best outcome
                    # as the scores propogate up the tree and the if statement has >= the = 
                    # will let this move be chosen.
                    # If the depth is right and it is equal to the max it is the best move.
                    if depth >= 4:
                        self.bestmove = move.moved
                # take the max of alpha and eval for the cutoffs
                alpha = max(alpha, eval)
                #if the beta is greater than the alpha stop searching the tree
                if beta <= alpha:
                    break
            #return the max score found
            return maxEval
        
        # If it is not this player's turn
        else:
            # generate the moves of the other player with the given board
            moves = U.genmoves(board, self.other)
            # set the worst min to max integer
            minEval = maxsize
            # for all the generated moves
            for move in moves:
                # evaluate all the move's children
                eval = self.miniMax(move.b, depth - 1, alpha, beta, True)
                # second caveat. we don't need this move but as far as searching the tree
                # goes this is still important. This AI should never play this move but
                # it needs to know as it is what the opponent would pick.
                # set the new min to eval if lower
                minEval = min(minEval, eval)
                # if eval is lower than beta take eval as beta
                beta = min(beta, eval)
                # if beta is less than alpha trim the tree 
                if beta <= alpha:
                    break
            #return the lowest score found
            return minEval

    # not exactly complicated scoring
    def score(self, board, depth):
        #if the board loses for this player
        if U.gameDone(board, self.who):
            # negative infinity score
            return -maxsize
        #if the board wins for this player 
        elif U.gameDone(board, self.other):
            # positive infinity score
            return maxsize
        # else
        else:
            # take the amount of moves you have - the other player has + the current depth
            # to encourage moves higher up in the tree and to encourage a win faster
            return len(U.genmoves(board, self.who)) - len(U.genmoves(board, self.other)) + depth
