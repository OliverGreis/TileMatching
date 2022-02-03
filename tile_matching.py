import pygame
from game import Game
from os import path
import os

# Setup pygame
pygame.init()
screen = pygame.display.set_mode((800, 600))#, pygame.FULLSCREEN)
myfont = pygame.font.SysFont("comic sans", 20)
clock = pygame.time.Clock()
color = (255,255,255)
# Initialize game variables
done = False
game = Game()
current_tile = (3,3)
effects = []
# tile vars
tile_colors = [(0,0,0), (255,0,0), (0,255,0), (0,0,255), (255,255,0), (0,255,255),(0,0,0),(255,255,255)]
tile_offset = [280,530]
tile_size = [50,50]
menu_img = pygame.image.load('menu.png')
play_img = pygame.image.load('play.png')
reset_img = pygame.image.load('reset.png')
trophy_img = pygame.image.load('trophy.png')
start_img = pygame.image.load('Startskærm.png')

pygame.mixer.init()
Sang = pygame.mixer.Sound("Spilsang.wav")
Sang.set_volume(0.3)
Sang.play(-1)

#Tegner Spil
def draw_game():
    pygame.draw.rect(screen, (53,53,53),pygame.Rect(0,0,800,600))
    if current_tile is not None:
        t = abs((pygame.time.get_ticks() % 512) - 256) % 256
        c = (t,t,t)
        pygame.draw.rect(screen, c, pygame.Rect(tile_offset[0] + current_tile[0]*tile_size[0] - 3, tile_offset[1] - (current_tile[1]+1)*tile_size[1] - 3, tile_size[0], tile_size[1]))
    for y in range(0,len(game.grid)):
        for x in range(0,len(game.grid[y])):
            if game.anim[x][y] > 0:
                game.anim[x][y] -= 1
                if game.anim[x][y] == 0:
                    game.detect_horizontal_matches(True)
                    game.detect_vertical_matches(True)
            pygame.draw.rect(screen, tile_colors[game.grid[x][y]], pygame.Rect(tile_offset[0] + x*tile_size[0], tile_offset[1] - (y+1)*tile_size[1] - game.anim[x][y], tile_size[0]-5, tile_size[1]-5))
            screen.blit(myfont.render("Du har {} point ".format(game.point), 0, (255,255,255)), (50,50))
            screen.blit(myfont.render("Du har {} træk tilbage".format(game.moves), 0, (255,255,255)), (50,100))
            color = (255,0,0)





#Tegner Menu

def draw_menu():
    screen.fill((53,53,53))
    screen.blit(myfont.render("Mit spil", 100, (192,192,192)), (100,50))
    play_button.draw()
    trophy_button.draw()
    start_button.draw()


#Tegner highscore side

def draw_highscore():
    screen.blit(myfont.render("Highscore er:", 100, (192,192,192)), (150,125)) #Highscore titel
    screen.blit(myfont.render(str(game.highscore2), 100, (192,192,192)), (350,125)) #Highscore nr.1
    screen.blit(myfont.render(str(game.highscore), 100, (192,192,192)), (350,250)) #Highscore nr.2





def pixels_to_cell(x,y):
    x1 = int((x - tile_offset[0])/tile_size[0])
    y1 = int((-y + tile_offset[1])/tile_size[1])
    return x1,y1

def cell_to_pixels(x,y):
    x1 = int(tile_offset[0] + x * tile_size[0])
    y1 = int(tile_offset[1] - y * tile_size[1])
    return x1,y1
#Opretter spil side

def output_logic(tilstand):
    if tilstand == 1:
        draw_game()
        reset_button.draw()
        menu_button.draw()
#Opretter menu side

def menu(tilstand):
    if tilstand == 2:
        game.bombe = False
        draw_menu()
#Opretter highscore side

def highscore(tilstand):
    if tilstand == 3:
        game.load_data()
        game.load_data2()
        game.show_go_screen()
        game.show_go_screen2()
        screen.fill((0,0,0))
        draw_highscore()


tilstand = 2

#Opretter knapper klasse
class Button():
    #Opretter knappens variabler
    def __init__(self,x,y,image,scale):
        width = image.get_width()
        height = image.get_height()
        self.image = pygame.transform.scale(image,(int(width*scale),int(height*scale)))
        self.rect = self.image.get_rect()
        self.rect.topleft = (x,y)
    #Tegner knappen
    def draw(self):
        screen.blit(self.image,(self.rect.x,self.rect.y))

#Laver de forskellige knapper

menu_button = Button(50,150,menu_img,0.2)
play_button = Button(50,450,play_img,0.2)
reset_button = Button(150,150,reset_img,0.2)
trophy_button = Button(150,450,trophy_img,0.2)
start_button = Button(50,50,start_img,0.45)
mouse_pos = pygame.mouse.get_pos()



#Main game loop
while not done:
    for event in pygame.event.get():
        if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
            done = True




        #Håndtering af input fra mus
        if tilstand == 1 and event.type == pygame.MOUSEBUTTONDOWN:
            pos = pygame.mouse.get_pos()
            x_cell, y_cell = pixels_to_cell(pos[0],pos[1])
            print(pos, cell_to_pixels(x_cell,y_cell))
            for i in range(0,10):
                for j in range(0,10):
                    if x_cell == i and y_cell == j:
                        game.detect_bombe()

            if 0 <= x_cell < len(game.grid) and 0 <= y_cell < len(game.grid[0]):
                if current_tile is None:
                    current_tile = (x_cell, y_cell)
                else:
                    game.swap_tiles(x_cell, y_cell, current_tile[0], current_tile[1])

                    #Når der er byttet brikker, kan vi kontrollere om der er lavet et match
                    game.detect_vertical_matches()
                    game.detect_horizontal_matches()
                    current_tile = None

            if 150 < pygame.mouse.get_pos()[0] < 230 and 150 < pygame.mouse.get_pos()[1] < 230:
                    pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                    game.Reset()
            if 50 < pygame.mouse.get_pos()[0] < 130 and 150 < pygame.mouse.get_pos()[1] < 230:
                screen.fill((53,53,53))
                pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                tilstand = 2

        #Hvis på spil side og ikke flere træk, gå til hovedmenu
        if tilstand == 1 and game.moves == 0:
            screen.fill((53,53,53))
            game.Reset()



        #Hvis på hovedmenuen og mus bliver trykket
        if tilstand == 2 and event.type == pygame.MOUSEBUTTONDOWN:

            #Hvis mus er på Spil
            if 50 < pygame.mouse.get_pos()[0] < 130 and 450 < pygame.mouse.get_pos()[1] < 530:
                    screen.fill((53,53,53))
                    game.point = 0
                    game.moves = 10
                    pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                    tilstand = 1
            #Hvis mus er på Highscore
            if 150 < pygame.mouse.get_pos()[0] < 230 and 450 < pygame.mouse.get_pos()[1] < 530:
                    screen.fill((53,53,53))
                    pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                    tilstand = 3


        #Hvis man trykker på highscore gå tilbage til start Menu
        if tilstand == 3 and event.type == pygame.MOUSEBUTTONDOWN:
            if 300 < pygame.mouse.get_pos()[0] < 400 and 25 < pygame.mouse.get_pos()[1] < 75:
                screen.fill((53,53,53))
                pygame.mixer.Sound.play(pygame.mixer.Sound("vgmenuhighlight.wav"))
                tilstand = 2



    menu(tilstand)
    output_logic(tilstand)
    highscore(tilstand)

    #pygame kommandoer til at vise grafikken og opdatere 60 gange i sekundet.
    pygame.display.flip()
    clock.tick(60)
