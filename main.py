import pygame
from fighter import Fighter

pygame.init()

#game window
SCREEN_WIDTH = 1000
SCREEN_HEIGHT = 600

screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("FightGame")

#framerate
clock = pygame.time.Clock()
FPS = 60

#define colours
YELLOW = (255, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

intro_count = 3
last_count_update = pygame.time.get_ticks()
score = [0, 0]
round_over = False
ROUND_OVER_COOLDOWN = 3000

#def player vars

WARRIOR_SIZE =  200
WARRIOR_SCALE = 4
WARRIOR_OFFSET = [90, 78]
WARRIOR_DATA = [WARRIOR_SIZE,WARRIOR_SCALE, WARRIOR_OFFSET]
HERO_SIZE = 200
HERO_SCALE = 4
HERO_OFFSET = [90, 78]
HERO_DATA = [HERO_SIZE,HERO_SCALE,HERO_OFFSET]
#background image
bg_img = pygame.image.load("assets/bkgimg.jpg").convert_alpha()

#LOAD SPRITE SHEETS
warrior_sheet = pygame.image.load("char_assets/Martial Hero 2/Sprites/warnou.png").convert_alpha()
hero_sheet = pygame.image.load("char_assets/Martial Hero/Sprites/heronou.png").convert_alpha()

victory_img = pygame.image.load("assets/Victory_banner-3928363755.png").convert_alpha()

#def nr of steps in animations
WARRIOR_ANI_STEPS = [4, 8, 2, 4, 4, 3, 7]
HERO_ANI_STEPS = [8, 8, 2, 6, 6, 4, 6]

#new font
count_font = pygame.font.Font("assets/Turok.ttf", 80)
score_font = pygame.font.Font("assets/Turok.ttf", 30)

#text
def draw_text(text, font,text_col,  x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x,y))

def draw_bkg():
    scaled_bg = pygame.transform.scale(bg_img, (SCREEN_WIDTH, SCREEN_HEIGHT))
    screen.blit(scaled_bg, (0, 0))

#draw healthbar
def draw_healthbar(health, x, y):
    ratio = health / 100
    pygame.draw.rect(screen, WHITE, (x - 2, y - 2, 404, 34))
    pygame.draw.rect(screen, RED, (x, y, 400 , 30))
    pygame.draw.rect(screen, YELLOW, (x, y, 400 * ratio, 30))

# add the 2 fighters

player1 = Fighter(1, 200, 310, WARRIOR_DATA, warrior_sheet, WARRIOR_ANI_STEPS)
player2 = Fighter(2, 700, 310,HERO_DATA, hero_sheet, HERO_ANI_STEPS)

#game loop

run = True
while run:

    clock.tick(FPS)

    draw_bkg()

    #PLAYER STATSd
    draw_healthbar(player1.health, 20, 20)
    draw_healthbar(player2.health, 580, 20)

    draw_text("P1:" + str(score[0]), score_font, WHITE, 20, 60)
    draw_text("P2:" + str(score[1]), score_font, WHITE, 580, 60)

    if intro_count <= 0:
        #movement
        player1.move(SCREEN_WIDTH,SCREEN_HEIGHT, player2, round_over)
        player2.move(SCREEN_WIDTH, SCREEN_HEIGHT, player1, round_over)
    else:
        draw_text(str(intro_count), count_font, WHITE , SCREEN_WIDTH / 2, SCREEN_HEIGHT / 3)
        if (pygame.time.get_ticks() - last_count_update) >= 1000:
            intro_count -= 1
            last_count_update = pygame.time.get_ticks()


    player1.update()
    player2.update()

   #W player2.move()

    player1.draw(screen)
    player2.draw(screen)

    #DEFEAT?
    if round_over == False:
        if player1.alive == False:
            score[1] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
        elif player2.alive == False:
            score[0] += 1
            round_over = True
            round_over_time = pygame.time.get_ticks()
    else:
        screen.blit(victory_img, (95, 150))
        if pygame.time.get_ticks() - round_over_time > ROUND_OVER_COOLDOWN:
            round_over = False
            intro_count = 3
            player1 = Fighter(1, 200, 310, WARRIOR_DATA, warrior_sheet, WARRIOR_ANI_STEPS)
            player2 = Fighter(2, 700, 310, HERO_DATA, hero_sheet, HERO_ANI_STEPS)

    for event in pygame.event.get():
         if event.type == pygame.QUIT:
             run = False
    pygame.display.update()

#exit game
pygame.quit()