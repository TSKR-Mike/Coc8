import pygame
import sys
from matrix import subWindow


class UsrNotice(subWindow):

    def __init__(self, window, loc, length, height, bkg_colour=(0, 191, 255), title='User Guide'):
        super().__init__(window, loc, length, height, bkg_colour=bkg_colour, title=title)
        self.font = pygame.font.Font('fonts/JetBrainsMono-Light.ttf')
        self.texts = []

        self.texts.append(
            self.font.render('                                Common Questions', True,
                             (0, 0, 0)))
        self.texts.append(self.font.render('1. About root', True, (0, 0, 0)))
        self.texts.append(
            self.font.render('     To use "root", you need to type the number of root BEFORE the "root" symbol,',
                             True, (0, 0, 0)))
        self.texts.append(self.font.render('     like "2root4" means ²√4, instead of 2*²√4',
                                           True, (150, 0, 0)))
        self.texts.append(self.font.render('2. Why is the window stuck?', True, (0, 0, 0)))
        self.texts.append(
            self.font.render('     Minimize all windows to look for unclosed warning/question/error windows',
                             True, (0, 0, 0)))
        self.texts.append(self.font.render('     , this will lead to the stuck of main loop.', True, (0, 0, 0)))
        self.texts.append(self.font.render('     (the windows will NOT show up in the quick bar)', True, (150, 0, 0)))
        self.texts.append(self.font.render('3. About "No-mouse" mode', True, (0, 0, 0)))
        self.texts.append(
            self.font.render('     The No-mouse mode is designed of the users who do NOT have mouse or keyboards', True,
                             (0, 0, 0)))
        self.texts.append(
            self.font.render('     so that they can better interact with charts in "complex" and "vector".', True,
                             (0, 0, 0)))
        self.texts.append(self.font.render('     If you have mouse and keyboard, you can ignore it.', True, (0, 0, 0)))
        self.texts.append(self.font.render('4. How to use matrix/complex/vector', True, (0, 0, 0)))
        self.texts.append(
            self.font.render('     Usually, select a file to insert data from it.You can find them in ',
                             True, (0, 0, 0)))
        self.texts.append(
            self.font.render('     /Coc<Type>Files or input the data manually and extract them later.',
                             True, (0, 0, 0)))
        self.texts.append(
            self.font.render('      The interact guide is on the the title bar.',
                             True, (0, 0, 0)))
        self.texts.append(self.font.render('5. How to insert data from Excel files', True, (0, 0, 0)))
        self.texts.append(self.font.render('     There is guide about how to load data in data science functions and matrix.', True, (0, 0, 0)))
        self.texts.append(
            self.font.render('     Follow the guide there.', True,
                             (0, 0, 0)))

    def draw(self):
        while True:
            pygame.draw.rect(self.window, self.bkg_colour, (self.loc[0], self.loc[1], self.length, self.height))

            for event in pygame.event.get():
                if self.cancel_button.handleEvent(event):
                    return
            self.title_bkg.draw()
            self.title_view.draw()
            self.cancel_button.draw()

            for obj, i in zip(self.texts, range(len(self.texts))):
                self.window.blit(obj, (0, 30 * i + 30))
            pygame.display.update()



if __name__ == '__main__':
    pygame.init()
    screen_width, screen_height = 1004, 610
    screen = pygame.display.set_mode((screen_width, screen_height))
    pygame.display.set_caption("Simple Pygame Window")
    a = UsrNotice(screen, (0, 0), 1004, 610)
    a.draw()

    pygame.quit()
    sys.exit()
