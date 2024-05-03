import pygame
from pygame.locals import *
import cv2
import numpy as np
from screeninfo import get_monitors

PLAYER_SIZE = 30
BALL_SIZE = 30
BALL_SPEED = 5
CAMERA_INDEX = 0

SCREEN_WIDTH = 1920
SCREEN_HEIGHT = 1080

def getPuckPos(x, y, w, h, frame):
    width = frame.shape[1]
    #height = frame.shape[0]

    distLeftWall = x
    distRightWall = width - (x + w)

    if distLeftWall < 20:
        pos = [x + w, y + h/2]
        pos = [int(pos[0] * SCREEN_WIDTH / frame.shape[1]), int(pos[1] * SCREEN_HEIGHT / frame.shape[0])]
        return 'left', pos[0], pos[1]
    
    if distRightWall < 20:
        pos = [x, y + h/2]
        pos = [int(pos[0] * SCREEN_WIDTH / frame.shape[1]), int(pos[1] * SCREEN_HEIGHT / frame.shape[0])]
        return 'right', pos[0], pos[1]
    
    return None

for m in get_monitors():
    SCREEN_WIDTH = m.width
    SCREEN_HEIGHT = m.height

backSub = cv2.createBackgroundSubtractorMOG2()
cap = cv2.VideoCapture(CAMERA_INDEX)
pygame.init()
clock = pygame.time.Clock()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

goal1 = pygame.Rect(0,screen.get_height()/2 - 50,10,100)
goal2 = pygame.Rect(screen.get_width()-10,screen.get_height()/2 - 50,10,100)
player1 = pygame.Rect(screen.get_width() * (1/4), 300, PLAYER_SIZE, PLAYER_SIZE)
player2 = pygame.Rect(screen.get_width() * (3/4), 300, PLAYER_SIZE, PLAYER_SIZE)
ball = pygame.Rect(screen.get_width()/2, screen.get_height()/2, BALL_SIZE, BALL_SIZE)
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
            cap.release()
            cv2.destroyAllWindows()
            pygame.quit()
            quit()

    ret, frame = cap.read()
    fgMask = backSub.apply(frame)

    contours, _ = cv2.findContours(fgMask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    for contour in contours:
        x, y, w, h = cv2.boundingRect(contour)

        # ignore small boxes
        if w < 20 or h < 20:
            continue

        pos = getPuckPos(x, y, w, h, frame)
        color = np.mean(frame[y:y+h, x:x+w], axis=(0, 1))
        dist_white = np.linalg.norm(color - [255, 255, 255])

        if dist_white < 120:
            pos = None

        print(dist_white)

        if pos is not None:
            side, x, y = pos

            if side == 'left':
                player1.x = x
                player1.y = y
            elif side == 'right':
                player2.x = x
                player2.y = y

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
    pygame.draw.rect(screen, (147,251,253), goal1)
    pygame.draw.rect(screen, (147,251,253), goal2)
    pygame.draw.rect(screen, (255,255,255), player1)
    pygame.draw.rect(screen, (255,255,255), player2)  
    pygame.draw.rect(screen, (255,255,255), ball)
    
    pygame.display.update()
    clock.tick(50)
