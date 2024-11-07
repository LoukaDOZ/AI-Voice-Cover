from gui.app import VoiceCoverApp
import pygame as pg
import pygame.mixer as mixer

if __name__ == "__main__":
    pg.init()
    mixer.init()
    
    vc = VoiceCoverApp()
    vc.run()