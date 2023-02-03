import pygame
from queue import PriorityQueue

WIDTH = 500
WIN = pygame.display.set_mode((WIDTH,WIDTH))
pygame.display.set_caption("A* Path Finding Algorithm")

Red = (255,0,0)
Green = (0,255,0)
Blue = (0,0,255)
Yellow = (255,255,0)
Black = (0,0,0)
White = (255,255,255)
Purple = (128,0,128)
Orange = (255,165,0)
Grey = (128,128,128)
Turquoise = (64,224,208)

class Cell:
    def __init__(self,row,col,width,total_rows):
        self.row = row
        self.col = col
        self.x = row*width
        self.y = col*width
        self.color = White
        self.neighbours = []
        self.width = width
        self.total_rows = total_rows
    
    def getPos(self):
        return self.row,self.col
    
    def isClosed(self):
        return self.color == Red
    
    def isOpen(self):
        return self.color == Green

    def isObstacle(self):
        return self.color == Black

    def isStart(self):
        return self.color == Orange

    def isEnd(self):
        return self.color == Turquoise

    def reset(self):
        self.color = White

    def makeClosed(self):
        self.color = Red

    def makeOpen(self):
        self.color = Green

    def makeObstacle(self):
        self.color = Black

    def makeStart(self):
        self.color = Orange
    
    def makeEnd(self):
        self.color = Turquoise
    
    def makePath(self):
        self.color = Purple
    
    def draw(self,win):
        pygame.draw.rect(win,self.color,(self.x,self.y,self.width,self.width))
    
    def updateNeighbours(self,grid):
        if self.row > 0 and not grid[self.row-1][self.col].isObstacle(): #up
            self.neighbours.append(grid[self.row-1][self.col])

        if self.row < self.total_rows-1 and not grid[self.row+1][self.col].isObstacle(): #down
            self.neighbours.append(grid[self.row+1][self.col])

        if self.col >0 and not grid[self.row][self.col-1].isObstacle(): #left
            self.neighbours.append(grid[self.row][self.col-1])

        if self.col < self.total_rows-1 and not grid[self.row][self.col+1].isObstacle(): #right
            self.neighbours.append(grid[self.row][self.col+1])
        

    def __lt__(self,other):
        return False

def h(p1,p2):
    x1,y1 = p1
    x2,y2 = p2
    return abs(x1 - x2) + abs(y1 - y2)

def reconstructPath(cameFrom,current,draw):
    while current in cameFrom:
        current = cameFrom[current]
        current.makePath()
        draw()
        

def algorithm(draw,grid,start,end):
    count = 0
    openSet = PriorityQueue()
    openSet.put((0,count,start))
    cameFrom = {}
    gScore = {cell: float("inf") for row in grid for cell in row}
    gScore[start] = 0
    fScore = {cell: float("inf") for row in grid for cell in row}
    fScore[start] = h(start.getPos(),end.getPos())
    openSetHash = {start}
    
    while not openSet.empty():
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()

        current = openSet.get()[2]
        openSetHash.remove(current)

        if(current == end):
            reconstructPath(cameFrom,end,draw)
            end.makeEnd()
            return True
        for neighbour in current.neighbours:
            temp_g_score = gScore[current]+1

            if temp_g_score < gScore[neighbour]:
                cameFrom[neighbour] = current
                gScore[neighbour] = temp_g_score
                fScore[neighbour] = temp_g_score + h(neighbour.getPos(),end.getPos())
                if neighbour not in openSetHash:
                    count+=1
                    openSet.put((fScore[neighbour],count,neighbour))
                    openSetHash.add(neighbour)
                    neighbour.makeOpen()

        draw()

        if current != start:
            current.makeClosed()

    return False       

def makeGrid(rows,width):
    grid = []
    cellWidth = width // rows
    for i in range(rows):
        grid.append([])
        for j in range(rows):
            cell = Cell(i,j,cellWidth,rows)
            grid[i].append(cell)
    return grid

def draw(win,grid,rows,width):
    win.fill(White)
    for row in grid:
        for cell in row:
            cell.draw(win)
    drawGrid(win,rows,width)
    pygame.display.update()

def drawGrid(win,rows,width):
    cellWidth = width // rows
    for i in range(rows):
        pygame.draw.line(win,Grey,(0,i*cellWidth),(width,i*cellWidth))
        for j in range(rows):
            pygame.draw.line(win,Grey,(j*cellWidth,0),(j*cellWidth,width))
    

def getCLickedPos(pos,rows,width):
    cellWidth = width // rows
    x,y = pos
    row = x//cellWidth
    col = y//cellWidth
    return row,col

def main(win,width):
    ROWS = 25
    grid = makeGrid(ROWS,width)
    start = None
    end = None
    run = True
    while run:
        draw(win,grid,ROWS,width)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if pygame.mouse.get_pressed()[0]: #left
                pos = pygame.mouse.get_pos()
                row,col = getCLickedPos(pos,ROWS,width)
                cell = grid[row][col]
                if not start and cell!=end:
                    start = cell
                    start.makeStart()
                elif not end and cell!=start:
                    end = cell
                    end.makeEnd()
                elif cell!=end and cell!=start:
                    cell.makeObstacle()

            elif pygame.mouse.get_pressed()[2]: #right
                pos = pygame.mouse.get_pos()
                row,col = getCLickedPos(pos,ROWS,width)
                cell = grid[row][col]
                cell.reset()
                if cell==start:
                    start=None
                elif cell==end:
                    end=None
                cell.reset()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and start and end:    
                    for row in grid:
                        for cell in row:
                            cell.updateNeighbours(grid)
                    algorithm(lambda: draw(win,grid,ROWS,width),grid,start,end)
                if event.key == pygame.K_c:
                    start = None
                    end = None
                    grid = makeGrid(ROWS,width)
            
            
    pygame.quit()   

main(WIN,WIDTH) 