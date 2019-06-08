import sys, os
sys.path.append(os.getcwd() + "\modules")
import pygame as pg
import traceback
import event_handler as eh
if __name__ == '__main__':
    try:
        #Init:
        width = 500
        height = 500
        gameDisplay = pg.display.set_mode((width, height))
        
        try:
            icon = pg.transform.scale(pg.image.load(".\\image\\robot-sprite.png"), (25, 25))
            pg.display.set_icon(icon)
        except: pass
        pg.display.set_caption(eh.GAME_NAME)    
        eh.executeMain(gameDisplay, width, height)
    except Exception as e:
        traceback.print_exc()
    finally:
        eh.Quit()


