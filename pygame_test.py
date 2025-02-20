import pygame
import sys
pygame.init()
from statistics import Message_window
m = Message_window()
screen = pygame.display.set_mode((640, 480))

m.select_file(dir='ComplexFiles')
pygame.quit()
sys.exit()
