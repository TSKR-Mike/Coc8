import pygame
import pygwidgets

from ButtonMgr import RectButton
from choices_center import ChoiceCenter



class Levels_Agreements_Error(Exception):
    pass


class Choices_Texts_UnMatched(Exception):
    pass


class Choices_Loc_ERROR(Exception):
    pass


class CheckBox:
    """
    -------------------------------
    - develop time:2024-1-17  -----
    - version: v5.0  --------------
    -------------------------------
    """

    def __init__(self, choice_num, choices_text, max_choices, window, clock, first_x:int=None,
                 first_y:int=None, loc_list_x:list[int]=None, loc_list_y:list[int]=None, each_add_x:int=None, each_add_y:int=None,
                 button_color=((90, 90, 150), (0, 50, 100), (20, 0, 80)),
                 background_color=(120, 120, 150), auto_adjust=False,buttons_adjust_length=50,levels=None, drawFuncs:list=None, eventHandlerFuncs:list=None,
                 bkg_width_adj:int=300, bkg_height_adj:int=120, font_name:str=None, font_size:int=20,
                 button_border_width:int=0, button_border_color=(0, 0, 0)):
        """

        :param choice_num:     ┐
        :param choices_text:   │
        :param max_choices:    │
        :param first_x:        │
        :param first_y:        │─> all these agreements must be None if levels is not None
        :param loc_list_x:     │
        :param loc_list_y:     │
        :param each_add_x:     │
        :param each_add_y:     ┘
        :param levels: ((<choices_texts>,<choices_loc>,<max_num>,<values>,<first_x> = NONE,<first_y> = NONE,<each_add_x> = NONE
                        <each_add_y> = NONE,<choices_text_colours> = (0,0,0) (or list by the user),
                        <level_text> = NONE),...)
        levels must be separate for at least 40(each choice <= 3 chars), add a char(base on 3 chars) means distance between the levels adds 5.

        :param button_color:#up, over and down

        """
        # --------------ERRORsThrowing----------------------------------------#
        if levels is None:
            if choice_num != len(choices_text) and levels is None:
                raise Choices_Texts_UnMatched
            if (levels is None and (first_y is None or first_x is None) and (
                    loc_list_x is None or loc_list_y is None or each_add_x is None
                    or each_add_y is None)):
                raise Choices_Loc_ERROR
        else:
            for i in levels:  # levels is a temple that includes other temples
                if len(i) > 10 or len(i) < 4:  # 'i' is also a temple
                    raise Levels_Agreements_Error('the user input the wrong numbers of '
                                                  'agreements')
                elif len(i) > 4:
                    if ((i[4] is None) ^ (i[5] is None) ^ (i[6] is None) ^ (i[7] is None) ^ True) and type(i[1]) != list:
                        # it means that the user didn`t input the choices`loc either
                        # input the four agreements completely
                        raise Levels_Agreements_Error('the user didn`t input the choices`loc neither input the four '
                                                  'agreements completely')

        self.clock = clock
        self.font_name = font_name
        self.font_size = font_size
        if levels is None:
            self.choice_text = choices_text
            self.choice_num = choice_num
        self.max_choices = max_choices
        self.choices = []
        self.clicked_choices = []
        if levels is None:
            self.values = [False for i in range(choice_num)]
        self.button_up = button_color[0]
        self.button_over = button_color[1]
        self.button_down = button_color[2]
        self.background_color = background_color
        mode = 0
        if levels is None:
            if first_y is not None and first_x is not None:
                self.x = first_x
                self.y = first_y
                if each_add_x is not None and each_add_y is not None:
                    mode = 1
                else:
                    raise Choices_Loc_ERROR
            elif loc_list_x is not None and loc_list_y is not None:
                mode = 2
            else:
                if levels is None:
                    raise Choices_Loc_ERROR
            if mode == 1:
                for i, m in zip(range(choice_num), choices_text):
                    if type(m) != str:
                        raise TypeError

                    else:
                        o = pygwidgets.TextRadioButton(window, (self.x, self.y), text=self.choice_text[i], group=1,
                                                       fontName=self.font_name, fontSize=self.font_size)
                        self.choices.append(o)
                    self.x += each_add_x
                    self.y += each_add_y
            else:
                for i, m in zip(range(choice_num), choices_text):
                    if type(m) != str:
                        raise TypeError
                    else:
                        o = pygwidgets.TextRadioButton(window, (loc_list_x[i], loc_list_y[i]), text=self.choice_text[i],
                                                       group=1, fontName=self.font_name, fontSize=self.font_size)
                        self.choices.append(o)
            if mode == 1:
                if not auto_adjust:
                    cancel = RectButton('cancel', window, 100, self.x + 80, self.y + buttons_adjust_length, upColor=self.button_up,
                                        overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                        border_width=button_border_width, border_color=button_border_color)

                    done = RectButton('done', window, 100, self.x - 30, self.y + buttons_adjust_length, upColor=self.button_up,
                                      overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                      border_width=button_border_width, border_color=button_border_color)

                else:
                    cancel = RectButton('cancel', window, 100, self.x + 80, self.y + each_add_y * choice_num + buttons_adjust_length, upColor=self.button_up,
                                        overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                        border_width=button_border_width, border_color=button_border_color)

                    done = RectButton('done', window, 100, self.x - 30, self.y + each_add_y * choice_num + buttons_adjust_length, upColor=self.button_up,
                                      overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                      border_width=button_border_width, border_color=button_border_color)


            else:
                cancel = RectButton('cancel', window, 100, loc_list_x[-1] + 80, loc_list_y[-1] + buttons_adjust_length, upColor=self.button_up,
                                    overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                    border_width=button_border_width, border_color=button_border_color)

                done = RectButton('done', window, 100, loc_list_x[-1] - 30, loc_list_y[-1] + buttons_adjust_length, upColor=self.button_up,
                                  overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                  border_width=button_border_width, border_color=button_border_color)


        else:  # user set the levels
            if max(len(i) for i in levels) < 7:
                min_x = min([min(k) for k in [r[0] for r in [m[1] for m in levels]]])
                #                             ----              ----------------------
                #                           read x              read choices`loc(list<x,y>)
                max_x = max([max(k) for k in [r[0] for r in [m[1] for m in levels]]])
                min_y = min([min(k) for k in [r[1] for r in [m[1] for m in levels]]])
                max_y = max([max(k) for k in [r[1] for r in [m[1] for m in levels]]])
                cancel = RectButton('cancel', window, 100, min_x + 80, (max_y - min_y) + buttons_adjust_length, upColor=self.button_up,
                                    overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                    border_width=button_border_width, border_color=button_border_color)

                done = RectButton('done', window, 100, min_x - 30, (max_y - min_y) + buttons_adjust_length, upColor=self.button_up,
                                  overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                  border_width=button_border_width, border_color=button_border_color)

            elif type(levels[0][4]) == type(levels[0][5]) == type(levels[0][6]) == type(levels[0][7]) == int:
                # start x,y and each add x,y is filled
                all_xs, all_ys = [], []
                for l in levels:
                    curr_num = len(l[0])
                    curr_each_add_x = l[6]
                    curr_each_add_y = l[7]
                    curr_start_x = l[4]
                    curr_start_y = l[5]
                    for i in range(curr_num):
                        all_xs.append(curr_start_x+curr_each_add_x*i)
                        all_ys.append(curr_start_y+curr_each_add_y*i)
                min_x = min(all_xs)
                max_x = max(all_xs)
                min_y = min(all_ys)
                max_y = max(all_ys)

                cancel = RectButton('cancel', window, 100, min_x + 80, (max_y - min_y) + buttons_adjust_length, upColor=self.button_up,
                                    overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                    border_width=button_border_width, border_color=button_border_color)
                done = RectButton('done', window, 100, min_x - 30, (max_y - min_y) + buttons_adjust_length, upColor=self.button_up,
                                  overColor=self.button_over, downColor=self.button_down, fontName=self.font_name, fontSize=self.font_size,
                                  border_width=button_border_width, border_color=button_border_color)

            for i,num in zip(levels,range(len(levels))):
                if len(i) >= 8:
                    if type(i[4]) == type(i[5]) == type(i[6]) == type(i[7]) == int:
                        choices_texts = i[0]
                        f_x = i[4]
                        f_y = i[5]
                        add_x = i[6]
                        add_y = i[7]
                        text_colours = None
                        if len(i) == 10:
                            text_colours = i[8]
                        else:
                            if len(i) > 8:
                                if len(i[8]) == 3:
                                    text_colours = i[8]
                                elif len(i) == 9:
                                    text_colours = [(0,0,0) for a in range(len(choices_texts))]
                            else:
                                text_colours=(0, 0, 0)
                        if text_colours is None:
                            new = ChoiceCenter(window, None, choices_texts, i[3], len(choices_texts),
                                       firstlocX=f_x,firstlocY=f_y,eachAddX=add_x,eachAddY=add_y, fontName=self.font_name, fontSize=self.font_size)
                        else:
                            new = ChoiceCenter(window, None, choices_texts, i[3],
                                           len(choices_texts), firstlocX=f_x, firstlocY=f_y, eachAddX=add_x, eachAddY=add_y,text_color=text_colours
                                               , fontName=self.font_name, fontSize=self.font_size)
                        self.choices.append(new)
                else:
                    choices_texts = i[0]
                    max_num = i[2]
                    loc = [(x, y) for x,y in i[1]]
                    if len(i) == 6:
                        text_colours = i[3]
                        new = ChoiceCenter(window, loc, choices_texts,i[3],len(choices_texts),max_num
                                           ,text_color=text_colours, fontName=self.font_name, fontSize=self.font_size)
                    else:
                        if len(i) > 4:
                            if len(i[4][0]) == 3:
                                text_colours = i[3]
                                new = ChoiceCenter(window, loc, choices_texts,i[3],len(choices_texts),max_num
                                               ,text_color=text_colours, fontName=self.font_name, fontSize=self.font_size)
                            else:
                                text_colours = [(0,0,0) for a in range(len(choices_texts))]
                                new = ChoiceCenter(window, loc, choices_texts,i[3],len(choices_texts),max_num
                                               ,text_color=text_colours, fontName=self.font_name, fontSize=self.font_size)
                        else:
                            new = ChoiceCenter(window, loc, choices_texts, i[3],
                                               len(i[0]), max_num, fontName=self.font_name, fontSize=self.font_size)
                    self.choices.append(new)
        Quit = False
        while not Quit:
            for event in pygame.event.get():
                if eventHandlerFuncs is not None:
                    for func in eventHandlerFuncs:
                        func(event)
                click_choice = None
                if levels is None:
                    for i, loc in zip(self.choices, range(len(self.choices))):
                        if i.handleEvent(event):
                            click_choice = loc
                            if self.values[loc]:
                                self.values[loc] = False

                            else:
                                self.values[loc] = True
                    for i, loc in zip(self.choices, range(len(self.choices))):
                        i.setValue(self.values[loc])
                    for i, loc in zip(self.choices, range(len(self.choices))):
                        if self.values[loc] is True and loc not in self.clicked_choices:
                            self.clicked_choices.append(loc)
                    for i, loc in zip(self.choices, range(len(self.choices))):
                        if self.values[loc] is False and loc in self.clicked_choices:
                            del self.clicked_choices[self.clicked_choices.index(self.choices.index(i))]
                    while len(self.clicked_choices) > self.max_choices:
                        if click_choice is not None:
                            del self.clicked_choices[0]
                    for i, loc in zip(self.choices, range(len(self.choices))):
                        if loc not in self.clicked_choices:
                            i.setValue(False)
                        else:
                            i.setValue(True)
                    for i, loc in zip(self.values, range(len(self.values))):
                        if i is True:
                            if loc not in self.clicked_choices:
                                self.values[loc] = False
                            else:
                                self.values[loc] = True
                        else:
                            if loc in self.clicked_choices:
                                self.values[loc] = True
                            else:
                                self.values[loc] = False
                else:
                    self.clicked_choices = []
                    for i in self.choices:
                        i.check_values(event)
                        self.clicked_choices.append(i.clicked_choices)
                #-----------------------------------------------------------------
                if drawFuncs is not None:
                    for func in drawFuncs:
                        func()
                #backGround.draw()
                if levels is None:

                    if mode==1:
                        pygame.draw.rect(window, (100, 100, 100, 128),
                                         (first_x-45, first_y-25, abs(first_x - self.x) + bkg_width_adj, abs(first_y - self.y) + bkg_height_adj), 0, 3)
                        pygame.draw.rect(window, background_color,
                                         (first_x - 50, first_y - 30, abs(first_x - self.x) + bkg_width_adj,
                                          abs(first_y - self.y) + bkg_height_adj), 0, 3)
                    else:
                        pygame.draw.rect(window, (100, 100, 100, 128),
                                         (first_x - 45, first_y - 25, abs(first_x - self.x) + bkg_width_adj,
                                          abs(first_y - self.y) + bkg_height_adj), 0, 3)
                        pygame.draw.rect(window, background_color,
                                         (first_x - 50, first_y - 30, abs(first_x - max(loc_list_x)) + bkg_width_adj,
                                          abs(first_y - max(loc_list_y)) + bkg_height_adj), 0, 3)
                else:
                    pygame.draw.rect(window, (100, 100, 100, 128),
                                        (min_x - 45, min_y - 25, abs(max_x - min_x) + bkg_width_adj,
                                        abs(max_y - min_y) + bkg_height_adj), 0, 3)
                    pygame.draw.rect(window, background_color,
                                        (min_x - 50, min_y - 30, abs(max_x - min_x) + bkg_width_adj,
                                        abs(max_y - min_y) + bkg_height_adj), 0, 3)
                if cancel.handleEvent(event):
                    self.clicked_choices = 'cancel'
                    Quit = True
                if done.handleEvent(event):
                    Quit = True
                for i in self.choices:
                    i.draw()
                cancel.draw()
                done.draw()
                pygame.display.update()
                self.clock.tick()


