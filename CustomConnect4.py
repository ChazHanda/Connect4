#Connect 4 game

import time
import random

#board dimensions
MIN_WIDTH = 4
MAX_WIDTH = 7
MIN_HEIGHT = 4
MAX_HEIGHT = 10

#AI score and limitations
WIN_VALUE = 9999
LOSE_VALUE = -9999
DRAW_VALUE = 0
#TWO_VALUE = 1
#THREE_VALUE = 10
MAX_EVAL = -99999
MIN_EVAL = 99999
DEFAULT_DEPTH = 8


#class containing board state and methods of board manipulation
class BoardState:
    def __init__ (self, rows, columns, state=None, depth=None):
        self.row = rows
        self.column = columns
        if state is None:
            self.board = [[0 for x in range(self.column)] for y in range(self.row)]
        else:
            self.board = state
        if depth is None:
            self.depth = DEFAULT_DEPTH
        else:
            self.depth = depth

    def clearBoard(self):
        self.board = [[0 for x in range(self.column)] for y in range(self.row)]
        return

    def otherPlayer(self, player):
        if (player == 1):
            return 2
        else:
            return 1

    def getColumn(self):
            return self.column

    def getRows(self):
        return self.row

    def getBoard(self):
        return self.board

    def boardCopy(self):
        return BoardState(self.row, self.column,[row[:] for row in self.board])

    def printBoard(self):
        for row in range(self.row):
            rowText = "|"
            for column in range(self.column):
                if (self.board[row][column] == 0):
                    rowText += " "
                elif (self.board[row][column] == 1):
                    rowText += "X"
                elif (self.board[row][column] == 2):
                    rowText += "O"
                rowText += "|"
            print(rowText)
        print("=" * (self.column * 2 + 1))
        bottomText = " "
        for columnPos in range(self.column):
            bottomText += str(columnPos+1) + " "
        print(bottomText)

#needs column index
    def checkValidMove(self, column):
        if (column <0 or
            column >=self.column):
            return False
        if(self.board[0][column] == 0):
            return True
        else:
            return False


#needs column index
#returns row of piece placement, -1 for no placement
    def placePiece(self, player, column):
        if (self.checkValidMove(column)):
            for rowPos in range(self.row-1, -1, -1):
                if (self.board[rowPos][column] == 0):
                    self.board[rowPos][column] = player
                    return rowPos
        else:
            return -1

#need row index
#optimize this later
    def checkColumnWin(self, player, row):
        for pos in range(self.column - 3):
            if (self.board[row][pos] == player and
                self.board[row][pos + 1] == player and
                self.board[row][pos + 2] == player and
                self.board[row][pos + 3] == player):
                return True
        return False

#need column index
#optimize this later
    def checkRowWin(self, player, column):
        for pos in range(self.row - 3):
            if (self.board[pos][column] == player and
                self.board[pos + 1][column] == player and
                self.board[pos + 2][column] == player and
                self.board[pos + 3][column] == player):
                return True
        return False

#full board check, need to optimize
    def checkDiagWin(self, player):
        for row in range(self.row - 3):
            for column in range(self.column - 3):
                if (self.board[row][column] == player and
                    self.board[row + 1][column + 1] == player and
                    self.board[row + 2][column + 2] == player and
                    self.board[row + 3][column + 3] == player):
                        return True
            for column in range(3, self.column):
                if (self.board[row][column] == player and
                    self.board[row + 1][column - 1] == player and
                    self.board[row + 2][column - 2] == player and
                    self.board[row + 3][column - 3] == player):
                        return True
        return False

    def checkWin(self, player, row, column):
        if(self.checkRowWin(player, column) or
           self.checkColumnWin(player, row) or
           self.checkDiagWin(player)):
            return True
        else:
            return False
           

    def checkDraw(self):
        count = 0
        for column in range(self.column):
            if (self.checkValidMove(column) == False):
                count +=1
                
        if (count == self.column):
            return True
        else:
            return False

#AI functions for "CustomConnect4.py"

#add this later, will count potential partial rows for points
    def pointCounter (self, board, player, lengthCount):
         pass

            
