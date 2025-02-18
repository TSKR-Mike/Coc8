import pygame
import sys
pygame.init()
from statistics import Message_window
m = Message_window()
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('获取窗口焦点示例')

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    screen.fill((255, 255, 255))
    pygame.display.flip()
pygame.quit()
sys.exit()
