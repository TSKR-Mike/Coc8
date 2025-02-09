import pygame
import sys
import random
# 初始化 Pygame
pygame.init()
from statistics import Message_window
m = Message_window()
# 创建窗口
screen = pygame.display.set_mode((640, 480))
pygame.display.set_caption('获取窗口焦点示例')

# 游戏主循环
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        # 可以添加其他事件处理代码
        if event.type == pygame.KEYDOWN:
            m.error('1')
    # 填充背景色
    screen.fill((255, 255, 255))
    # 更新屏幕显示
    pygame.display.flip()

pygame.quit()
sys.exit()