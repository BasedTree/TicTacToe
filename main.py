#Created by Anthony Di Donato
import pygame as pg

pg.init()

#set display and screen up
width = 700
height = 700
screen = pg.display.set_mode((width, height))


#Load Sprites
BoardSprite =pg.transform.scale(pg.image.load("Assets\\boardsprite.png"), (500,500))
xsprite = pg.transform.scale(pg.image.load("Assets\\xsprite.png"),(100,100))
osprite = pg.transform.scale(pg.image.load("Assets\\osprite.png"), (100,100))

xwinsprite = pg.image.load("Assets\\xwin.png")
owinsprite = pg.image.load("Assets\\owin.png")
tiesprite = pg.image.load("Assets\\tiesprite.png")

#audio initialization
channel = pg.mixer.Channel(0)
channelbusy = False
winsound = pg.mixer.Sound("Assets\\winner.mp3")
tiesound = pg.mixer.Sound("Assets\\tie.mp3")

#extra variables
DoneGame = False
turn = "o"
winner = "none"


class Game:
    def __init__(self):
        self.board = [[0,0,0], [0,0,0], [0,0,0]] #the actual internal game board. 0 represents an empty spot

    
    def checkforwinner(self):
        #function to check for a winner
        #returns if the game has been ended and who won 

        b = self.board
        #rows
        for row in b:                   #rows are easy just iterate through the board list and compare
            if row == ["x", "x", "x"] or row == ["o", "o", "o"]:
                return True, row[0] 
        
        #columns
        for column in range(len(b)):
            templist = []               #must collect the columns in a temporary list to check for 3 in a row
            for cell in range(len(b)):
                templist.append(b[cell][column])
            if templist == ["x", "x", "x"] or templist == ["o", "o", "o"]:
                return True, templist[0]
            
        #diagonals
        templist = []                   #diagonals stored in temporary lists and checked, but need 2 for both diagonals
        templist2 = []
        for i in range(len(b)):
            templist.append(b[i][i])
            templist2.append(b[i][2-i])
        if templist == ["x", "x", "x"] or templist == ["o", "o", "o"]:
            return True, templist[0]
        if templist2 == ["x", "x", "x"] or templist2 == ["o", "o", "o"]:
            return True, templist2[0]
        
        #tie 
        zeros = 0                # simply checks if there are any zeros left, this would only run at the end of the game as if someone had won, this method would not be called anymore
        for row in b:
            for cell in row:
                if cell == 0:
                    zeros+=1
        if zeros ==0:
            return True, "tie"
        

        return False, "none"   #nobody won...yet
                


    def placeinboard(self, position, type):
        #The actual modification of the internal board when someone places an x or o
        #arguments: position: as a number from 0 to 8, the index of the "flattened" game board, type: an x or o
        #flattens the board into a single vector, changes the entry in index "position", then reassembles the board
        self.flattenedboard = []        
        for i in range(3):
            self.flattenedboard += self.board[i]
        self.flattenedboard[position] = type
        self.board = [self.flattenedboard[0:3], self.flattenedboard[3:6], self.flattenedboard[6:9]]
        

class play_button:
    def __init__(self, pos, size, image, location):
        self.pos = pos
        self.size=size
        self.image = pg.transform.scale(image, size)
        self.rect = self.image.get_rect()
        self.rect.center = pos
        self.location = location
        self.active = True
        
    def check_for_click(self):
        #returns true if the button is clicked
        #button cant be clicked only if self.active is true
        if (self.active):
            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] in range (self.rect.left, self.rect.right) and mouse_pos[1] in range (self.rect.top, self.rect.bottom):
                return True
            else:
                return False
        
    def update(self, turn):
        #this method is responsible for the translucent x or o that appears when you hover over a spot
        #it has to take the turn as an argument to determine which sprite to show
        #arguments: turn: which turn is in play ("x" or "o")
        if (self.active):
            if (turn == "o"):
                self.image = pg.transform.scale(pg.image.load("Assets\\osprite.png"), self.size)
            if (turn == "x"):
                self.image = pg.transform.scale(pg.image.load("Assets\\xsprite.png"), self.size)
            self.image.set_alpha(100)
            self.rect = self.image.get_rect()
            self.rect.center = self.pos

            mouse_pos = pg.mouse.get_pos()
            if mouse_pos[0] in range (self.rect.left, self.rect.right) and mouse_pos[1] in range (self.rect.top, self.rect.bottom):
                screen.blit(self.image, self.rect)


