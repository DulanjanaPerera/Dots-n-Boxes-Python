import pygame
from Grid import Grid
from Cells import Cells
from AIdecision import AIdecision
import copy, time

print("\n********** Dots and Boxes*************\n")
print("Lines can be drawn only between two adjacent dots. Higher plyies(>4) will take\nsignificant time to compute the computer's next move")

# program consider ROWs as dots. Hence number of Dots = Number of Boxes + 1
ROWs = int(input("Enter number of Boxes in a row: ")) + 1
COLs = int(input("Enter number of Boxes in a column: ")) + 1
plys = int(input("Number of plys: "))


# Before the game starts, the dots coordinates, neighbors, corresponding cells and cell values are calculated and
# store in dictionaries for fast membership search. List are not ideal for membership because it is not a hash object

grid = Grid(ROWs, COLs)  # create the grid object
dotVertices = grid.grid_vertices()  # Grid vertices (a.k.a Dots)
cellValues = grid.cellvalue  # get the cell values as a list
WIDTH = grid.WIDTH  # get the grid width
HEIGHT = grid.HEIGHT  # get the grid height

# create cell info object which has cell vertices, value and edges
cellInfo = Cells(ROWs, COLs, dotVertices, cellValues)
cellDictionary = cellInfo.cellDictionary  # contains cell vertices, value and player's selected the edges
edgeInfo = cellInfo.edgecell  # contains the cell indexes that corresponds with the a edge
childDictionary = cellInfo.childDictionary  # get the all the child dots and edge for each dots for the search tree


# GUI initializing
BOARD = (WIDTH, HEIGHT)
pygame.init()
window = pygame.display.set_mode(BOARD)

# Define colors for text, board, dots and squares
GREEN = (0, 138, 0)  # drawn lines
WHITE = (255, 255, 255)  # board background
VIOLET = (170, 0, 255)  # Player text color, won boxes
PINK = (244, 144, 208)  # Player's dots
YELLOW = (227, 200, 0)  # AI won boxes
BLACK = (12, 12, 12)  # Initial dots


# Create text for players and match status
myfont = pygame.font.SysFont("Times New Roman", 15)
winFont = pygame.font.SysFont("Times New Roman", 25)
User = myfont.render("User", True, (255, 0, 255))
Machine = myfont.render("Machine", True, (255, 0, 0))
wintext = winFont.render("You Win", True, (255, 0, 0))
losetext = winFont.render("You Lose", True, (255, 0, 0))


# Player details
UserselectedDots = []  # Store the selected dots locations
Userwins = []  # player won box vertex for drawing
player_score = 0  # score player won so far
userplayedStatus = False  # player turn

# AI bot details
AIwins = []
ai_score = 0
aiplayerStatus = False

# store line locations
drawnlines = []

# visited edges - create empty set for fast membership check
visitedEdges = set()

RUNNING = True
pos = None

