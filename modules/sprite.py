import pygame as pg
import colours as cl

import os
folder = os.getcwd().rstrip("\\/")
if folder[-7:] == 'modules':
    folder = folder[:-7].rstrip("\\/")
folder += "\\images\\"

class Sprite(object):
    def __init__(self, moveleft = pg.K_LEFT, moveright = pg.K_RIGHT, moveup = pg.K_UP, movedown = pg.K_DOWN):
        """moveleft, moveright, moveup and movedown are keyboard buttons that user will use to control the sprite."""
        self.__rawimage = pg.image.load(folder+"robot-sprite.png")
        self.__rawWd, self.__rawHt = self.__rawimage.get_size()
        self.__ml = moveleft
        self.__mr = moveright
        self.__mu = moveup
        self.__md = movedown
        self.canDie = True

    def levelInit(self, loc, cellsize):
        """Method that preps the Sprite before a Level.
Needs to be called before the start of a level.
loc is the index position in the level.Level.grid matrix.
cellsize is the size of the cells being used (for image resizing purposes)"""
        self.loc = list(loc)
        self.__cellsize = cellsize
        if self.__rawWd > self.__rawHt:
            scalar = float(cellsize)/float(self.__rawWd)
        else:
            scalar = float(cellsize)/float(self.__rawHt)
        w = int(self.__rawWd*scalar)
        h = int(self.__rawHt*scalar)
        self.blitwidth = w - 2 #to avoid the cell boundary margins
        self.blitheight = h - 2
        self.blitimage = pg.transform.scale(self.__rawimage, (self.blitwidth, self.blitheight))
    
    def move(self, grid, dx = 0, dy = 0):
        """Moves the sprite in the grid, by moving it dx cells up/down and dy cells left/right, in the level.Level.grid matrix
Negative dx is for upward movement and negative dy is for leftward movement.
As diagonal movement not allowed, horizontal movement shall be preferred, unless it is not allowed.

This method returns True if the location of the sprite has changed."""
        if dx != 0 and grid[self.loc[0]+dx][self.loc[1]].isPassable(self):
            self.loc[0] += dx
            return True
        if dy != 0 and grid[self.loc[0]][self.loc[1]+dy].isPassable(self):
            self.loc[1] += dy
            return True
        return False

    def getUserInput(self, grid, keystate):
        """Move the sprite depending on the keyboard input, and return True if the sprite moved, and False otherwise.
grid is the level.Level.grid matrix.
keystate is the pygame.key.get_pressed() list"""
        return self.move(grid, (keystate[self.__md] - keystate[self.__mu]), (keystate[self.__mr] - keystate[self.__ml]))

    def changeControl(self, moveleft = None, moveright = None, moveup = None, movedown = None):
        """To change the keyboard controls for moving the sprite.
If a particular control is left as None, then that control does not change."""
        if moveleft != None:
            self.__ml = moveleft
        if moveright != None:
            self.__mr = moveright
        if moveup != None:
            self.__mu = moveup
        if movedown != None:
            self.__md = movedown

    def blit(self, surface, origin = (0, 0)):
        """blit the sprite onto the surface, with reference to the origin.
The origin should be a point on the surface object, and not grid indices"""
        cx = origin[0] + self.loc[1] * self.__cellsize 
        cy = origin[1] + self.loc[0] * self.__cellsize
        blitx = cx + ((self.__cellsize - self.blitwidth)/2)
        blity = cy + ((self.__cellsize - self.blitheight)/2)
        surface.blit(self.blitimage, (blitx, blity))
