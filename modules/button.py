import pygame as pg
import colours as cl
import textgraphics as tg
import time

MOUSE_LEFT = 0
MOUSE_MIDDLE = 1
MOUSE_RIGHT = 2

class Clickable(object):
    def __init__(self, x, y, wd, ht):
        """x = xpos of top left corner,
y = ypos of top right corner,
wd = width of the object,
ht = height of the object"""
        self.x = x
        self.y = y
        self.wd = wd
        self.ht = ht
    def is_in(self, mpos):
        return (self.x <= mpos[0] <= self.x + self.wd) and \
               (self.y <= mpos[1] <= self.y + self.ht)
    def get_click(self, mouse = MOUSE_LEFT):
        """get_click(mouse = MOUSE_LEFT): return (mouse_x, mouse_y) if mouse has clicked inside the rectangle,
False if not.
mouse dictates which mouse click to choose.
pygame.event.get() needs to be called before this."""
        m = pg.mouse.get_pos()
        clicked = pg.mouse.get_pressed()[mouse]
        if not clicked: return False
        if self.is_in(m): return m
        else: return False

RETURN_TRUE = 0
RETURN_FALSE = 1
RETURN_TEXT = 2
RETURN_ACTION = 3
RETURN_MOUSEPOS = 4

BORDER_COLOUR = cl.BLACK

class Button(Clickable):

    TIME_DELAY_ON_CLICK = 0.1
    
    def __init__(self, x, y, wd, ht, text = "EXIT", inactive = cl.RED, active = cl.ORANGE,
                 textcolour = cl.BLACK, textsize = 25, border = False, activated = True):
        self.Rect = pg.Rect(x, y, wd, ht)
        super(Button, self).__init__(x, y, wd, ht)
        self.inactive = inactive
        self.active = active
        self.text = text
        self.textc = textcolour
        self.textsize = textsize
        self.border = border
        self.activated = activated
        
    def get_click(self, returnmode = RETURN_TRUE, mouse = MOUSE_LEFT, action = None):
        """get_click(returnmode = RETURN_TRUE, mouse = MOUSE_LEFT, action = None):
\t\treturn None if not clicked on button, else return something else.
Return value is dictated by returnmode and action. action should be None if returnmode != RETURN_ACTION
mouse dictates which mouse button to detect"""
        if not self.activated:
            return None
        ret = super(Button, self).get_click(mouse)
        #print 'Db:', ret
        if ret != False:
            time.sleep(Button.TIME_DELAY_ON_CLICK)
            if returnmode == RETURN_TRUE:
                return True
            elif returnmode == RETURN_FALSE:
                return False
            elif returnmode == RETURN_TEXT:
                return self.text
            elif returnmode == RETURN_ACTION:
                return action
            elif returnmode == RETURN_MOUSEPOS:
                return ret
        return None
    def blit(self, surface, update = False):
        """blit(surface, update = False)--> return None
surface should be the pygame.Surface object on which the button should be drawn on.
if update is true, then call pygame.display.update()
Should be called after pygame.event.get()"""
        if self.is_in(pg.mouse.get_pos()) and self.activated:
            c = self.active
        else:
            c = self.inactive
        pg.draw.rect(surface, c, self.Rect)
        if self.border:
            pg.draw.rect(surface, BORDER_COLOUR, self.Rect, 1)
        tg.text_to_button(surface, self.text, self.textc, self.Rect, self.textsize, True)
        if update:
            pg.display.update()
