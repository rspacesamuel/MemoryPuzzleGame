#my draft for memory puzzle game
import pygame, sys, random, itertools
from pygame.locals import *

#global variables in upper case
WINDOW_WIDTH = 250
WINDOW_HEIGHT = 250
BOXES_ACROSS = 4
BOXES_DOWN = 4
#box width/height are not global, they are class variables of Box class. See class definition below
END_OF_ROW = False
#need to add an assertion so that Window dimensions and the no. of boxes match; also the no. of boxes and the no. of board color/shapes should match

WHITE = (255,255,255)
GAME_BKGRND_COLOR = WHITE

RED = (255,0,0)
GREEN = (0,100,0)
BLUE = (0,0,205)
YELLOW = (255,255,0)
PURPLE = (160,32,240)
PINK = (255,20,147)
PEACH = (255,218,185)
CYAN = (0,255,255)

COLORS = [RED, GREEN, BLUE, YELLOW, PURPLE, PINK, PEACH, CYAN]
SHAPES = ["CIRCLE", "DIAMOND", "CROSS", "TRIANGLE", "DONUT", "SQUARE", "X", "SQUAREDONUT"]

#list of shapes and colors.
BOARD = [] 

#Box cosmetics
CLEARBLUE = (0,0,255) 
TOP_LEFT_X = -50
TOP_LEFT_Y = 10

def setupMainBoard():
    global BOARD, COLORS, SHAPES
    #set up Main board randomly for each run
    random.shuffle(COLORS)
    random.shuffle(SHAPES)
    for color, shape in zip(COLORS, SHAPES):
        #(color,shape) is a tuple because this ordered pair shouldn't be taken apart:
        BOARD.append((color,shape))
    #copy filled half to the empty half in the list
    BOARD = BOARD + BOARD
    random.shuffle(BOARD)

#calculates and returns top left (x,y) coordinates of each box as they are instantiated as objects (should this be a member function?)
def incrementXY(eachBoxAcross):
    global TOP_LEFT_X, TOP_LEFT_Y, END_OF_ROW

    if eachBoxAcross == BOXES_ACROSS-1:
        #this is the last box of the row
        END_OF_ROW = True
        TOP_LEFT_X += 60
    elif END_OF_ROW == True:
        #end of row was set to True for last box, so this box starts in next row
        END_OF_ROW = False
        TOP_LEFT_X = 10
        TOP_LEFT_Y += 60
    else:
        #keep going on the current row of boxes
        TOP_LEFT_X += 60
        
    #return top left (x,y) of current box as a tuple. This is unpacked at function call using * operator
    return (TOP_LEFT_X, TOP_LEFT_Y)

