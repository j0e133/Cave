import pygame, sys, prng
import random as r
from pygame.locals import *

pygame.init()

#list of all of the pixels in the map
cells = []

#colors
FLOOR = (250, 250, 250)
WALL_GREY = (100, 100, 100)
SHADOW_GREY = (175, 175, 175)
TREASURE = (255, 0, 0)

#inputed variables
width = int(input('width?       '))             #cell map width
height = int(input('height?      '))            #cell map height
fillPercent = int(input('density?     '))       #how densley the original cell map is filled
seed = int(input('seed?        '))              #used to generate pseudo random numbers for the original cell map
scale = int(input('scale?       '))             #how big each pixel is
smoothness = int(input('smoothness?   '))       #how many times the map will be smoothed


#generates the original map
for x in range(width):                                                  #repeats for each cell in the width
    cells.append([])                                                    #makes a new list inside of the 'cells' list
    for y in range(height):                                             #repeats for each cell in the height
        if x == 0 or y == 0 or x == width - 1 or y == height - 1:       #if the x and y are on any of the four edges of the pixel map
            fill = WALL_GREY                                            #sets the cell's fill color to a wall
        elif prng.randomSeed(seed * (x / y), 100) <= fillPercent:       #if the cell isn't an edge, it gets a pseudo random number based on the seed, x, and y. If that random number is less than the fill percent
            fill = WALL_GREY                                            #also sets the cell's fill color to a wall
        else:                                                           #if the cell still isn't a wall
            fill = FLOOR                                                #sets the cells fill color to the floor
                
        cells[x].append(fill)                                           #adds the cell to the x list


    
def smoothen():                                                             #the method for smoothing the pseudo random cells into a cave-like structure

    global cells                                                            #gets the global variable that holds the list of cells

    newCells = cells.copy()                                                 #makes a coppy of the cell map to make changes to

    for x in range(width):                                                  #repeats for each cell
        for y in range(height):                                             #/\
            if not x == 0 or y == 0 or x == height - 1 or y == width - 1:   #if the x and y aren't on any of the four edges of the pixel map
                neighbors = numOfNeighbors([x, y])                          #gets the number of neighbors that cell has
                if neighbors > 4:                                           #if the cell has more than four neighbors
                    newCells[x][y] = WALL_GREY                              #sets the cell to a wall
                elif neighbors < 4:                                         #if the cell has less than four neighbors
                    newCells[x][y] = FLOOR                                  #sets the cell to the floor
                                                                            #if the cell has exactly four neighbors, it stays the same
    cells = newCells.copy()                                                 #replaces the cell map with the modified cell map



def numOfNeighbors(coordinate):                                                                             #function used to find the number of wall neighbors a given point has
    
    global cells                                                                                            #the global list of cells

    neighbors = 0                                                                                           #makes a variable for the number of neighbors the point has
    coordinateX = coordinate[0]                                                                             #sets an x for the point
    coordinateY = coordinate[1]                                                                             #sets a y for the point

    if coordinateX != 0 and coordinateY != 0 and coordinateX != width - 1 and coordinateY != height - 1:    #if the point isn't on the border
        for x in range(-1,2):                                                                               #repeats for each of the 9 cells in a 3 x 3 around the point
            for y in range(-1,2):                                                                           #/\
                if cells[coordinateX + x][coordinateY + y] == WALL_GREY and not x == y == 0:                #if the neighboring cell is a wall and not the point itself
                    neighbors += 1                                                                          #increases the neighbor value by 1

        return neighbors                                                                                    #returns the number of neighbors

    else:                                                                                                   #if the point is a border cell
        return 8                                                                                            #returns 8 so the borders always stay walls


    
def showMap():                                                                                  #shows the cell map using the pygame library

    global cells                                                                                #the global list of cells

    for x in range(width):                                                                      #repeats for each cell in the width
        for y in range(height):                                                                 #/\
            pygame.draw.rect(windowSurface, cells[x][y], (x * scale, y * scale, scale, scale))  #pygame to draw a square with size based on the scale

    pygame.display.update()                                                                     #pygame diplays the update to the window with all of the new squares



def shadows():                                                                                                  #changes the cell map so the final result looks more 3d

    global cells                                                                                                #the global list of cells

    for x in range(width):                                                                                      #repeats for each cell
        for y in range(height):                                                                                 #/\
            if cells[x][y] == FLOOR and cells[x][y - 1] == WALL_GREY:                                           #does some math to make a 3 cell long shadow below any floor cell with a wall above it
                cells[x][y] = SHADOW_GREY                                                                       #/\
            if cells[x][y] == FLOOR and cells[x][y - 1] == SHADOW_GREY and not cells[x][y - 3] == SHADOW_GREY:  #/\
                cells[x][y] = SHADOW_GREY                                                                       #/\



