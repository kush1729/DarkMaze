import pygame as pg
import colours as cl
import textgraphics as tg #For blitting identifier
import random as rd

#Number according to order of appearance on instructions
CT_WALL = 0
CT_FLOOR = 1
CT_GOAL = 3
CT_START = 2
CT_TELEPORTER = 7
CT_HAVEN = 5
CT_ENEMY_HAVEN = 6
CT_BROKEN_WALLS = 4

blockinfo = {
CT_WALL:"WALLS : These blocks form the walls of the maze. The robot cannot go through these walls.",
CT_FLOOR:"FLOORS : The Robot can travel in these blocks, however so can everything else that can move.",
CT_START:"STARTING POINT: The Robot starts here at this block. Only the Robot can occupy this space.",
CT_GOAL:"THE GOLD: The Robot must get this, by occupying that cell. Once the Robot reaches this cell, the level is complete.",
CT_TELEPORTER:"TELEPORTERS: These cells transport the Robot from one to another. Each teleporter is connected with another unique teleporter, and they send the Robot only between themselves. These are labelled with numbers to identify the pairs.",
CT_HAVEN:"SAFE SPOTS: These cells are not accessible to any monster. These are safe havens for the Robot.",
CT_ENEMY_HAVEN:"MONSTER PATHS: These cells are accessible to any monster, but not to the Robot.",
CT_BROKEN_WALLS:"BROKEN WALLS: These cells look like walls, but are accessible to the Robot. As this is a broken wall, it disappears briefly at regular intervals.",
-1:'' #Dummy 
}

class Cell(object):

    BROKEN_WALL_INTERVAL = (3, 50) 
    EDGE_COLOUR = cl.BLACK
    #Cell types that require number identifiers to be blitted onto it must have light colours
    colour_dict = {CT_WALL : cl.BROWN, CT_FLOOR : cl.WHITE, CT_GOAL : cl.GOLD, CT_START : cl.GREEN,
                   CT_TELEPORTER : cl.BLUE, CT_HAVEN : cl.PINK, CT_ENEMY_HAVEN : cl.LIGHTGREY,
                   CT_BROKEN_WALLS : cl.BROWN}
    char_code = {'W' : CT_WALL, ' ' : CT_FLOOR, 'G' : CT_GOAL, 'S' : CT_START, 'T' : CT_TELEPORTER, 'H': CT_HAVEN,
                 'E' : CT_ENEMY_HAVEN, 'B' : CT_BROKEN_WALLS}
    num_code = {CT_WALL : 'W', CT_FLOOR : ' ', CT_GOAL : 'G', CT_START : 'S', CT_TELEPORTER : 'T', CT_HAVEN : 'H',
                CT_ENEMY_HAVEN : 'E', CT_BROKEN_WALLS : 'B'}
    
    def __init__(self, x, y, size, blocktype = CT_FLOOR, num_id = None, debug = False):
        """x and y are the indices of the cell in the level.Level.grid matrix
x denotes the row and y denotes the column.
num_id is an unique identifier for this cell, and is used for teleportation/door-key functionality.
Preferably should be left as None. Any non None value will be blitted
The debug attribute is for cells which are active during the game, to indicate that these cells should become easier to identify/work with for the user."""
        self.x = x
        self.y = y
        self.size = size
        if isinstance(blocktype, str):
            blocktype = Cell.char_code[blocktype]
        if blocktype not in Cell.num_code.keys():
            raise ValueError("No such cell exists")
        self.__colour = Cell.colour_dict[blocktype]
        self.blocktype = blocktype
        self.id = num_id
        self.__debug = debug
        
    def blit(self, surface, origin = (0, 0), leveltime = 0):
        """Blits the cell onto the surface, with reference to the origin.
The origin should be a point on the surface object, and not the cell indices."""
        x = origin[0] + self.y * self.size #as self.y refers to column
        y = origin[1] + self.x * self.size #as self.x referse to row
        cell_colour = self.__colour
        text = self.id
        if self.blocktype == CT_BROKEN_WALLS:
            if self.__debug:
                text = 'B'
            int_a = Cell.BROKEN_WALL_INTERVAL[0]
            int_b = Cell.BROKEN_WALL_INTERVAL[1]
            if leveltime % int_b >= int_b - int_a:
                cell_colour = Cell.colour_dict[CT_FLOOR]
        pg.draw.rect(surface, cell_colour, (x, y, self.size, self.size))
        pg.draw.rect(surface, Cell.EDGE_COLOUR, (x, y, self.size, self.size), 1)
        if text != None:
            tg.text_to_button(surface, str(text), cl.BLACK, (x, y, self.size, self.size), 4*self.size // 5, True)

    def changeCode(self, blocktype, num_id = None):
        """To change the type of cell.
blocktype and num_id are same as that in the __init__ method"""
        if isinstance(blocktype, str):
            blocktype = Cell.char_code[blocktype]
        self.__colour = Cell.colour_dict[blocktype]
        self.blocktype = blocktype
        self.id = num_id
        self.timeCount = 0

    def isPassable(self, sprite):
        """Checks if the sprite can move through this cell.
Return True if yes and False if not.
sprite.Sprite object is passed for future functionality..."""
        if self.blocktype in (CT_WALL, CT_ENEMY_HAVEN):
            return False
        elif self.blocktype in (CT_FLOOR, CT_START, CT_GOAL, CT_TELEPORTER, CT_HAVEN, CT_BROKEN_WALLS):
            return True
    
    

if __name__ == '__main__':
    pg.init()
    screen = pg.display.set_mode((400, 400))
    clock = pg.time.Clock()
    c = Cell(1, 0, 20)
    while True:
        for e in pg.event.get():
            if e.type == pg.QUIT:
                pg.quit()
                quit()
        screen.fill(cl.RED)
        c.blit(screen)
        pg.display.flip()
        clock.tick(15)