#initialize the buttons into a list
buttonlist = []
for i in range(3):
    for j in range(3):
        new_button = play_button((100+i*500/3 + 500/6,100+ j*500/3+ 500/6), (100,100), BoardSprite, (i, j)) #sets the location of the buttons to their appropriate places in the grid, note that 500 is the width/height of the grid sprite
        buttonlist.append(new_button)

#initialize the game class
game = Game()

## Runs inside the main game loop -----------------------------------------------------------------------------


def main(turn):
    #the main game function
    
    turn_local = turn  #takes the argument "turn" and makes it a local variable in the function namespace

    #draws the board
    screen.fill("black")
    BoardRect = BoardSprite.get_rect()
    BoardRect.center = (width/2, height/2)
    screen.blit(BoardSprite, BoardRect)

    #gets our game board array
    board=game.board

    #calls update on all buttons, allowing them to do the translucent hover thing
    for i in range(len(buttonlist)):
        button = buttonlist[i]
        button.update(turn)


    #handles pressing the buttons
    for event in pg.event.get():
        if event.type == pg.MOUSEBUTTONDOWN:        #only runs if mouse is pressed down
            for i in range(len(buttonlist)):        #check all buttons
                button = buttonlist[i]              
                if (button.check_for_click()):          #runs for the button that is pressed
                    game.placeinboard(i, turn_local)    #places whoevers turn it is at index i into the flattened list
                    button.active = False               #deactivates the button so it cant be pressed again
                    
                    if (turn_local == "x"):             #the rest flips the turn
                        turn_local = "o"
                    else:
                        turn_local = "x"



    #draws os and xs that have been placed    
    for row in range(len(game.board)):
        for column in range(len(game.board)):
            cell = board[row][column]
            if (cell == "x"):
                #draw x
                rect = xsprite.get_rect()
                rect.center= (100+row*500/3 + 500/6,100+ column*500/3+ 500/6)
                screen.blit(xsprite, rect)
            if (cell == "o"):
                #draw 0
                rect = osprite.get_rect()
                rect.center= (100+row*500/3 + 500/6,100+ column*500/3+ 500/6)
                screen.blit(osprite, rect)

    return turn_local           #since the flipping of the turn happens in this function, it must be returned to the global namespace

    

#game loop, DoneGame is set to false when there is no winner
while not DoneGame:

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()


    turn = main(turn)                   #runs the main function of the game
    DoneGame, winner = game.checkforwinner()        #checks the board for a winner, automatically ends the game if one has been found
    pg.display.flip()


#the endgame state of the game
while DoneGame: 
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
    
    screen.fill("black")
    board = game.board

    #draws final board
    BoardRect = BoardSprite.get_rect()
    BoardRect.center = (width/2, height/2)
    screen.blit(BoardSprite, BoardRect)
    for row in range(len(game.board)):
        for column in range(len(game.board)):
            cell = board[row][column]
            if (cell == 0):
                pass
            if (cell == "x"):
                #draw x
                rect = xsprite.get_rect()
                rect.center= (100+row*500/3 + 500/6,100+ column*500/3+ 500/6)
                screen.blit(xsprite, rect)
            if (cell == "o"):
                #draw 0
                rect = osprite.get_rect()
                rect.center= (100+row*500/3 + 500/6,100+ column*500/3+ 500/6)
                screen.blit(osprite, rect)

    #draws winning text and sound effect
    if (winner == "x"):
        if not channelbusy:
            channelbusy = True
            channel.play(winsound)

        rect = xwinsprite.get_rect()
        rect.center = (width/2, height/2)
        screen.blit(xwinsprite, rect)

    if (winner == "o"):
        if not channelbusy:
            channelbusy = True
            channel.play(winsound)

        rect = owinsprite.get_rect()
        rect.center = (width/2, height/2)
        screen.blit(owinsprite, rect)

    if (winner == "tie"):
        if not channelbusy:
            channelbusy = True
            channel.play(tiesound)

        rect = tiesprite.get_rect()
        rect.center = (width/2, height/2)
        screen.blit(tiesprite, rect)

    pg.display.flip()