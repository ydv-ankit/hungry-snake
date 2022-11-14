from sre_parse import SPECIAL_CHARS
import random
import pygame
pygame.mixer.init()
pygame.mixer.music.set_volume(1)

pygame.init()

# colors
white = (255,255,255)
red = (255,0,0)
black = (0,0,0)
blue = (0,0,255)

global highscore
highscore = 0

# window specs
screen_height = 600
screen_width = 1000

# creating window
gameWindow = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption("SNAKE")
pygame.display.update()

clock = pygame.time.Clock()
font = pygame.font.SysFont(None,55)
gameOverfont = pygame.font.SysFont(None,35)

# backgrounds and music
def soundPlay(file,again = 0):
    pygame.mixer.music.load(file)
    pygame.mixer.music.play(again)

def soundStop():
    pygame.mixer.music.stop()


# display score
def screenText(text,color,x,y):
    screen_text = font.render(text,True,color)
    gameWindow.blit(screen_text,(x,y))

def plotSnake(gameWindow,color,snk_list,snake_size):
    for x,y in snk_list:
        pygame.draw.rect(gameWindow,color,[x,y,snake_size,snake_size])

def welcome():
    exit_game=  False
    soundPlay("bg.mp3",-1)
    while not exit_game:
        gameWindow.fill(white)
        screenText("WELCOME To Snake Game",black,200,200)
        screenText("Press ENTER to play",black,250,300)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit_game = True    
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    exit_game = True
        pygame.display.update()
        # clock.tick()

# game loop
def gameloop(highscore):
    soundStop()
    # game specific variables        
    snk_list = list()
    snk_len = 1
    exit_game = False
    game_over = False
    score = 0
    snake_x = 255
    snake_y = 255
    snake_size = 8
    snake_dir = ''
    vel_x = 0
    vel_y = 0
    init_vel = 8
    big_food = False
    food_x = random.randint(50,screen_width/2)
    food_y = random.randint(50,screen_height/2)
    fps = 10 # frames per second
    # call gameWindow in loop
    while not exit_game:
        if game_over:
            gameWindow.fill(white)
            if score>highscore and score > 0:
                screenText("NEW HIGHSCORE : "+str(score),blue,350,200) 
            else:
                screenText("HIGHSCORE : "+str(highscore),blue,350,200)
            screenText("Saamp mar gaya !! Jinda karna hai ?",red,200,300)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RETURN:
                        gameloop(score)

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    exit_game = True

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_RIGHT and snake_dir != 'x':
                        vel_x = init_vel
                        vel_y = 0
                        snake_dir = 'x'
                    if event.key == pygame.K_LEFT and snake_dir != 'x':
                        vel_x = -init_vel
                        vel_y = 0
                        snake_dir = 'x'
                    if event.key == pygame.K_UP and snake_dir != 'y':
                        vel_x = 0
                        vel_y = -init_vel
                        snake_dir = 'y'
                    if event.key == pygame.K_DOWN and snake_dir != 'y':
                        vel_x = 0
                        vel_y = init_vel
                        snake_dir = 'y'
                    # cheat codes
                    if event.key == pygame.K_e: #increase score
                        score+=20
                    if event.key == pygame.K_c: # decrease snake speed
                        init_vel = 3
            
            if big_food:
                if abs(snake_x - food_x)<20 and abs(snake_y - food_y)<20:
                # pygame.mixer.music.pause()
                    soundPlay("bigbite.mp3")
                    # pygame.mixer.music.unpause()
                    score +=15
                    food_x = random.randint(50,screen_width/2)
                    food_y = random.randint(50,screen_height/2)
                    snk_len += 2
                    big_food = False
            else:
                if abs(snake_x - food_x)<8 and abs(snake_y - food_y)<8:
                # pygame.mixer.music.pause()
                    soundPlay("smallbite.mp3")
                    # pygame.mixer.music.unpause()
                    score +=7
                    food_x = random.randint(50,screen_width/2)
                    food_y = random.randint(50,screen_height/2)
                    snk_len += 1

            snake_x+=vel_x
            snake_y+=vel_y

            gameWindow.fill(white)
            if (score%4==0 and score > 0):
                pygame.draw.rect(gameWindow,red,[food_x,food_y,20,20])
                big_food = True
            else:
                pygame.draw.rect(gameWindow,red,[food_x,food_y,snake_size,snake_size])
            screenText("SCORE : "+str(score),red,5,5)
            screenText("HIGHSCORE : "+str(highscore),red,300,5) 

            head = []
            head.append(snake_x)
            head.append(snake_y)
            snk_list.append(head)
            if len(snk_list) > snk_len:
                del snk_list[0]

            if snake_x<0 or snake_x>screen_width or snake_y<50 or snake_y>screen_height:
                game_over = True
            if head in snk_list[:-1]:
                game_over = True
            plotSnake(gameWindow,blue,snk_list,snake_size)
            pygame.draw.line(gameWindow,black,(0,48),(screen_width,48))
        pygame.display.update()
        clock.tick(fps)

    # at last
    pygame.quit()
    quit()

# start game
welcome()
gameloop(highscore)