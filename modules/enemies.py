import pygame as pg
import cell
import random as rd
from enemies_base import *

class Patroller(Enemy):
    """An enemy which continuously moves from one fixed point to another on the shortest distance possible."""
    def __init__(self, startPt, endPt, grid):
        """startPt is one end of the linear path patrolled by this monster.
endPt is the other end. grid is required to get the cell size and also to find the path between startPt and endPt
This monster will spawn at startPt"""
        #Allowed only on floors and the goal
        super(Patroller, self).__init__(startPt[0], startPt[1], PATROLLER, grid[0][0].size,
                                        [cell.CT_GOAL, cell.CT_TELEPORTER])
        self.path = self.findPath(grid, startPt, endPt)
        self.__pathlen = len(self.path)
        self.__i = 0
        self.__dir = 1 #+1 for moving forward and -1 for moving backward through the path

    def move(self, grid, sprite):
        """Move the enemy through the path"""
        self.loc = self.path[self.__i]
        self.__i += self.__dir
        if self.__i >= self.__pathlen:
            self.__i = self.__pathlen-1
            self.__dir = -1
        if self.__i < 0:
            self.__i = 0
            self.__dir = 1
    
class Chaser(Enemy):
    __moveDir = {}
    __curLevel = 1 #to prevent multiple computation
    __BASE = 100 #to encode a pair of points as an integer.
    PASSABLE_BLOCKS = [cell.CT_GOAL, cell.CT_TELEPORTER, cell.CT_START, cell.CT_FLOOR]
    
    PAUSE_TIME = (11, 15) #Move PAUSE_TIME[0] times every PAUSE_TIME[1] frames -- PAUSE_TIME[0]/PAUSE_TIME[1] times the max speed of the sprite
    
    """An enemy which slowly chases after the sprite, using the shortest distance possible."""
    def __init__(self, startPt, grid, curLevel):
        """startPt is the starting position of this enemy.
Grid is required to initialize its level map to get the adjacency matrices for djikstra"""
        super(Chaser, self).__init__(startPt[0], startPt[1], CHASER, grid[0][0].size, Chaser.PASSABLE_BLOCKS)
        Chaser.__BASE = max(len(grid), len(grid[0])) + 1
        if Chaser.__curLevel != curLevel:
            Chaser.setMovementDict(grid)
            Chaser.__curLevel = curLevel
        self.countTime = rd.randrange(0, Chaser.PAUSE_TIME[1])
        self.lastDir = (0, 0)
        l = range(0, Chaser.PAUSE_TIME[1])
        rd.shuffle(l)
        self.moveTimes = l[:Chaser.PAUSE_TIME[0]]

    @staticmethod
    def __getCode(x1, y1, x2, y2, b = -1):
        """Gets an integer code in base representation b, of the form x1 y1 x2 y2
If b <= 0 b defaults to Chaser.__BASE"""
        if b <= 0:
            b = Chaser.__BASE
        c1 = x1*b + y1
        c2 = x2*b + y2
        return (c1 * b * b) + c2
    
    @staticmethod
    def setMovementDict(grid):
        """Set Chaser.__moveDir to a dictionary which maps two points on the level grid to a (dx, dy) direction tuple.
This tuple tells the sprite which way to move."""
        rows = len(grid)
        cols = len(grid[0])
        Chaser.__moveDir.clear()
        #Get all possible points that it is possible to go on:
        allPts = []
        for i in xrange(1, rows-1):
            for j in xrange(1, cols-1):
                if grid[i][j].blocktype in Chaser.PASSABLE_BLOCKS:
                    allPts.append((i, j))
        #Do BFS starting from each
        left = (0, -1)
        right = (0, 1)
        up = (-1, 0)
        down = (1, 0)
        noDir = (0, 0)
        for sx, sy in allPts:
            #Keep track of which direction to move from source (sx, sy) to reach (i, j)
            gotBy = [[None for j in xrange(cols)] for i in xrange(rows)]
            gotBy[sx][sy] = noDir
            queue = []
            for d in (left, right, up, down):
                x = sx+d[0]
                y = sy+d[1]
                if grid[x][y].blocktype in Chaser.PASSABLE_BLOCKS:
                    gotBy[x][y] = d
                    queue.append((x, y))
                    Chaser.__moveDir[Chaser.__getCode(sx, sy, x, y)] = d
            while queue != []:
                x, y = queue[0]
                del queue[0]
                for d in (left, right, up, down):
                    x1 = x + d[0]
                    y1 = y + d[1]
                    if grid[x1][y1].blocktype in Chaser.PASSABLE_BLOCKS and gotBy[x1][y1] == None:
                        queue.append((x1, y1))
                        gotBy[x1][y1] = gotBy[x][y]
                        Chaser.__moveDir[Chaser.__getCode(sx, sy, x1, y1)] = gotBy[x][y]

    @staticmethod
    def getMoveDir():
        return Chaser.__moveDir

    def move(self, grid, sprite):
        """find which direction to move"""
        if self.countTime in self.moveTimes:
            sx, sy = self.loc
            ex, ey = sprite.loc
            code = Chaser.__getCode(sx, sy, ex, ey)
            dx, dy = self.lastDir
            try:
                dx, dy = Chaser.__moveDir[code]
            except KeyError:
                if not self.canGo(grid[sx+dx][sy+dy]):
                    dx = 0
                    dy = 0
            self.loc[0] += dx
            self.loc[1] += dy
            self.lastDir = (dx, dy)
        self.countTime = (self.countTime+1)%Chaser.PAUSE_TIME[0]

if __name__ == '__main__':
    gridS = """WWWWW
W W W
W W W
W   W
WWWWW"""
    print gridS
    gridS = gridS.split('\n')
    grid = [[cell.Cell(x, y, 50, gridS[x][y]) for y in xrange(len(gridS[0]))] for x in xrange(len(gridS))]
    c = Chaser((1, 1), grid)
    print Chaser.getMoveDir()
