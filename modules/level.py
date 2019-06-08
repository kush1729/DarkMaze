import pygame as pg
import cell
import enemies as en
import colours as cl
#from os import getcwd

LEVELS_FOLDER = ".\\modules\\levels\\"
#del getcwd

class Level(object):
    def __init__(self, levelno = 0, cellsize = -1, darkened = 0):
        """Load the level levelno, from the files in the map folder
This function fully preps the level, and so must be called to start a new level
cellsize refers to the size of the individual cells, in pixels.
A negative value reverts cellsize to the default value given in the map file
The cellsize should remain between 10 and 50, otherwise strange behaviour is expected.
Also, the cellsize should divide both the display_width and display_height, otherwise strange behaviour is expected.
If darkened is a positive integer, then only a square of side length darkened centered at the sprite will be blitted,
and the rest will be black. If darkened <= 0, the entire grid visible will be shown."""
        self.darkened = darkened
        self.lvl = levelno
        
        with open(LEVELS_FOLDER + "level_%d_info.litxt"%self.lvl, "r") as f:
            
            #Prep map of the level:
            self.rows, self.cols, cs = map(int, f.readline().strip().split())
            if cellsize > 0:
                cs = cellsize
            self.grid = [[None for _ in xrange(self.cols)] for _ in xrange(self.rows)]
            for x in xrange(self.rows):
                row = f.readline().strip("\n")
                for y in xrange(self.cols):
                    self.grid[x][y] = cell.Cell(x, y, cs, row[y])
                    if self.grid[x][y].blocktype == cell.CT_START:
                        self.__start_Sprite = (x, y)
            self.cellsize = cs
            
            #For special Blocks Info:
            self.teleports = []
            numSpecial = int(f.readline())
            for i in xrange(numSpecial):
                #<block code> <other space seperated details>
                inp = f.readline().strip().split()
                blocktype = cell.Cell.char_code[inp[0]]
                inp = inp[1:]
                if blocktype == cell.CT_TELEPORTER:
                    x1, y1, x2, y2 = map(int, inp)
                    self.teleports.append((x1, y1, x2, y2))
                    self.grid[x1][y1].changeCode('T', i+1)
                    self.grid[x2][y2].changeCode('T', i+1)
            self.canTeleport = True

            #For enemy info:
            self.monsters = []
            self.numMonsters = int(f.readline())
            for i in xrange(self.numMonsters):
                #<enemy code> <other space seperated details>
                inp = f.readline().strip().split()
                enType = en.Enemy.getNumCode(inp[0])
                inp = inp[1:]
                if enType == en.PATROLLER:
                    sx, sy, ex, ey = map(int, inp)
                    #rest --> startX, startY, endX, endY
                    e = en.Patroller((sx, sy), (ex, ey), self.grid)
                elif enType == en.CHASER:
                    #C start_x start_y
                    start = tuple(map(int, inp))
                    e = en.Chaser(start, self.grid, self.lvl)
                else:
                    raise Exception("Cannot find the Enemy sub class with type %s"%inp[0])
                    
                self.monsters.append(e)
                
        self.__internalClock = 0 #To regulate monsters and dynamic cells.
            
        self.topmost = [0,0]  #grid indices

    @staticmethod
    def __getNextInput(s):
        if s != '':
            return int(s)
        return 0
            

    def centerScreen(self, width, height, spriteloc = None):
        """Centers the starting screen onto the sprite.
Has to be called at the beginning of the level.
Not calling it results in the screen starting at the topleft corner of the maze.
width and height are the width and height of the actual screen space dedicated to the maze.
spriteloc is the current location of the sprite. If None, it will default to the starting position of the sprite"""
        if spriteloc == None:
            spriteloc = self.__start_Sprite
        sx, sy = spriteloc
        numrows = height//self.cellsize
        numcols = width//self.cellsize
        self.topmost[0] = max(0, sx - numrows//2)
        self.topmost[1] = max(0, sy - numcols//2)

    def getStartSprite(self):
        """Returns the starting position for the sprite for the particular level"""
        return self.__start_Sprite

    def getOrigin(self):
        return (- self.topmost[1] * self.cellsize, - self.topmost[0] * self.cellsize)

    def checkwin(self, sprite):
        """Check if the sprite has won the level"""
        sx, sy = sprite.loc
        if self.grid[sx][sy].blocktype == cell.CT_GOAL:
            return True
        return False

    def checklost(self, sprite):
        for i in xrange(self.numMonsters):
            if self.monsters[i].checkKill(sprite):
                return True
        x, y = sprite.loc
        if not self.grid[x][y-1].isPassable(sprite) and not self.grid[x][y+1].isPassable(sprite) and \
           not self.grid[x-1][y].isPassable(sprite) and not self.grid[x+1][y].isPassable(sprite):
            return True
        return False

    def blitBoard(self, surface, display_width, display_height, spriteloc = (-1, -1)):
        """Method to blit the entire grid on surface
The display_width and display_height are used to figure out how much of the board should be shown.

sprite loc is required if the board is to be darkened"""
        origin = self.getOrigin()
        #The below 4 variables are used to refer to indices, for sublists.
        numcols = (display_width / self.cellsize)
        numrows = (display_height / self.cellsize)
        if self.darkened <= 0:
            lefti = self.topmost[1]
            righti = lefti + numcols + 1 #for safety
            upi = self.topmost[0]
            downi = upi + numrows + 1 #for safety
        else:
            lefti = max(0, spriteloc[1] - (self.darkened//2))
            righti = min(spriteloc[1] + (self.darkened//2), self.cols+1)
            upi = max(0, spriteloc[0] - (self.darkened//2))
            downi = min(spriteloc[0] + (self.darkened//2), self.rows+1)
        pg.draw.rect(surface, cl.BLACK, (0, 0, display_width, display_height))
        for row in self.grid[upi:downi+1]:
            for cell in row[lefti:righti+1]:
                cell.blit(surface, origin, self.__internalClock)
        self.__internalClock += 1

    def blitMonsters(self, surface, spriteloc):
        """Method that blits all the monsters of the level, if any.
spriteloc is used if the level is in dark mode, and also if it is required by the monsters.blit method."""
        dx = self.darkened//2
        for i in xrange(self.numMonsters):
            if self.darkened <= 0 or ((spriteloc[0]-dx <= self.monsters[i].loc[0] <= spriteloc[0]+dx) and \
                                      (spriteloc[1]-dx <= self.monsters[i].loc[1] <= spriteloc[1]+dx)):
                self.monsters[i].blit(surface, self.getOrigin())

    def moveMonsters(self, sprite, period = 1):
        """Method that moves the monsters, if any.
The period parameter is used to regulate the movement of the monsters, by actually moving them every period times this method is called."""
        if self.__internalClock % period == 0:
            for i in xrange(self.numMonsters):
                self.monsters[i].move(self.grid, sprite)
    
    def checkScroll(self, spriteloc, disp_width, disp_height):
        """return False if the sprite is visible to the user, and (dx, dy) if it is not, where dx and dy define how to scroll"""
        if 1 > spriteloc[0] - self.topmost[0]: #The sprite is above the screen
            return (-1, 0)
        if 1+spriteloc[0] >= self.topmost[0] + (disp_height/self.cellsize): #The sprite is below the screen
            return (1, 0)
        if 1 > spriteloc[1] - self.topmost[1]: #The sprite is left of the screen
            return (0, -1)
        if 1+spriteloc[1] >= self.topmost[1] + (disp_width/self.cellsize): #The sprite is right of the screen
            return (0, 1)
        return False

    def scrollBoard(self, display_width, display_height, dx = 0, dy = 0):
        """scrolls through the board, by moving dx cells up or down, and dy cells left or right.
Here, dx and dy refer to changes in the index of Level.grid, and NOT pygame.Surface references"""
        self.topmost[0] += dx
        self.topmost[1] += dy
        self.topmost[0] = min(max(0, self.topmost[0]), self.rows-(display_height/self.cellsize))
        self.topmost[1] = min(max(0, self.topmost[1]), self.cols-(display_width/self.cellsize))

    def scroll(self, spriteloc, disp_width, disp_height):
        """Scroll through the board, by checking the position of the sprite.
If there is no need to scroll, it will not."""
        ret = self.checkScroll(spriteloc, disp_width, disp_height)
        if isinstance(ret, tuple):
            self.scrollBoard(disp_width, disp_height, 2*ret[0], 2*ret[1])

    def specialCells(self, sprite, width, height):
        """Method to implement special cells such as teleports etc.
width and height are required to center the screen onto the sprite, in case"""
        sx, sy = sprite.loc
        if self.grid[sx][sy].blocktype == cell.CT_TELEPORTER:
            if self.canTeleport:
                i = self.grid[sx][sy].id - 1
                self.canTeleport = False #to prevent multiple teleports at once
                if self.teleports[i][:2] == (sx, sy):
                    nx, ny = self.teleports[i][2:]
                else:
                    nx, ny = self.teleports[i][:2]
                sprite.loc = [nx, ny]
                self.centerScreen(width, height, (nx, ny))
        else:
            self.canTeleport = True

if __name__ == '__main__':
    import colours as cl
    pg.init()
    wd = 400
    ht = 400
    screen = pg.display.set_mode((wd, ht))
    clk = pg.time.Clock()
    lvl = Level(0)
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT or (e.type == pg.KEYDOWN and e.key == pg.K_ESCAPE):
                pg.quit()
                quit()
            if e.type == pg.KEYDOWN:
                if e.key == pg.K_UP:
                    lvl.scrollBoard(wd, ht, -1, 0)
                elif e.key == pg.K_DOWN:
                    lvl.scrollBoard(wd, ht, 1, 0)
                elif e.key == pg.K_LEFT:
                    lvl.scrollBoard(wd, ht, 0, -1)
                elif e.key == pg.K_RIGHT:
                    lvl.scrollBoard(wd, ht, 0, 1)
        screen.fill(cl.LIGHTBLUE)
        lvl.blitBoard(screen, wd, ht)
        pg.display.flip()
        clk.tick(20)
