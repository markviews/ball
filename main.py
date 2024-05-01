import pygame
from pygame.locals import *

PLAYER_SIZE = 30
BALL_SIZE = 30
BALL_SPEED = 5

pygame.init()

clock = pygame.time.Clock()
screen = pygame.display.set_mode((800,600))

goal1 = pygame.Rect(0,screen.get_height()/2 - 50,10,100)
goal2 = pygame.Rect(screen.get_width()-10,screen.get_height()/2 - 50,10,100)
player1 = pygame.Rect(200,300,PLAYER_SIZE,PLAYER_SIZE)
player2 = pygame.Rect(600,300,PLAYER_SIZE,PLAYER_SIZE)
ball = pygame.Rect(screen.get_width()/2,screen.get_height()/2,BALL_SIZE,BALL_SIZE)
ballVelocity = [BALL_SPEED,BALL_SPEED]
score1 = 0
score2 = 0

def score(dir):
    ballVelocity[0] = BALL_SPEED * dir
    ballVelocity[1] = BALL_SPEED * dir
    ball.x = screen.get_width()/2
    ball.y = screen.get_height()/2

def text(msg, x, y):
    txt = pygame.font.SysFont("comicsansms", 65).render(str(msg) , True, (255,255,255))
    textRect = txt.get_rect()
    textRect.center = (screen.get_width()/2+x) , ((screen.get_height()/2) + y)
    screen.blit(txt,textRect)

while True:
        
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
    
    # apply velocity
    ball.x += ballVelocity[0]
    ball.y += ballVelocity[1]

    # collision with players
    if ball.colliderect(player1) or ball.colliderect(player2):
        ballVelocity[0] = -ballVelocity[0]
        ballVelocity[1] = -ballVelocity[1]

    # collision with walls
    if ball.y < 0 or ball.y > screen.get_height() - BALL_SIZE:
        ballVelocity[1] *= -1
    if ball.x < 0 or ball.x > screen.get_width() - BALL_SIZE:
        ballVelocity[0] *= -1

    # collision with goals
    if ball.colliderect(goal1):
        score2 += 1
        score(1)
    elif ball.colliderect(goal2):
        score1 += 1
        score(-1)

    # draw stuff
    screen.fill((0,0,0))
    text(score1, -150, -200)
    text(score2, 150, -200)
    pygame.draw.rect(screen, (255,100, 100), player1)
    pygame.draw.rect(screen, (255,100, 100), player2)  
    pygame.draw.rect(screen,(147,251,253),goal1)
    pygame.draw.rect(screen,(147,251,253),goal2)
    pygame.draw.rect(screen,(255,255,255),ball)
    
    pygame.display.update()
    clock.tick(50)
