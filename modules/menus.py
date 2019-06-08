import pygame as pg
import button as bt
import textgraphics as tg
import colours as cl
import event_handler as eh

def getButtonList(dwidth, maxunlocked, totalLevels):
    y = 100
    bsize = 90
    gap = 20
    
    numPerRow = (dwidth - gap) // (gap + bsize)
    #dwidth = leftGap (x) + rightGap (x) + numPerRow * bsize + (numPerRow - 1) * gap 
    leftGap = (dwidth - (numPerRow * bsize) - ((numPerRow - 1) * gap)) // 2
    x = leftGap
    blist = []
    for l in xrange(1, 1+totalLevels):
        if l <= maxunlocked:
            act = True
            ic = cl.RED
            ac = cl.ORANGE
            tc = cl.BLACK
        else:
            act = False
            ac = cl.WHITE
            ic = cl.DARKGREY
            tc = cl.LIGHTGREY
            
        blist.append(bt.Button(x, y, bsize, bsize, "LEVEL %d"%l, active = ac, inactive = ic,
                               textsize = 20, textcolour = tc, activated = act))
        x += (bsize + gap)
        if l % numPerRow == 0:
            x = leftGap
            y += (bsize + gap)
    return blist, numPerRow

def levelSelect(display, dwidth, dheight):
    """Menu for selecting the levels"""
    curlvl, maxunlock, total = eh.getLevelsInfo()
    clock = pg.time.Clock()
    levelbuttons, numPerRow = getButtonList(dwidth, maxunlock, total)
    gap = 20
    btnht = 40
    backbtn = bt.Button(gap, dheight-btnht-gap, dwidth - 2*gap, btnht, "MAIN MENU", cl.BLUE, cl.LIGHTBLUE, border = True)
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
        if backbtn.get_click():
            return eh.FC_MAINMENU
        for b in levelbuttons:
            t = b.get_click(returnmode = bt.RETURN_TEXT)
            if t != None:
                l = int(t.lstrip("LEVEL "))
                eh.setLevelsInfo(curLevel = l)
                return eh.FC_PLAYLEVEL
        display.fill(eh.BACKGROUND_COLOUR)
        tg.message_to_screen(display, "LEVEL SELECT", cl.GOLDENROD, (dwidth//2, 50), 60, True)
        for b in levelbuttons:
            b.blit(display)
        backbtn.blit(display)
        pg.display.flip()
        clock.tick(eh.FPS)

def mainMenu(display, width, height):
    clock = pg.time.Clock()
    gap = 20
    btnwd = width//3 - 3*gap//2
    btnht = height//2 - 2*gap
    btny = height - btnht - 3*gap
    ts = 40
    levels = bt.Button(gap, btny, btnwd, btnht, "LEVELS", cl.GOLD, cl.YELLOW, textsize = ts, border = True)
    instr = bt.Button((width - btnwd)//2, btny, btnwd, btnht, "HELP", cl.GREEN, cl.GREENYELLOW, textsize = ts, border = True)
    quitbtn = bt.Button(width - gap - btnwd, btny, btnwd, btnht, "EXIT", cl.DARKGREY, cl.GREY, textsize = ts, border = True,
                        textcolour = cl.LIGHTGREY)
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
        if levels.get_click():
            return eh.FC_LEVELMENU
        if instr.get_click():
            return eh.FC_INSTRUCTIONS
        if quitbtn.get_click():
            return eh.FC_QUIT
        display.fill(eh.BACKGROUND_COLOUR)
        tg.message_to_screen(display, "WELCOME TO", cl.RED, (width//2, 2*gap), 50, True)
        tg.message_to_screen(display, eh.GAME_NAME.upper(), cl.GOLD, (width//2, 3*gap+50), 100, True)
        levels.blit(display)
        instr.blit(display)
        quitbtn.blit(display)
        pg.display.flip()
        clock.tick(eh.FPS)