class room:                     #makes a class of room objects
    def __init__(self, cells):  #when a new room object is created, it gets all of it's cells passed in
        self.cells = cells      #makes a cell list inside of the room object that holds all of the passed in cells



def findAreas():                                                            #finds all of the rooms(pockets of floor) and walls(pockets of wall)

    global cells                                                            #the global list of cells
    global rooms                                                            #gets the global variable that holds the list of rooms
    global walls                                                            #gets the global variable that holds the list of wall sections

    alreadyChecked = []                                                     #makes a list of already checked cells

    for x in range(width):                                                  #repeats for each cell
        for y in range(height):                                             #/\
            if not ([x, y] in alreadyChecked):                              #if the cell hasn't already been checked
                fillArea = floodFill(x, y)                                  #makes a variable that stores a flood fill starting at the cell's position

                if cells[x][y] == WALL_GREY:                                #if the area is made of walls
                    walls.append(room(fillArea))                            #adds a room object with the area's cells to the 'walls' list
                else:                                                       #if the area isn't made of walls
                    rooms.append(room(fillArea))                            #adds a room object with the area's cells to the 'rooms' list

                for cell in fillArea:                                       #for each cell in the flood filled area
                    alreadyChecked.append(cell)                             #adds that cell to the already checked list



def floodFill(x, y):                                                                        #the flood fill(takes in a starting x and y)

    global cells                                                                            #the global list of cells

    que = []                                                                                #a que of cells that need to be evaluated
    area = []                                                                               #a list of all the cells in the area
    areaType = cells[x][y]                                                                  #the area's type(walls or room)

    que.append([x, y])                                                                      #adds the starting x y position to the que

    while len(que) > 0:                                                                     #while the que has items in it
        area.append(que[0])                                                                 #adds the first item of the que to the area

        currentCellX = que[0][0]                                                            #sets a variable for the x and y of the evaluating cell
        currentCellY = que[0][1]                                                            #/\

        for x in range(-1, 2):                                                              #repeats for each of the 9 cells in a 3 x 3 around the cell
            for y in range(-1, 2):                                                          #/\

                newCellX = currentCellX + x                                                 #sets a variable for the x and y of the new cell
                newCellY = currentCellY + y                                                 #/\

                if (currentCellX == newCellX or currentCellY == newCellY) and not x == y:   #if the new cell is directly next to the evaluating cell(all the cells in a plus shape) and isn't the evaluating cell itself
                    if 0 <= newCellX <= width - 1 and 0 <= newCellY <= height - 1 and cells[newCellX][newCellY] == areaType and not [newCellX, newCellY] in que and not [newCellX, newCellY] in area:   # explanation on line 158
                        que.append([newCellX, newCellY])                                    #adds the new cell to the que
                                                                                            #(explanation for line 156) if the new cell is inside or on the border AND the new cell is the same type as the area AND the new cell isn't in the que or area lists
        que.remove(que[0])                                                                  #removes the first item of the que

    return area                                                                             #returns the area list of all of the cells



def deleteGaps(minimumSize):

    global cells
    global rooms
    global walls

    newRooms = rooms.copy()
    newWalls = walls.copy()

    for room in rooms:
        if len(room.cells) < minimumSize:
            for cell in room.cells:
                cells[cell[0]][cell[1]] = WALL_GREY

            newRooms.remove(room)

    for wall in walls:
        if len(wall.cells) < minimumSize:
            for cell in wall.cells:
                cells[cell[0]][cell[1]] = FLOOR

            newWalls.remove(wall)

    rooms = newRooms
    walls = newWalls


    
def treasure(amount, difference):

    global cells
    global width

    treasures = r.randint(amount - round(difference / 2 - 0.1), amount + difference)
    treasuresPlaced = 0

    while treasuresPlaced < treasures:
        x = r.randint(0, width - 1)
        y = r.randint(0, height - 1)

        if cells[x][y] != WALL_GREY:
            cells[x][y] = TREASURE
            treasuresPlaced += 1



windowSurface = pygame.display.set_mode((width * scale, height * scale), 0, 32)
pygame.display.set_caption('Cave Generator')

windowSurface.fill(FLOOR)


for i in range(smoothness):
    smoothen()

rooms = []
walls = []

findAreas()
deleteGaps(35)
shadows()

roomTiles = 0
for room in rooms:
    roomTiles += len(room.cells)

numOfTreasures = round(roomTiles / 1000)
variability = round(numOfTreasures / 5)

treasure(numOfTreasures, variability)
showMap()


while True:
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            sys.exit()





