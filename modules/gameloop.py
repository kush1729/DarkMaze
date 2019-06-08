import level
import sprite as sp
import colours as cl
import event_handler as eh
import pygame as pg
import time
import textgraphics as tg
import button as bt

def playLevel(display, disp_width, disp_height, bannersize = 150):
    """game loop to actually play the level levelno"""
    levelno, unlocked, maxlevels = eh.getLevelsInfo()
    clock = pg.time.Clock()
    
    lvl = level.Level(levelno, darkened = 5)
    lvl.centerScreen(disp_width, disp_height-bannersize)
    player = sp.Sprite()
    player.levelInit(lvl.getStartSprite(), lvl.cellsize)

    MONSTER_MOVEMENT_PERIOD = 4
    
    bannerTextc = cl.GOLDENROD

    HEADER_BANNER_SIZE = 50
    banner_xpos = disp_width//2# - 50
    banner_ypos = disp_height - bannersize + HEADER_BANNER_SIZE//2 + 5
    LEVEL_TIMER_SIZE = 30
    timer_xpos = disp_width//2 #- 50
    timer_ypos = disp_height - bannersize + 10 + HEADER_BANNER_SIZE + LEVEL_TIMER_SIZE//2

    btnwidth = disp_width - 40
    btnht = 40
    btnx = 20
    btny = disp_height - btnht - 10
    backBtn = bt.Button(btnx, btny, btnwidth, btnht, text = "BACK", border = True)
    
    startTime = time.time()

    playerwon = False
    paused = False
    pausetime = 0
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
            if event.type == pg.KEYDOWN and event.key == pg.K_p:
                paused = not paused
                if paused:
                    pausetime = time.time()
        if paused:
            startTime += (time.time() - pausetime)
            pausetime = time.time()
            
        #Functional Stuff:
        #lvl.centerScreen(disp_width, disp_height-bannersize, player.loc)
        if not paused:
            lvl.specialCells(player, disp_width, disp_height-bannersize)
            
            keystate = pg.key.get_pressed() 
            player.getUserInput(lvl.grid, keystate)
            lvl.scroll(player.loc, disp_width, disp_height - bannersize)
            lvl.moveMonsters(player, MONSTER_MOVEMENT_PERIOD)
            
        if backBtn.get_click():
            return eh.FC_MAINMENU
        #Display Stuff:
        display.fill(eh.BACKGROUND_COLOUR)
        lvl.blitBoard(display, disp_width, disp_height - bannersize, player.loc)
        player.blit(display, lvl.getOrigin())
        lvl.blitMonsters(display, player.loc)
        #banner:
        pg.draw.rect(display, eh.BACKGROUND_COLOUR, (0, disp_height-bannersize, disp_width, bannersize))
        tg.message_to_screen(display, "LEVEL %d - %dx%d grid"%(levelno, lvl.rows, lvl.cols), bannerTextc,
                             (banner_xpos, banner_ypos), size = HEADER_BANNER_SIZE, bold = True)
        s = "PAUSE" if not paused else "RESUME"
        tg.message_to_screen(display, ("TIME TAKEN: %s  PRESS P TO %s" % (getTimeStamp(startTime), s)), bannerTextc,
                             (timer_xpos, timer_ypos), LEVEL_TIMER_SIZE)
        backBtn.blit(display)
        
        pg.display.flip()
        clock.tick(eh.FPS)
        
        #Check win:
        if lvl.checkwin(player):
            playerwon = True
            break
        if lvl.checklost(player):
            playerwon = False
            break
        
    #GAME OVER STUFF:
    tstamp = getTimeStamp(startTime)
    if playerwon:
        unlocked = min(unlocked + 1, maxlevels)
        eh.setLevelsInfo(maxUnlocked = unlocked)
        if levelno == maxlevels:
            return gameover(display, disp_width, disp_height, tstamp)
        else:
            return winpage(display, disp_width, disp_height, tstamp, levelno)
    else:
        return losspage(display, disp_width, disp_height, tstamp)

def getTimeStamp(startTime):
    """get the time as a formatted string"""
    timetaken = int(time.time() - startTime)
    m = timetaken // 60
    s = timetaken % 60
    if s < 10: sstr = "0" + str(s)
    else: sstr = str(s)
    return "%d:%s"%(m, sstr)

