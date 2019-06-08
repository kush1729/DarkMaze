import event_handler as eh
import pygame as pg
import textgraphics as tg
import colours as cl
import cell
import button as bt
import enemies as en

genmsgs = """The objective of this game is to help the Robot navigate the Maze, avoid all obstacles and find the golden treasure.

Use the arrow keys to move the Robot."""

genFontC = cl.GOLDENROD

def getEnemyHelpSurf(c, wd, bkc, blocksize = 40, gap = 10):
    w = wd - gap - blocksize
    textS = tg.getParagraph(en.enemyinfo[c], genFontC, w, bkc, 30, hyphenated = False)
    htext = textS.get_height()
    e = en.Enemy(0, 0, c, blocksize)
    ht = max(htext, blocksize)
    surf = pg.Surface((wd, ht))
    surf.fill(bkc)
    ey = (ht - blocksize)//2
    pg.draw.rect(surf, cell.Cell.colour_dict[cell.CT_FLOOR], (0, ey, blocksize, blocksize))
    e.blit(surf, (0, ey))
    surf.blit(textS, (gap+blocksize, (ht - htext)//2))
    return surf

def getBlockHelpSurf(btype, wd, bkc, blocksize = 40, gap = 10):
    w = wd - gap - blocksize
    textS = tg.getParagraph(cell.blockinfo[btype], genFontC, w, bkc, hyphenated = False)
    htext = textS.get_height()
    e = cell.Cell(0, 0, blocksize, blocktype = btype)
    ht = max(htext, blocksize)
    surf = pg.Surface((wd, ht))
    surf.fill(bkc)
    e.blit(surf, (0, (ht - blocksize)//2))
    surf.blit(textS, (gap+blocksize, (ht - htext)//2))
    return surf

def getHelpSurface(wd, bkc, spacing = 15):
    blocksize = 60
    gap = 20
    LEAVE_EXTRA_SPACE = 3*spacing//2
    
    allSurf = [tg.getParagraph(genmsgs, genFontC, wd, bkc, 35, hyphenated = False), 2*LEAVE_EXTRA_SPACE]
    blocks = "There are many different types of cells that could make up the Maze. They are:"
    allSurf.append(tg.getParagraph(blocks, genFontC, wd, bkc, 30, hyphenated = False))
    allSurf.append(LEAVE_EXTRA_SPACE)
    for c in sorted(cell.blockinfo.keys()):
        if c >= 0:
            allSurf.append(getBlockHelpSurf(c, wd, bkc, blocksize, gap))

    allSurf.append(2*LEAVE_EXTRA_SPACE)
    enemy_s = "There also many different monsters that live in the maze. Each monster has they're own unique behaviour, but all will kill you if they get you. You must try to avoid them at all costs. These monsters are:"
    allSurf.append(tg.getParagraph(enemy_s, genFontC, wd, bkc, 30, hyphenated = False))
    allSurf.append(LEAVE_EXTRA_SPACE)
    for c in sorted(en.enemyinfo.keys()):
        if c >= 0:
            allSurf.append(getEnemyHelpSurf(c, wd, bkc, blocksize, gap))
                                   
    ht = -spacing
    i = 0
    for i in xrange(len(allSurf)):
        if isinstance(allSurf[i], int):
            ht += allSurf[i]
        else:
            ht += (allSurf[i].get_height() + spacing)
    surf = pg.Surface((wd, ht))
    surf.fill(bkc)
    y = 0
    for i in xrange(len(allSurf)):
        if isinstance(allSurf[i], int):
            y += allSurf[i]
        else:
            surf.blit(allSurf[i], (0, y))
            y += allSurf[i].get_height() + spacing
    return surf, ht

def instrPage(display, width, height):
    gap = 10
    helpSurf, hsHt = getHelpSurface(width - 2*gap, eh.BACKGROUND_COLOUR)
    
    btnwd = 60
    scrollbtnheight = 30
    backbtnheight = 40
    bannerheight = 4*gap + 2*scrollbtnheight + backbtnheight
    btnx = width - gap - btnwd
    
    upbtn = bt.Button(btnx, gap, btnwd, scrollbtnheight, "/\\", textsize = scrollbtnheight//2, textcolour = cl.BLACK,
                      inactive = cl.LIGHTGREY, active = cl.WHITE)
    downbtn = bt.Button(btnx, bannerheight - gap - scrollbtnheight, btnwd, scrollbtnheight, "\\/",
                        textsize = scrollbtnheight, textcolour = cl.BLACK, inactive = cl.LIGHTGREY, active = cl.WHITE)
    backbtn = bt.Button(btnx, 2*gap+scrollbtnheight, btnwd, backbtnheight, "BACK", textsize = 20)
    
    textx = (width - btnwd - 2*gap)//2
    texty = bannerheight // 2
    textSize = bannerheight//2
    instrColour = cl.GOLD
    
    scrolly = bannerheight
    SHIFT = 10
    clock = pg.time.Clock()
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
            if event.type == pg.KEYDOWN:
                if event.key == pg.K_UP:
                    scrolly += SHIFT
                elif event.key == pg.K_DOWN:
                    scrolly -= SHIFT
        if upbtn.get_click():
            scrolly += SHIFT
        if downbtn.get_click():
            scrolly -= SHIFT
        if backbtn.get_click():
            return eh.FC_MAINMENU
        if scrolly + hsHt < height - gap:
            scrolly = height - hsHt - gap
        if scrolly > bannerheight:
            scrolly = bannerheight
        display.fill(eh.BACKGROUND_COLOUR)
        display.blit(helpSurf, (gap, scrolly))
        pg.draw.rect(display, eh.BACKGROUND_COLOUR, (0, 0, width, bannerheight))
        tg.message_to_screen(display, "INSTRUCTIONS", instrColour, (textx, texty), bold = True, size = textSize)
        upbtn.blit(display)
        downbtn.blit(display)
        backbtn.blit(display)
        pg.display.flip()
        clock.tick(eh.FPS)
        
