import pygame as pg
pg.init()
import gameloop
import menus
import instructions
import colours as cl
from level import LEVELS_FOLDER

GAME_NAME = "THE MAZE"

BACKGROUND_COLOUR = cl.GREY
FPS = 20

def checkQuit(event):
    """Check if user wants to quit"""
    if event.type == pg.QUIT or (event.type == pg.KEYDOWN and event.key == pg.K_ESCAPE): 
        return True
    return False

MOD_LEVELCREATOR = 0
MOD_MAIN = 1

def getLevelFolder(importer = MOD_MAIN):
    if importer == MOD_LEVELCREATOR:
        folder = LEVELS_FOLDER.replace("\\modules", "")
    else:
        folder = LEVELS_FOLDER
    return folder

def getLevelsInfo(importer = MOD_MAIN):
    """Returns a tuple containing (current_level_played, maximum_level_unlocked, maximum_number_of_levels)"""
    folder = getLevelFolder(importer)
    with open(folder+"general_level_info.litxt", "r") as f:
        t = tuple(map(int, f.read().strip().split()))
    return t

def setLevelsInfo(curLevel = None, maxUnlocked = None, totalLevels = None, importer = MOD_MAIN):
    """Edits the text file containing the general level information. If argument is None, that particular value does not change."""
    t = getLevelsInfo(importer)
    curlevel = curLevel if curLevel != None else t[0]
    maxlvl = maxUnlocked if maxUnlocked != None else t[1]
    tot = totalLevels if totalLevels != None else t[2]
    folder = getLevelFolder(importer)
    with open(folder+"general_level_info.litxt", "w") as f:
        f.write("%d\n%d\n%d\n"%(curlevel, maxlvl, tot))

def Quit():
    pg.quit()
    quit()

#Codes to handle function calls
#Each function will return these codes to tell which function to call next
#Each function must return a tuple, where the first element is this 'Function Call' Code, and the rest
#of the tuple is other related info

FC_QUIT = 0
FC_LEVELMENU = 1
FC_MAINMENU = 2
FC_PLAYLEVEL = 3
FC_INSTRUCTIONS = 4

def executeMain(gameDisplay, width, height, startPage = FC_MAINMENU):
    code = startPage
    #Start:
    while code != FC_QUIT:
        if code == FC_PLAYLEVEL:
            code = gameloop.playLevel(gameDisplay, width, height)
        elif code == FC_LEVELMENU:
            code = menus.levelSelect(gameDisplay, width, height)
        elif code == FC_MAINMENU:
            code = menus.mainMenu(gameDisplay, width, height)
        elif code == FC_INSTRUCTIONS:
            code = instructions.instrPage(gameDisplay, width, height)