def winpage(display, width, height, timestamp, level):
    backcolour = cl.PINK
    clock = pg.time.Clock()
    gap = 20
    btnwd = width//2 - gap - gap//2
    btnht = (height//2 - 3*gap)//2
    btny1 = height//2
    btny2 = 3*height//4
    btnx1 = gap
    btnx2 = width - gap - btnwd
    nextlevel = bt.Button(btnx1, btny1, btnwd, btnht, "NEXT LEVEL", cl.GREEN, cl.GOLD, border = True)
    playagain = bt.Button(btnx2, btny1, btnwd, btnht, "PLAY AGAIN", cl.BLUE, cl.LIGHTBLUE, border = True)
    levelmenu = bt.Button(btnx1, btny2, btnwd, btnht, "LEVEL MENU", cl.RED, cl.ORANGE, border = True)
    quitbtn = bt.Button(btnx2, btny2, btnwd, btnht, "EXIT", cl.DARKGREY, cl.LIGHTGREY, textcolour = cl.WHITE, border = True)
    headersize = 70
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
        if nextlevel.get_click():
            eh.setLevelsInfo(curLevel = level+1)
            return eh.FC_PLAYLEVEL
        if playagain.get_click():
            return eh.FC_PLAYLEVEL
        if levelmenu.get_click():
            return eh.FC_LEVELMENU
        if quitbtn.get_click():
            return eh.FC_QUIT
        display.fill(backcolour)
        tg.message_to_screen(display, "YOU WON! :)", cl.GOLDENROD, (width//2, 3*gap), size = headersize, bold = True)
        tg.message_to_screen(display, "TIME: %s"%timestamp, cl.CYAN, (width//2, 4*gap + headersize//2),
                             size = headersize//2)
        nextlevel.blit(display)
        playagain.blit(display)
        levelmenu.blit(display)
        quitbtn.blit(display)
        pg.display.flip()
        clock.tick(eh.FPS)

def losspage(display, width, height, timestamp):
    backcolour = cl.ORANGE
    clock = pg.time.Clock()
    gap = 20
    btnwd = (width//3) - gap
    btny = height // 2
    btnht = btny - gap
    playagain = bt.Button(gap, btny, btnwd, btnht, "PLAY AGAIN?", cl.GREEN, cl.GOLD, border = True)
    quitbtn = bt.Button(width-btnwd-gap, btny, btnwd, btnht, inactive = cl.DARKGREY, active = cl.LIGHTGREY,
                        textcolour = cl.WHITE, border = True)
    levelmenu = bt.Button((width-btnwd)//2, btny, btnwd, btnht, "LEVEL MENU", border = True)
    headersize = 75
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
        if playagain.get_click():
            return eh.FC_PLAYLEVEL
        if levelmenu.get_click():
            return eh.FC_LEVELMENU
        if quitbtn.get_click():
            return eh.FC_QUIT
        display.fill(backcolour)
        tg.message_to_screen(display, "YOU LOST :(", cl.RED, (width//2, 4*gap), size = headersize, bold = True)
        tg.message_to_screen(display, "TIME: %s"%timestamp, cl.CYAN, (width//2, 5*gap + headersize//2),
                             size = headersize//2)
        playagain.blit(display)
        levelmenu.blit(display)
        quitbtn.blit(display)
        pg.display.flip()
        clock.tick(eh.FPS)

def gameover(display, width, height, timestamp):
    backcolour = cl.GOLD
    clock = pg.time.Clock()
    gap = 20
    btnwd = (width//3) - gap
    btny = height // 2
    btnht = btny - gap
    mainmenu = bt.Button(gap, btny, btnwd, btnht, "MAIN MENU", cl.GREEN, cl.GOLD, border = True)
    quitbtn = bt.Button(width-btnwd-gap, btny, btnwd, btnht, inactive = cl.DARKGREY, active = cl.LIGHTGREY,
                        textcolour = cl.WHITE, border = True)
    playagain = bt.Button((width-btnwd)//2, btny, btnwd, btnht, "PLAY AGAIN", cl.ORANGE, cl.YELLOW, border = True)
    headersize = 70
    while True:
        for event in pg.event.get():
            if eh.checkQuit(event):
                return eh.FC_QUIT
        if playagain.get_click():
            return eh.FC_PLAYLEVEL
        if mainmenu.get_click():
            return eh.FC_MAINMENU
        if quitbtn.get_click():
            return eh.FC_QUIT
        display.fill(backcolour)
        tg.message_to_screen(display, "YOU WON!", cl.RED, (width//2, 2*gap), size = 2*headersize//3, bold = True)
        tg.message_to_screen(display, "GAMEOVER!!", cl.PURPLE, (width//2, 3*gap + headersize//2),
                             size = headersize, bold = True)
        tg.message_to_screen(display, "TIME: %s"%timestamp, cl.CYAN, (width//2, 4*gap + headersize),
                             size = headersize//2)
        playagain.blit(display)
        mainmenu.blit(display)
        quitbtn.blit(display)
        pg.display.flip()
        clock.tick(eh.FPS)
    