#function returns a point value for the minimax algorithm
#currently not used
    def scoreTheBoard (self, board, row, column, player):
        if (board.checkDraw()):
            return DRAW_VALUE
            
        elif (board.checkWin(player, row, column)):
            return WIN_VALUE
            
    #change this to a scoring system later
        else:
            return 0


    def miniMax(self, board, depth, alpha, beta, mPlayer, player, pWon):
            
        if (board.checkDraw() == True):
                return DRAW_VALUE
        if (pWon == True):
            if (mPlayer == True):
                return LOSE_VALUE
            else:
                return WIN_VALUE
        if (depth == 0):
            #Add scoring later
                return DRAW_VALUE
            #return board.scoreTheBoard(board, row, column, player)
                    
        if (mPlayer == True):
            maxEval = MAX_EVAL
            for column in range(self.column):
                if (board.checkValidMove(column)):
                    bCopy = board.boardCopy()
                    row = bCopy.placePiece(player, column)
                    if (bCopy.checkWin(player, row, column)):
                        pWon = True
                    evaluation = bCopy.miniMax(bCopy, depth - 1, alpha, beta, False, bCopy.otherPlayer(player), pWon)
                    maxEval = max(maxEval, evaluation)
                    alpha = max(alpha, evaluation)
                    if (alpha >= beta):
                        break
            return maxEval
        else:
            minEval = MIN_EVAL
            for column in range(self.column):
                if (board.checkValidMove(column)):
                    bCopy = board.boardCopy()
                    row = bCopy.placePiece(player, column)
                    if (bCopy.checkWin(player, row, column)):
                        pWon = True
                    evaluation = bCopy.miniMax(bCopy, depth - 1, alpha, beta, True, bCopy.otherPlayer(player), pWon)
                    minEval = min(minEval, evaluation)
                    beta = min(beta, evaluation)
                    if (beta <= alpha):
                        break
            return minEval
            
    def bestMove(self, board, depth, player):
        bestScore = MAX_EVAL
        bestMove = None

        for column in range(self.column):
            if (board.checkValidMove(column)):
                    bCopy = board.boardCopy()
                    row = bCopy.placePiece(player, column)
                    if (bCopy.checkWin(player, row, column)):
                        pWon = True
                    else:
                        pWon = False
                    score = bCopy.miniMax(bCopy, depth - 1, MAX_EVAL, MIN_EVAL, False, bCopy.otherPlayer(player), pWon)
                    if (score > bestScore):
                        bestScore = score
                        bestMove = column
                    elif (score == bestScore):
#might need adjustment if MIN_WIDTH number is allowed to be 1 or smaller
                        randomNumber = random.randint(0, 2)
                        if (randomNumber == 0):
                            bestScore = score
                            bestMove = column
        return bestMove
        
    def aiPlacePiece(self, board, player):
        
        row = board.bestMove(board, self.depth, player)
        column = board.placePiece(player, row)
        return [row, column]
        
        
#maybe add 3rd player later
def playerSwap(player):
    if (player == 1):
        return 2
    else:
        return 1
    
#maybe add 3rd player later
def playerLabel(player):
    if (player == 1):
        return "X"
    else:
        return "O"

def invalidInput():
    print("Invalid input.")
    time.sleep(2)
    print("\n\n")

def yesNoPrompt(userInput):
    if(userInput.lower() != "n"):
        return True
    else:
        return False
    
#parameter "height" is bool
def inputBoardDimension(height):
    if (height == True):
        dimension = "height"
        minimum = int(MIN_HEIGHT)
        maximum = int(MAX_HEIGHT)
                      
    else:
        dimension = "width"
        minimum = int(MIN_WIDTH)
        maximum = int(MAX_WIDTH)
        
    while (invalidInput):
        try:
            userInput = int(input("Enter a board " + dimension + "(" + str(minimum) + "-" + str(maximum) + "):"))

            if (userInput>= minimum and
                userInput<= maximum):
                return userInput
            else:
                invalidInput()
        except:
            invalidInput()
    
def promptPlayerAI (player):
    invalidInput = True
    while (invalidInput):
        try:
            userInput = input("Will player " + playerLabel(player) + " be AI controlled? (Y/N):")
            return yesNoPrompt(userInput)
        except:
            invalidInput()
            
#returns index of player's move
def inputMove(board, pLabel):
    invalidInput = True
    while (invalidInput):
        try:
            board.printBoard()
            userInput = input("Player " + pLabel + " select move (type 1-" + str(board.getColumn()) + "):")
            moveRowPos = int(userInput) - 1
            if (board.checkValidMove(moveRowPos)):
                invalidInput = False
                return userInput
        except:
            invalidInput()

def inputPlayAgain():
    invalidInput = True
    while (invalidInput):
        try:
            userInput = input("Play again? (Y/N):")
            return yesNoPrompt(userInput)
        except:
            invalidInput()
            
def inputSameRules():
    invalidInput = True
    while (invalidInput):
        try:
            userInput = input("Same Rules? (Y/N):")
            return yesNoPrompt(userInput)
        except:
            invalidInput()

sameRules = False
keepPlaying = True
while (keepPlaying == True):
    
    player = 1
    
    if (sameRules == False):
        height = inputBoardDimension(True)
        width = inputBoardDimension(False)
        board = BoardState(height, width)
        playerAI = [False, False]

        #modify if making 3 person game
        if (promptPlayerAI(1)):
            playerAI[0] = True
            
        if (promptPlayerAI(2)):
            playerAI[1] = True

    else:
        
        sameRules = False
        
    board.clearBoard()   
    draw = False    
    play = True    
    while (play == True):
        if (playerAI[player - 1] == True):
            pos = board.aiPlacePiece(board, player)
            moveRowPos = pos[0]
            columnPos = pos[1]
                
        else:
            moveRowPos = inputMove(playerLabel(player))
            columnPos = board.placePiece(player, moveRowPos)              

        if (board.checkWin(player, columnPos, moveRowPos)):
            play = False
                        
        elif (columnPos == 0 and
            board.checkDraw()):
            play = False
            draw = True
            
        print("\n\n")
        board.printBoard()
        player = playerSwap(player)

    
    if(draw == True):
        print("Draw!")
    else:
        pLabel = playerLabel(playerSwap(player))
        print("Player " + pLabel + " Wins!")
        
    keepPlaying = inputPlayAgain()
    if(keepPlaying == True):
        sameRules = inputSameRules()
                          
    
