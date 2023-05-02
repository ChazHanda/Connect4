#Connect 4 game
import time

#class containing board state and methods of board manipulation
class BoardState:
    def __init__ (self, rows, columns, state=None):
        self.row = rows
        self.column = columns
        if state is None:
            self.board = [[0 for x in range(self.column)] for y in range(self.row)]
        else:
            self.board = state

    def otherPlayer(self, player):
        if (player == 1):
            return 2
        else:
            return 1

    def getColumn(self, sub = None):
        if (sub == None):
            return self.column
        else:
            return int( self.column - 1)
    
    def getBoard(self):
        return self.board

    def boardCopy(self):
        return [row[:] for row in self.board]

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

#no out-of-bounds check, only checking specific column
    def checkValidMove(self, column):
        if (column <=0 or
            column >self.row):
            return False
        if(self.board[0][column-1] == 0):
            return True
        else:
            return False

#returns row of piece placement, -1 for no placement
#might remove checkValidMove
    def placePiece(self, player, column):
        if (self.checkValidMove(column)):
            for rowPos in range(self.row-1, -1, -1):
                if (self.board[rowPos][column-1] == 0):
                    self.board[rowPos][column-1] = player
                    return rowPos
        else:
            return -1

#optimize this later
    def checkColumnWin(self, player, row):
        for pos in range(self.column - 3):
            if (self.board[row][pos] == player and
                self.board[row][pos + 1] == player and
                self.board[row][pos + 2] == player and
                self.board[row][pos + 3] == player):
                return True
        return False

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
        if(self.checkRowWin(player, row) or
           self.checkColumnWin(player, column) or
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
        
#optimize not working       
#    def checkDiagWin(self, player, row, column):
#        if (row < 3):
#            rowStart = 0
#        else:
#            rowStart = row - 3
#            
#        if (row > self.row -4):
#            rowEnd = self.row -1
#        else:
#            rowEnd = row + 3
#            
#        if (column < 3):
#            columnStart = 0
#        else:
#            columnStart = column - 3
#            
#        if (column > self.column -4):
#            columnEnd = self.column -1
#       else:
#           columnEnd = column + 3
#
#        if(columnEnd - columnStart >= 3 and rowEnd - rowStart >= 3):
#            for pos in range(rowStart, rowEnd - 3):
#                for pos2 in range (columnStart, columnEnd - 2):
#                    if (self.board[pos][pos2] == player and
#                        self.board[pos + 1][pos2 + 1] == player and
#                        self.board[pos + 2][pos2 + 2] == player and
#                        self.board[pos + 3][pos2 + 3] == player):
#                        return True
#                for pos2 in range (columnEnd, columnStart + 2, -1):
#                    if (self.board[pos][pos2] == player and
#                        self.board[pos + 1][pos2 - 1] == player and
#                        self.board[pos + 2][pos2 - 2] == player and
#                        self.board[pos + 3][pos2 - 3] == player):
#                        return True
#                    
#            return False
        
def playerSwap(player):
    if (player == 1):
        return 2
    else:
        return 1
def playerLabel(player):
    if (player == 1):
        return "X"
    else:
        return "O"

#testBoard = [
#    [2, 1, 1, 1],
#    [1, 1, 2, 1],
#    [1, 1, 2, 2],
#    [1, 1, 2, 1],
#]
#board2 = BoardState(4,4, testBoard)
#
#board2.printBoard()
#
#print(board2.checkWin(1,1,3))
#print(board2.checkDraw())


#board = BoardState (4, 4)
player = 2
play = True
draw = False
width = int(input("Enter a width:"))
height = int(input("Enter a height:"))
board = BoardState(int(width), height)

while (play == True):
    print("\n\n")
    player = playerSwap(player)
    invalidMove = True
    while (invalidMove == True):
        board.printBoard()
        moveRowPos = -1
        pLabel = playerLabel(player)
        userInput = input("Player " + pLabel + " select move (type 1-" + str(board.getColumn()) + "):")
        try:
            moveRowPos = int(userInput)
        except ValueError:
            pass
        if (board.checkValidMove(moveRowPos)):
            columnPos = board.placePiece(player, moveRowPos)
            invalidMove = False

            if (board.checkWin(player, (moveRowPos -1), columnPos)):
                play = False
                
            elif (columnPos == 0 and
                board.checkDraw()):
                play = False
                draw = True
                
            
        else:
            print("Invalid Move.")
            time.sleep(2)
            print("\n\n")


board.printBoard()
if(draw == True):
    print("Draw!")
else:
    pLabel = playerLabel(player)
    print("Player " + pLabel + " Wins!")


    