if __name__ == '__main__':
    import sys

    all_statistic_types = ['mean', 'max', 'min', 'standard deviation', 'mode', 'variance',
                           'median', 'range', 'percentile', 'skew', 'kurtosis', 'correlation', 'covariance',
                           'moving average', 'Exponential-Weighted-Moving-Average', 'Z-scores',
                           'Cumulative Distribution Function',
                           'Probability Density Function', 'MAD', 'M2', 'info entropy', 'auto-correlation',
                           'Jackknife-statistics', 'frequency count', 'Median Absolute Deviation Ratio',
                           'linear-trend', 'trimmed-mean', 'F statistic', 'T statistic', 'P statistic',
                           'coefficient of variation', 'Pearson correlation coefficient']

    window = pygame.display.set_mode((1004, 610))
    clock = pygame.time.Clock()
    pygame.init()
    n = pygwidgets.TextButton(window, (300, 400), 'test')
    #analyse_choice = CheckBox(32, all_statistic_types, 32,
    #                          window, clock, first_x=50, first_y=30, each_add_x=0, each_add_y=15, auto_adjust=False,
    #                          buttons_adjust_length=40, bkg_width_adj=400,
    #                          background_color=(90, 90, 150), font_name='fonts/JetBrainsMono-Light.ttf', font_size=15)
    while True:
        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            window.fill((0, 191, 255))
            pygame.display.update()
            if n.handleEvent(event):
                charting_sigma_selector = CheckBox(4, ['1 sigma', '2 sigma', '3 sigma', 'mean'], 4,
                                                   window, clock, first_x=40, first_y=100, each_add_x=0, each_add_y=20,
                                                   buttons_adjust_length=0, background_color=(90, 90, 150), font_name='fonts/JetBrainsMono-Light.ttf',font_size=18,
                                                   button_border_color=(110, 110, 170), button_border_width=1)
            n.draw()
            pygame.display.update()
            clock.tick(30)
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