while RUNNING:
    window.fill(WHITE)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            RUNNING = False

        # Detect the mouse down click
        if event.type == pygame.MOUSEBUTTONDOWN:
            indxD = 0
            pos = event.pos  # Get the cursor location
            indxD = grid.selected_dot(pos)  # get the corresponding location index from the vertices list
            print(indxD)
        if event.type == pygame.MOUSEBUTTONUP and not userplayedStatus:
            indxU = 0
            pos = event.pos
            indxU = grid.selected_dot(pos)
            print(indxU)

            # only different dots are selected, then line is drawn.
            if indxU >= 0 and indxD >= 0 and not(indxD == indxU):  # if index is <0, that means the out of grid
                # rearrange the selected dots' indices to ascending order which match with dictionary - edgeInfo
                if indxD > indxU:
                    edge = str(indxU) + "," + str(indxD)
                else:
                    edge = str(indxD) + "," + str(indxU)
                if not edge in visitedEdges:
                    visitedEdges.add(edge)  # add to the visited edge set
                    userplayedStatus = True
                    cellIndex = edgeInfo[edge]  # get the corresponding cell indices of the edge
                    for i in cellIndex:
                        # store the player in the corresponding cell "P" - player, "A" - AI bot
                        cellDictionary.get(i)[3].append("P")
                        if len(cellDictionary.get(i)[3]) == 4:  # if number of players are 4 then cell is completed
                            # store the cell vertices for drawing the rectangle and cell value for final calculation
                            Userwins.append(cellDictionary.get(i)[0])
                            player_score += cellDictionary.get(i)[2]
                            print("Player current score", player_score)
                            print("Computer current score", ai_score, "\n")

                    vertex1 = dotVertices[indxD]  # get corresponding index position (x,y) for drawing
                    vertex2 = dotVertices[indxU]
                    UserselectedDots.append(vertex1)  # append corresponding dot location
                    UserselectedDots.append(vertex2)
                    drawnlines.append([vertex1, vertex2])  # store in a list for draw the lines

        # AI bot turn
        if userplayedStatus:
            userplayedStatus = False

            # create a deep copy because inside the method theses dictionaries are updates but I don't need the
            # referenced object to be updated.
            _visitedEdges = copy.deepcopy(visitedEdges)
            _cellDictionary = copy.deepcopy(cellDictionary)
            start_time = time.time()
            aidecision = AIdecision(_visitedEdges, childDictionary, _cellDictionary, edgeInfo, edge, plys)
            print("--- %s seconds ---" % (time.time() - start_time))
            ai_move = aidecision.bestMove
            if not (ai_move is None) and ai_move not in visitedEdges:
                visitedEdges.add(ai_move)
                cells = edgeInfo[ai_move]
                for i in cells:
                    cellDictionary.get(i)[3].append("A")
                    # print(cellDictionary.get(i)[3])
                    if len(cellDictionary.get(i)[3]) == 4:
                        AIwins.append(cellDictionary.get(i)[0])
                        ai_score += cellDictionary.get(i)[2]
                        print("Player current score", player_score)
                        print("Computer current score", ai_score, "\n")

                vertexList = cellInfo.edge_to_dots(ai_move)
                vertex1 = dotVertices[vertexList[0]]
                vertex2 = dotVertices[vertexList[1]]
                drawnlines.append([vertex1, vertex2])

    window.blit(User, (40, 10))  # Add the text 'User'
    window.blit(Machine, (20, 30))  # Add the text 'Machine'

    if len(dotVertices) > 0:  # draw dots
        for i in range(len(dotVertices)):
            pygame.draw.circle(window, BLACK, (dotVertices[i][0], dotVertices[i][1]), 2)

    if len(UserselectedDots) > 0:  # draw selected dots in different color
        for i in range(len(UserselectedDots)):
            pygame.draw.circle(window, PINK, (UserselectedDots[i][0], UserselectedDots[i][1]), 5)

    if len(drawnlines) > 0:  # Draw all the selected edges
        for i in range(len(drawnlines)):
            pygame.draw.line(window, GREEN, drawnlines[i][0], drawnlines[i][1], 5)

    if len(Userwins) > 0:  # Draw player won squares
        for i in range(len(Userwins)):
            pygame.draw.rect(window, VIOLET, (Userwins[i][0][0], Userwins[i][0][1], grid.CELLSIZE, grid.CELLSIZE))

    if len(AIwins) > 0:  # Draw Bot won squares
        for i in range(len(AIwins)):
            pygame.draw.rect(window, YELLOW, (AIwins[i][0][0], AIwins[i][0][1], grid.CELLSIZE, grid.CELLSIZE))

    if len(AIwins) + len(Userwins) == len(cellDictionary):
        print("Player Score: ", player_score, "\n", "AI bot Score: ", ai_score, "\n\n")
        if player_score == ai_score:
            print("Match Draw !!!!!")
            window.blit(losetext, (WIDTH / 4, 20))
        elif player_score > ai_score:
            print("Winner is Player !!!!!")
            window.blit(wintext, (WIDTH / 4, 20))
        else:
            print("Winner is AI bot !!!!!")
            window.blit(losetext, (WIDTH / 4, 20))
        User = myfont.render("User", True, WHITE)
        Machine = myfont.render("Machine", True, WHITE)
        window.blit(User, (40, 10))  # Add the text 'User'
        window.blit(Machine, (20, 30))  # Add the text 'Machine'
        pygame.display.update()
        time.sleep(3)
        RUNNING = False

    pygame.display.update()
pygame.quit()
