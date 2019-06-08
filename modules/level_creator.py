if __name__ != '__main__':
    raise ImportError("Cannot import this module.")

import pygame as pg
import textgraphics as tg
import cell
import colours as cl
import button as bt
import event_handler as eh

n = eh.getLevelsInfo(importer = eh.MOD_LEVELCREATOR)[2]
n += 1
print "LEVEL EDITOR: LEVEL %d"%n
print """
Instructions:
0. Beware, no error handling done AT ALL!!
1. Enter the rows, cols and the cellsize the level should default to.
2. Click on the buttons to choose what to place.
3. Click on a particular cell on the grid to place the item.
4. If required, scroll through the grid using arrow keys.
4. Follow all messages (if any) that are present after the 'Current Code' indicator.
5. Press exit to close the editing. The program will then process the information and print out the formatted text containing the level information.
"""

rows = int(raw_input("Enter number of rows: "))
cols = int(raw_input("Enter number of cols: "))
cellsize = int(raw_input("Enter default size of the cells: "))

width = 1000
height = 600
display = pg.display.set_mode((width, height))
pg.display.set_caption("LEVEL EDITOR: level %d"%n)
clock = pg.time.Clock()

order = ('.', 'S', 'G', 'W', 'B', 'H', 'E', 'T', 'P', 'C')
x = 20
bl = []
for c in order:
    bl.append(bt.Button(x, height - 50, 40, 40, c.upper()))
    x += 50

bannersize = 100

size = max(min(width/cols, (height - bannersize)/rows), 20)
grid = [[cell.Cell(x, y, size, 'W', debug = True) for y in xrange(cols)] for x in xrange(rows)]
qt = False
s = '.'
maxRowFit = min(1 + (height - bannersize)/size, rows)
maxColFit = min(1 + width/size, cols)

specialBlocks = []
blockInfoRequired = 0

numTeleportPairs = 0 #For the correct numbering of teleports

enemies = []
enemyInfoRequired = 0

origin = [0, 0]
specialMessage = ""

while True:
    for event in pg.event.get():
        if eh.checkQuit(event):
            if blockInfoRequired != 0:
                specialMessage = "PLACEMENT OF LAST SPECIAL BLOCK INCOMPLETE!!!"
            if enemyInfoRequired != 0:
                pass
            else:
                qt = True
                break
        elif event.type == pg.MOUSEBUTTONDOWN:
            x, y = event.pos
            if x < 0 or x > width or y < 0 or y > height-bannersize:
                continue
            x -= origin[0]
            y -= origin[1]
            i = y/size
            j = x/size
            if 1 <= i <= rows - 2 and 1 <= j <= cols - 2:
                if s == 'T':
                    if blockInfoRequired == 0:
                        specialBlocks.append(['T', i, j, 0, 0])
                        specialMessage = "Please position the second teleport"
                        blockInfoRequired = 1
                        numTeleportPairs += 1
                    else:
                        specialBlocks[-1][-2] = i
                        specialBlocks[-1][-1] = j
                        specialMessage = ''
                        blockInfoRequired = 0
                    grid[i][j].changeCode('T', numTeleportPairs)
                elif s == 'P': #Patroller
                    if enemyInfoRequired == 0:
                        specialMessage = "Please click on ending point for Patroller"
                        enemies.append(['P', i, j, None, None])
                        enemyInfoRequired = 1
                    elif enemyInfoRequired == 1:
                        enemyInfoRequired = 0
                        specialMessage = ''
                        enemies[-1][3] = i
                        enemies[-1][4] = j
                        print 'PATROLLER PLACED AT:', enemies[-1]
                elif s == 'C': #Chaser
                    enemies.append(['C', i, j])
                    print 'CHASER PLACED AT:', enemies[-1]
                else:
                    grid[i][j].changeCode(s.replace('.', ' '))
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP:
                origin[1] += size
            elif event.key == pg.K_DOWN:
                origin[1] -= size
            elif event.key == pg.K_RIGHT:
                origin[0] -= size
            elif event.key == pg.K_LEFT:
                origin[0] += size
    
    if qt: break

    if origin[0] > 0: origin[0] = 0
    elif cols*size >= width:
        origin[0] = max(origin[0], width - cols*size)
        
    if origin[1] > 0: origin[1] = 0
    elif rows*size >= height and origin[1] < height - bannersize - rows*size:
        origin[1] = height - rows*size - bannersize 

    if enemyInfoRequired == 0 and blockInfoRequired == 0:
        for btn in bl:
            temp = btn.get_click(bt.RETURN_TEXT)
            if temp != None:
                s = temp
                break
    
    display.fill(cl.WHITE)
    posx = abs(origin[0]//size)
    posy = abs(origin[1]//size)
    for col in grid[posy:posy+maxRowFit]:
        for b in col[posx:posx+maxColFit]:
            b.blit(display, origin = origin)
    tly = -origin[0]/size
    tlx = -origin[1]/size
    tg.message_to_screen(display, "Current topleft cell: (%d,%d); Current code: %s ; %s" % (tlx, tly, s, specialMessage),
                         cl.RED, (width/2, height - 70),
                     size = 30, bold = True)
    
    for b in bl: b.blit(display)
    pg.display.flip()
    clock.tick(20)

pg.quit()

mapstr = ""
for i in xrange(rows):
    for j in xrange(cols):
        if isinstance(grid[i][j], bt.Button):
            grid[i][j] = cell.Cell(i, j, size, ' ')
        mapstr += cell.Cell.num_code[grid[i][j].blocktype]
    mapstr += '\n'
mapstr += "%d\n"%len(specialBlocks)
for t in specialBlocks:
    s = " ".join(map(str, t))
    mapstr += "%s\n"%s

mapstr += "%d\n"%len(enemies)    
for t in enemies:
    s = " ".join(map(str, t))
    mapstr += "%s\n"%s
    
print "Your map:"
print mapstr

ch = raw_input("SAVE THIS LEVEL? (n for no and anything else for yes): ").lower()
if ch == 'n':
    quit()

with open(eh.getLevelFolder(eh.MOD_LEVELCREATOR)+"level_%d_info.litxt"%n, 'w') as f:
    f.write("%d %d %d\n" %(rows, cols, cellsize))
    f.write(mapstr)
eh.setLevelsInfo(totalLevels = n, importer = eh.MOD_LEVELCREATOR)
