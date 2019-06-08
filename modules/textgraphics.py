import pygame as pg

RAW_TEXT_FONT_SIZE = 100

def text_objects(text, colour, size, bold = False):
    """returns a text surface.
text must be a single line.
Size is the height of rectangle of the pygame.Surface object for the line of text"""
    textSurface = pg.font.SysFont("comicsansms", RAW_TEXT_FONT_SIZE, bold = bold).render(text, True, colour)
    w, h = textSurface.get_size()
    scalar = float(size) / float(h)
    textSurface = pg.transform.scale(textSurface, (int(w * scalar), size))
    return textSurface

def text_to_button(screen, msg, color, rect, size = 25, bold = False):
    """Prints text onto the center of the button.
rect is either a pygame.Rect object or a tuple constructor for the pygame.Rect object.
size is pixel height of the text object"""
    if not isinstance(rect, pg.Rect):
        rect = pg.Rect(*tuple(rect))
    textSurf = text_objects(msg, color, size, bold = bold)
    textRect = textSurf.get_rect()
    textRect.center = rect.center
    screen.blit(textSurf, textRect)

def message_to_screen(screen, msg, color, center_loc, size = 25, bold = False):
    """Blits text, centered at center_loc. size is pixel height of the text object"""
    textSurf = text_objects(msg, color, size, bold = bold)
    textRect = textSurf.get_rect()
    textRect.center = center_loc
    screen.blit(textSurf, textRect)
    return textRect

def getParagraph(msg, colour, width, backcolour, size = 25, bold = False, linespacing = 0, paraspacing = 15,
                 hyphenated = False):
    """Get a pygame.Surface text object to use for blitting, by left aligning the msg.
Used for blitting large paragraphs, constrained by width.
size is the pixel height for the text, and backcolour is the background colour.
linespacing is the pixel gap between consecutive lines, whereas paraspacing is the pixel gap between consecutive paragraphs
If hyphenated is True, then if word overflows the width it will append a '-' and carry over rest of word to next line
If False, the entire word will get carried over.

As this method may be memory and time inefficient [O(len(msg))] for large messages, should be called once before the while True loop.
Blit the surface directly onto the screen."""
    if msg == None or msg == '':
        msg = 'MESSAGE'
    def getSurf(c):
        return text_objects(c, colour, size, bold)
    
    tempSurf = pg.Surface((width, size*len(msg)))
    tempSurf.fill(backcolour)
    x = 0
    y = 0
    
    if hyphenated:
        hypSurf = getSurf('-') 
        hypwidth = hypSurf.get_width()
        n = len(msg)
        i = 0
        while i < n and hyphenated:
            if msg[i] == '\n':
                x = 0
                y += (size + paraspacing)
            else:
                t = getSurf(msg[i])
                dx = t.get_width() 
                if msg[i] in (" ", "") and x != 0: #change back
                    tempSurf.blit(t, (x, y))
                    x += dx
                else:
                    if (i < n-1 and not msg[i+1].isalnum()) or i == n-1:
                        #x + dx > width should not occur, due to hyphenating...
                        tempSurf.blit(t, (x, y))
                        x += dx
                    else: #i < n-1 and msg[i+1].isalnum() always True, if above is False
                        dx1 = max(hypwidth, getSurf(msg[i+1]).get_width())
                        if (x + dx + dx1) <= width:
                            tempSurf.blit(t, (x, y))
                            x += dx
                        elif (x + dx + dx1) > width and (x + dx) <= width: #space for only 1 character left
                            tempSurf.blit(hypSurf, (x, y))
                            x = width + 1
                            i -= 1
                        else: #x + dx > width
                            i -= 1
                            x += dx
            if x >= width:
                x = 0
                y += (size+linespacing)
            i += 1

    #if not hyphenated::
    if not hyphenated:
        #msg = msg.replace('\n', ' \n')
        wordSep = ".,/?\\-=!&;:"
        word = ""
        for c in msg:
            if c in wordSep or c.isspace() or c == '\n':
                if c == '\n':
                    tc = ''
                else:
                    tc = c
                t = getSurf((word+tc))
                dx = t.get_width()
                if x + dx > width:
                    x = 0
                    y += (size+linespacing)
                tempSurf.blit(t, (x, y))
                x += dx
                word = ""
            else:
                word += c
            if c == '\n':
                x = 0
                y += (size+paraspacing)
                c = ''
        
    if x == 0: height = y
    else: height = y + size
    surface = pg.Surface((width, height))
    surface.fill(backcolour)
    surface.blit(tempSurf, (0, 0))
    return surface

if __name__ == '__main__':
    WHITE = (255, 255, 255)
    BLACK = (0, 0, 0)
    RED = (255, 0, 0)
    pg.init()
    clk = pg.time.Clock()
    surface = pg.display.set_mode((400, 500))
    msg = """Get a pygame.Surface text object to use for blitting, by left aligning the msg.
Used for blitting large paragraphs, constrained by width
Size is the pixel height for the text, and backcolour is the background colour.
Linespacing is the pixel gap between consecutive lines, whereas paraspacing is the pixel gap between consecutive paragraphs.
If hyphenated is True, then if word overflows the width it will append a '-' and carry over rest of word to next line
If False, the entire word will get carried over

As this method may be memory and time inefficient [O(len(msg))] for large messages, should be called once before the while True loop.
Blit the surface directly onto the screen."""
    para = getParagraph(msg, BLACK, 400, RED, hyphenated = False)
    y = 0
    x = 0
    while True:
        for event in pg.event.get():
            if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE):
                pg.quit()
                quit()
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    y -= 5
                elif event.key == pg.K_DOWN:
                    y += 5
                elif event.key == pg.K_LEFT:
                    x -= 5
                elif event.key == pg.K_RIGHT:
                    x += 5
        surface.fill(WHITE)
        surface.blit(para, (x, y))
        pg.display.flip()
        clk.tick(20)
        
