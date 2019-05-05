from wumpusWorld import *
import pygame
from pygame.locals import *
from constant import *

pygame.init()
screen = pygame.display.set_mode((width,height))
running = True
grid = []
gold_img = None


pygame.display.set_caption("Wumpus World")
clock = pygame.time.Clock()

gold_img_file = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\G.png')
pit_img_file = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\hole.png')

player_R_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\PR.png')
player_L_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\PL.png')
player_U_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\PU.png')
player_D_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\PD.png')

wumpus_L_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\W.png')
wumpus_D_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\WD.png')

breez_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\B.png')
stench_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\S.png')
bs_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\BS.png')
legend_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\legend.png')
legend2_img = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\legend2.png')

gameover = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\gameover.png')
youwin = pygame.image.load(r'C:\Users\acer\Documents\WumpusWorldPygame\Img\youwin.png')
player_img = player_R_img
playerpos = []
coord = []
coord_wumpus = []
font2 = pygame.font.SysFont("comicsanms", 30)

player = Explorer(program)
env = WumpusEnvironment(player, size, size)


def draw_world(player_img):
    screen.blit(legend_img,[470,MARGIN])
    screen.blit(legend2_img, [470, 120])
    font = pygame.font.SysFont("arial", 15)
    percept_text = font.render("Percept : "+str(env.percepts_from(player,player.location)),True
                       ,WHITE)
    performance_text = font.render("Performance : " + str(player.performance), True
                               , WHITE)
    win_text = font.render("Win Status : " + str(player.win), True
                               , WHITE)
    screen.blit(percept_text,[470,220])
    screen.blit(performance_text, [470, 240])
    screen.blit(win_text, [470, 260])


    for row in range(size):
        for column in range(size):
            breeze, stench, wumpus, pit, gold, thereis_percept = False, False, False, False, False, False
            loc = (row,column)
            cell = world[row][column]
            coord_wumpus = [column * (HEIGHT + MARGIN) + (HEIGHT / 2) - (30),
                            row * (WIDTH + MARGIN) + (WIDTH / 2) - (25)]
            coord = [(column * HEIGHT) + (column + 1) * MARGIN, (row * WIDTH) + (row + 1) * MARGIN]

            if (loc == player.location):
                color = WHITE
                playerpos = [column*(HEIGHT+MARGIN)+(HEIGHT/2)-(30),row*(WIDTH+MARGIN)+(WIDTH/2)-(25)]
            elif (loc in env.visited):
                color = WHITE
            elif (loc == env.wumpus.location and not env.wumpus.alive):
                color = WHITE
            else:color = GREY

            pygame.draw.rect(screen, color, [(MARGIN+WIDTH)*column+MARGIN, (MARGIN+WIDTH)*row+MARGIN, WIDTH, HEIGHT ])
            if (loc == player.location):
                if(not env.in_danger(player)):
                    screen.blit(player_img, playerpos)

            if (loc == env.wumpus.location and not env.wumpus.alive and loc != player.location):
                screen.blit(wumpus_D_img,coord_wumpus)

            if (loc in env.visited):
                for element in cell:
                    if (isinstance(element, Wumpus)):
                        wumpus = True
                    elif (isinstance(element, Gold)):
                        gold = True
                    elif (isinstance(element, Breeze)):
                        breeze = True
                    elif (isinstance(element, Stench)):
                        stench = True
                    elif (isinstance(element, Pit)):
                        pit = True
                        pass
                if (breeze or stench): thereis_percept = True
                if (breeze and stench):
                    screen.blit(bs_img,coord)
                if (breeze):
                    screen.blit(breez_img,coord)
                if (stench):
                    screen.blit(stench_img,coord)
                if (wumpus and env.wumpus.alive):
                    screen.blit(wumpus_L_img, coord_wumpus)
                if (pit):
                    screen.blit(pit_img_file, coord)
                if (gold):
                    screen.blit(gold_img_file,coord)

    if(player.win):
        screen.blit(youwin,[0,0])
        # Tampilkan score
        text = font2.render("Score: {}".format(str(player.performance)), True, (255, 255, 255))
        screen.blit(text, [200,250])

    if (env.in_danger(player)):
        screen.blit(gameover, [0, 0])
        # Tampilkan score
        text = font2.render("Score: {}".format(str(player.performance)), True, (255, 255, 255))
        screen.blit(text, [200, 250])














while(running):

    # 5 - Clear the screen ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~
    screen.fill(DARK_GREY)
    world = env.get_world()
    draw_world(player_img)
    print(player.performance)
    print(player.alive)
    print(player.location[0])

    pygame.display.flip()

    # 8 - Event Loop ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_LEFT:
                env.execute_action(player,"TurnLeft")
                player_img = player_L_img
            if event.key == pygame.K_RIGHT:
                env.execute_action(player,"TurnRight")
                player_img = player_R_img
            if event.key == pygame.K_UP:
                env.execute_action(player,"Up")
                player_img = player_U_img
            if event.key == pygame.K_DOWN:
                env.execute_action(player,"Down")
                player_img = player_D_img
            if event.key == pygame.K_SPACE:
                env.execute_action(player, "Forward")
            if (event.key == pygame.K_RCTRL):
                env.execute_action(player,'Shoot')
            if (event.key == pygame.K_LCTRL):
                env.execute_action(player, 'Shoot')
            if (event.key == pygame.K_LSHIFT):
                env.execute_action(player,'Grab')
            if (event.key == pygame.K_RSHIFT):
                env.execute_action(player, 'Grab')

        # event saat tombol exit diklik
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
        # 10 - Win/Lose check ~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~





while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            exit(0)
pygame.display.flip()