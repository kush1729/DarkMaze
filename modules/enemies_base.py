import cell
import pygame as pg

import os
folder = os.getcwd().rstrip("\\/")
if folder[-7:] == 'modules':
    folder = folder[:-7].rstrip("\\/")
folder += "\\images\\"

PATROLLER = 1
CHASER = 2

enemyinfo = {
PATROLLER : "This monster just moves in a fixed line path, and bounces around between some two fixed points.",
CHASER : "This monster slowly chases after the sprite. It knows the exact position of the sprite and also knows the exact layout of the maze. Thus, it isn't safe to get caught in a deadend by this monster.",
-1:None #So that i dont have to keep scrolling through and find the commas
}


class Enemy(object):
    """Base class for any specific enemy class"""
    Code_strToInt = {'P':PATROLLER, 'C':CHASER}
    Code_intToStr = {PATROLLER:'P', CHASER:'C'}

    @staticmethod
    def getNumCode(c):
        if isinstance(c, str):
            c = Enemy.Code_strToInt[c]
        return c
    
    def __init__(self, x, y, enemytype, cellsize, allowedCells = []):
        """x and y are the grid coordinates for blitting. Enemytype is the code type, used for getting the image
Cellsize is the size of the cells being used in the level. Used for getting the image to correct size.

allowedCells is a sequence of cell type codes from cell module. These are the cells that the enemy can move on.
cell.CT_FLOOR and cell.CT_ENEMY_HAVEN are automatically included, so there is no need to mention it in the allowedCells parameter."""
        self.loc = [x, y]
        self.type = Enemy.getNumCode(enemytype)
        if self.type not in Enemy.Code_strToInt.values():
            raise ValueError("No such enemy exists")
        try:
            self.rawimage = pg.image.load("%senemy-%d.png"%(folder, self.type))
        except:
            self.rawimage = pg.Surface((cellsize-2, cellsize-2))
        self.image = self.__getImage(cellsize)
        self.blitwidth, self.blitheight = self.image.get_size()
        for c in (cell.CT_FLOOR, cell.CT_ENEMY_HAVEN):
            if c not in allowedCells:
                allowedCells.append(c)
        self.allowed = sorted(allowedCells)
        self.__cellsize = cellsize
        
    def __getImage(self, size):
        rwd, rht = self.rawimage.get_size()
        scale = float(size)/float(max(rwd, rht))
        w = int(rwd*scale)-2 #Avoid cell margins
        h = int(rht*scale)-2
        return pg.transform.scale(self.rawimage, (w, h))
    
    def blit(self, surface, origin = (0, 0)):
        """blit the sprite onto the surface, with reference to the origin.
The origin should be a point on the surface object, and not grid indices"""
        cx = origin[0] + self.loc[1] * self.__cellsize 
        cy = origin[1] + self.loc[0] * self.__cellsize
        blitx = cx + ((self.__cellsize - self.blitwidth)/2)
        blity = cy + ((self.__cellsize - self.blitheight)/2)
        surface.blit(self.image, (blitx, blity))
        
    def move(self, grid, sprite):
        """Each sub class of Enemy must define their own move method, as this defines the basic nature of the enemy.
The function signature must be exactly the same."""
        raise NotImplementedError("Method 'move' for Enemy %s is undefined"%Enemy.Code_intToStr[self.type])

    def checkKill(self, sprite):
        return (sprite.canDie and self.loc[0] == sprite.loc[0] and self.loc[1] == sprite.loc[1])
    
    def canGo(self, cell):
        b = 0
        e = len(self.allowed) - 1
        celltype = cell.blocktype
        while b <= e:
            m = b + (e-b)//2
            if self.allowed[m] == celltype: return True
            elif self.allowed[m] < celltype: b = m+1
            else: e = m-1
        return False
    
    def findPath(self, grid, startPt, endPt):
        """Returns the path of least distance from the grid index startPt to the grid index endPt
Both startPt and endPt must be a (row_index, col_index) tuple.
This method is implemented using BFS"""
        startPt = tuple(startPt)
        ex, ey = endPt
        del endPt
        rows = len(grid)
        cols = len(grid[0])
        queue = [startPt]
        visitedFrom = []
        for i in xrange(rows):
            visitedFrom.append([])
            for j in xrange(cols):
                if self.canGo(grid[i][j]): #allowed to move on this cell
                    visitedFrom[-1].append(None) #Not visited Yet
                else: #this cell not allowed
                    visitedFrom[-1].append((-1, -1))
        visitedFrom[startPt[0]][startPt[1]] = startPt
        while queue != []:
            x, y = queue[0]
            del queue[0]
            if x == ex and y == ey:
                break
            for dx, dy in ((1, 0), (-1, 0), (0, 1), (0, -1)):
                if 0 < x+dx < rows and 0 < y+dy < cols and visitedFrom[x+dx][y+dy] == None:
                    queue.append((x+dx, y+dy))
                    visitedFrom[x+dx][y+dy] = (x, y)
        if visitedFrom[ex][ey] in (None, (-1, -1)):
            raise ValueError("endPt (%d, %d) is not reachable from startPt (%d, %d)."%(ex, ey,
                                                                                       startPt[0], startPt[1]))
        x = ex
        y = ey
        path = []
        while visitedFrom[x][y] != (x, y):
            path.append((x, y))
            x, y = visitedFrom[x][y]
        path.append(startPt)
        return path[::-1] #Reverse it so path[0] == startPt
