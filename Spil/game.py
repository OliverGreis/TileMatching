import random
from os import path
import pygame
import os


class Game():



    def __init__(self):
        self.grid = [[random.randint(1,5) for y in range(0,10)] for x in range(0,10)]
        self.anim = [[0 for y in range(0,10)] for x in range(0,10)]
        self.point = 0
        self.moves = 10
        self.highscore = 0
        self.highscore2 = 0
        self.d = 0
        #print(self.grid)
        print(self.grid[1][1])
        self.running = True
        self.dir = path.dirname('highscore.txt')
        self.dir2 = path.dirname('highscore2.txt')
        self.bombe = False
    def build_grid(self):
        #import pdb; pdb.set_trace()
        for x in range(0, len(self.grid)):
            for y in range(0, len(self.grid)):
                if self.grid[x][y] == 0:
                    if y < len(self.grid[x])-1 and not all(self.grid[x][yy] == 0 for yy in range(y, len(self.grid[x]))):
                        # Flyt kolonnen ned
                        while(self.grid[x][y] == 0):
                            self.grid[x][y:] = self.shift_column(self.grid[x][y:], 1)
                            self.anim[x][y:] = [50 for i in range(y,len(self.anim[x]))]
                    # Fyld op med nye tiles
                    for fill in range(0,len(self.grid[x])):
                        if self.grid[x][fill] == 0:
                            self.grid[x][fill] = random.randint(1,5)

    def load_data(self):

        with open(os.path.join(self.dir, 'highscore.txt'), 'r+') as f:
            try:
                self.highscore = int(f.read())
            except:
                self.highscore = 0

    def load_data2(self):

       with open(os.path.join(self.dir2, 'highscore2.txt'), 'r+') as f:
           try:
               self.highscore2 = int(f.read())
           except:
               self.highscore2 = 0


    def show_go_screen(self):
        if not self.running:
            return
        if self.point > self.highscore:
            self.highscore = self.point
        else:
                return

    def show_go_screen2(self):
            if self.highscore > self.highscore2:
                self.highscore2, self.highscore = self.highscore, self.highscore2
            else:
                    return

            with open(path.join(self.dir2,  "highscore2.txt"), 'r+') as f:
                f.write(str(self.highscore2))
            with open(path.join(self.dir,  "highscore.txt"), 'r+') as f:
                f.write(str(self.highscore))


    def shift_column(self, l, n):
        return l[n:] + l[:n]


    def swap_tiles(self, x1, y1, x2, y2):
        #Sørg for, at vi kun kan bytte naboceller.
        if abs(x1-x2) <= 1 and abs(y1-y2) <= 1:
            self.grid[x1][y1], self.grid[x2][y2] = self.grid[x2][y2], self.grid[x1][y1]
            self.moves = self.moves - 1

    def detect_bombe(self, auto = False):
        for x in range(1, len(self.grid)-1):
            for y in range(0, len(self.grid)):
                if self.grid[1][1] == 6:
                    self.grid[x-1][y] = 0
                    self.grid[x][y] = 0
                    self.grid[x+1][y] = 0
                    self.grid[x][y+1] = 0
                    self.grid[x][y-1] = 0
                    self.grid[x+1][y+1] = 0
                    self.grid[x+1][y-1] = 0
                    self.grid[x-1][y+1] = 0
                    self.grid[x-1][y-1] = 0
                    self.point = self.point+9
                    self.bombe = True
                    self.build_grid()



    def detect_horizontal_matches(self, auto = False):
        for x in range(1, len(self.grid)-1):
            for y in range(0, len(self.grid)):


                #Detect horizontal match
                if self.grid[x][y] == self.grid[x-1][y] and self.grid[x][y] == self.grid[x+1][y]:
                    if self.grid[x][y] == self.grid[x-1][y] and self.grid[x][y] == self.grid[x+1][y] and self.grid[x-2][y] or self.grid[x+2][y] :
                        self.grid[1][1] = 6
                    c = self.grid[x][y]
                    self.grid[x-1][y] = 0
                    self.grid[x][y] = 0
                    self.grid[x+1][y] = 0
                    pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                    self.point = self.point + 1 #Hvis match detected få point til at stige med en
                    x1 = x+2
                    #Er der flere end tre brikker i træk?
                    while x1 < len(self.grid) and self.grid[x1][y] == c:
                        self.grid[x1][y] = 0
                        x1 += 1
                    #Hvis vi har fjernet brikker, skal pladen fyldes igen
                        self.point = self.point + 1
                    self.build_grid()





    def detect_vertical_matches(self, auto = False):
        for x in range(0, len(self.grid)):
            for y in range(1, len(self.grid)-1):

            #Detect horizontal match
                if self.grid[x][y] == self.grid[x][y-1] and self.grid[x][y] == self.grid[x][y+1]:
                    c = self.grid[x][y]
                    self.grid[x][y-1] = 0
                    self.grid[x][y] = 0
                    self.grid[x][y+1] = 0
                    pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                    self.point = self.point+1
                    y1 = y+2
                    #Er der flere end tre brikker i træk?
                    while y1 < len(self.grid) and self.grid[x][y1] == c:
                        self.grid[x][y1] = 0
                        y1 += 1

                    #Hvis vi har fjernet brikker, skal pladen fyldes igen
                        self.point = self.point + 1
                    self.build_grid()





#Knap til reset
    def Reset(self):
        self.point = 0
        self.moves = 10
        self.__init__()