def main():
    #variables for MOUSEBUTTONUP action
    #these 2 are lists instead of tuples just so that they can be changed along the way, otherwise they store exactly one tuple of color, shape
    firstBoxColorShape = []
    secondBoxColorShape = []
    firstBoxIndex = -1
    secondBoxIndex = -1
    numBoxesRevealed = 0
    prevTopLeftX = -1
    prevTopLeftY = -1
    
    pygame.init()
    gamesurface = pygame.display.set_mode ((WINDOW_WIDTH, WINDOW_HEIGHT))
    gamesurface.fill(GAME_BKGRND_COLOR)
    setupMainBoard()
    
    class Box:
        #box default values. These will apply to ALL box instances
        boxOuterColor = CLEARBLUE
        boxHighlighterColor = YELLOW
        boxBorderColor = YELLOW
        boxWidth = 50
        boxHeight = 50
        
        def __init__(self, topLeftX, topLeftY):
            #initialize object specific variables for each box
            self._topLeftX = topLeftX
            self._topLeftY = topLeftY
            self._boxHighlighted = False
            self._boxRevealed = False
            self._boxRevealedAndScored = False
            self._firstOfTwoBoxes = False
            self._colorAndShape = []
            #draw box
            pygame.draw.rect(gamesurface, self.boxOuterColor, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),0)
            pygame.draw.rect(gamesurface, self.boxBorderColor, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),2)

        def mousePointerOnBox(self, mouseX, mouseY):
            #returns True if mouse pointer is on current box
            if mouseX >= self._topLeftX and mouseX <= self._topLeftX+50 and mouseY >= self._topLeftY and mouseY <= self._topLeftY+50:
                return True
            else:
                return False
            
        def highlightBox(self, mouseX, mouseY):
            if self.mousePointerOnBox(mouseX, mouseY):
                #use the box's border color to give a halo
                pygame.draw.rect(gamesurface, self.boxBorderColor, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),6)
                self._boxHighlighted = True
            elif self._boxHighlighted == True:
                #clear highlighting of previously highlighted box
                self._boxHighlighted = False
                #turn off halo by painting background color
                pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),6)
                #reinstate box's border color
                pygame.draw.rect(gamesurface, self.boxBorderColor, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),2)

        def revealBox(self, mouseX, mouseY):
                self._boxRevealed = True
                                
                if self._colorAndShape[0][1] == "SQUARE":
                    #assign point list (x,y of each vertex) to a variable
                    squareVertices = [(self._topLeftX+15, self._topLeftY+15), (self.boxWidth-30, self.boxHeight-30)]
                    #"break open" the box by painting background color
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight), 0)
                    #draw the shape and color for the revealed object (in this case SQUARE) "inside" the "opened" box
                    pygame.draw.rect(gamesurface, self._colorAndShape[0][0], squareVertices, 0)
                    #do the same steps for all revealed objects below
                
                elif self._colorAndShape[0][1] == "SQUAREDONUT":
                    sqrDonutVertices = [(self._topLeftX+15, self._topLeftY+15), (self.boxWidth-30, self.boxHeight-30)]
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight), 0)
                    pygame.draw.rect(gamesurface, self._colorAndShape[0][0], sqrDonutVertices, 6)

                elif self._colorAndShape[0][1] == "DIAMOND":
                    diamondVertices = [(self._topLeftX+int(self.boxWidth/2),self._topLeftY+10), (self._topLeftX+self.boxWidth-10,self._topLeftY+int(self.boxHeight/2)), (self._topLeftX+int(self.boxWidth/2),self._topLeftY+self.boxHeight-10), (self._topLeftX+10,self._topLeftY+int(self.boxHeight/2))]
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight), 0)
                    pygame.draw.polygon(gamesurface, self._colorAndShape[0][0], diamondVertices, 0)
                    
                elif self._colorAndShape[0][1] == "TRIANGLE":
                    triangleVertices = [(self._topLeftX+int(self.boxWidth/2),self._topLeftY+10), (self._topLeftX+self.boxWidth-10,self._topLeftY+self.boxHeight-10), (self._topLeftX+10, self._topLeftY+self.boxHeight-10)]
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight), 0)
                    pygame.draw.polygon(gamesurface, self._colorAndShape[0][0], triangleVertices, 0)
       
                elif self._colorAndShape[0][1] == "CIRCLE":
                    circleCenter = (self._topLeftX+int(self.boxWidth/2), self._topLeftY+int(self.boxHeight/2))
                    radius = int(self.boxWidth/2)-10
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),0)
                    pygame.draw.circle(gamesurface, self._colorAndShape[0][0], circleCenter, radius, 0)

                elif self._colorAndShape[0][1] == "DONUT":
                    circleCenter = (self._topLeftX+int(self.boxWidth/2), self._topLeftY+int(self.boxHeight/2))
                    radius = int(self.boxWidth/2)-12
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),0)
                    pygame.draw.circle(gamesurface, self._colorAndShape[0][0], circleCenter, radius, 6)
               
                elif self._colorAndShape[0][1] == "CROSS":
                    line1StartPos = (self._topLeftX+int(self.boxWidth/2), self._topLeftY+10)
                    line1EndPos = (self._topLeftX+int(self.boxWidth/2), self._topLeftY+self.boxHeight-10)
                    line2StartPos = (self._topLeftX+10,self._topLeftY+int(self.boxHeight/2))
                    line2EndPos = (self._topLeftX+self.boxWidth-10,self._topLeftY+int(self.boxHeight/2))
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),0)
                    pygame.draw.line(gamesurface, self._colorAndShape[0][0], line1StartPos, line1EndPos, 3)
                    pygame.draw.line(gamesurface, self._colorAndShape[0][0], line2StartPos, line2EndPos, 3)

                elif self._colorAndShape[0][1] == "X":
                    line1StartPos = (self._topLeftX+10, self._topLeftY+10)
                    line1EndPos = (self._topLeftX+self.boxWidth-10, self._topLeftY+self.boxHeight-10)
                    line2StartPos = (self._topLeftX+self.boxWidth-10,self._topLeftY+10)
                    line2EndPos = (self._topLeftX+10,self._topLeftY+self.boxHeight-10)
                    pygame.draw.rect(gamesurface, GAME_BKGRND_COLOR, (self._topLeftX, self._topLeftY, self.boxWidth, self.boxHeight),0)
                    pygame.draw.line(gamesurface, self._colorAndShape[0][0], line1StartPos, line1EndPos, 3)
                    pygame.draw.line(gamesurface, self._colorAndShape[0][0], line2StartPos, line2EndPos, 3)
                                                                                                                                                                     
    #instantiate the Object List for Box
    boxes = [Box(*incrementXY(eachBoxAcross)) for eachBoxDown in range(BOXES_DOWN) for eachBoxAcross in range(BOXES_ACROSS)]

    for i, eachBox in enumerate(boxes):
        eachBox._colorAndShape = [BOARD[i]]
        
    while True:
        for event in pygame.event.get():
            
            #exit game when clicking on x button on window
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
                
            elif event.type == MOUSEMOTION:
                #highlight the box that mouse pointer hovers
                mouseXY = pygame.mouse.get_pos()
                for eachBox in boxes:
                    eachBox.highlightBox(*mouseXY)
                    
            elif event.type == MOUSEBUTTONUP:                
                mouseXY = pygame.mouse.get_pos()
                for i, eachBox in enumerate(boxes):
                    if eachBox.mousePointerOnBox(*mouseXY) and eachBox._boxRevealedAndScored == False:
                        #if the box is clicked twice (or more) do nothing
                        if prevTopLeftX == eachBox._topLeftX and prevTopLeftY == eachBox._topLeftY:
                            #but: when the second box don't match with first it remains closed, and if it's clicked again,
                            #the player intends to open it, so open it. Ignore all other cases of clicking twice.
                            if numBoxesRevealed != 0:
                                break
                        else:
                            prevTopLeftX = eachBox._topLeftX
                            prevTopLeftY = eachBox._topLeftY
                        #reveal the box. Then check if it's first or second box.
                        eachBox.revealBox(*mouseXY)
                        numBoxesRevealed += 1
                        if numBoxesRevealed == 1:
                            firstBoxColorShape = eachBox._colorAndShape
                            firstBoxIndex = i
                            break
                        if numBoxesRevealed == 2:
                            secondBoxColorShape = eachBox._colorAndShape
                            secondBoxIndex = i
                            #moment of truth: if both boxes revealed the same items, mark both boxes as scored, else move on
                            if len(firstBoxColorShape) != 0 and len(secondBoxColorShape) != 0:
                                if (firstBoxColorShape == secondBoxColorShape):
                                    boxes[firstBoxIndex]._boxRevealedAndScored = True
                                    boxes[secondBoxIndex]._boxRevealedAndScored = True
                                else:
                                    pygame.time.wait(1000)
                                    #is this init calling appropriate??
                                    boxes[firstBoxIndex].__init__(boxes[firstBoxIndex]._topLeftX,boxes[firstBoxIndex]._topLeftY)
                                    boxes[secondBoxIndex].__init__(boxes[secondBoxIndex]._topLeftX,boxes[secondBoxIndex]._topLeftY)
                                    #init resets the box's color and shape, so get it back from BOARD
                                    boxes[firstBoxIndex]._colorAndShape = [BOARD[firstBoxIndex]]
                                    boxes[secondBoxIndex]._colorAndShape = [BOARD[secondBoxIndex]]
                            numBoxesRevealed = 0
                            del firstBoxColorShape[0], secondBoxColorShape[0]
                            break                
                        
        pygame.display.update()
    
if __name__ == '__main__':
    main()
