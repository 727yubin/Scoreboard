#!/usr/bin/python3

# Copyright 2019 Yubin Lee <727yubin@gmail.com>
# Licensed under GPL v3

# A scoreboard for basketball games

from ast import literal_eval  # For getting tuples from config
import datetime
import os
import pygame
from pygame.locals import *
import sys
import time

try:
    config = open('config.txt', 'r')
except FileNotFoundError:
    print('Configuration file not found.')
    input('Please download https://github.com/727yubin/Scoreboard/blob/master/config.txt')
    sys.exit()

# Get values from config file
BGCOLOR = literal_eval(config.readline().rstrip('\n'))
TEXTCOLOR = literal_eval(config.readline().rstrip('\n'))
TIMEFONTSIZE = int(config.readline().rstrip('\n'))
TEAMFONTSIZE = int(config.readline().rstrip('\n'))
SCOREFONTSIZE = int(config.readline().rstrip('\n'))
FOULNUMBERFONTSIZE = int(config.readline().rstrip('\n'))
BASEFONTTYPE = config.readline().rstrip('\n')
SCHOOLFONTTYPE = config.readline().rstrip('\n')

try:
    logo = pygame.image.load('logo.png')
    logo = pygame.transform.scale(logo, (80, 80))
except:
    print('School logo not found.')
    input('Please place your logo as logo.png in the same directory')
    sys.exit()

pygame.init()
print('')

WIDTH = 1280
HEIGHT = 720
reloaded = False
state_a = state_b = False

try: # Fonts
    TIMEFONT = pygame.font.Font(BASEFONTTYPE, TIMEFONTSIZE)
    TEAMFONT = pygame.font.Font(BASEFONTTYPE, TEAMFONTSIZE)
    SCOREFONT = pygame.font.Font(BASEFONTTYPE, SCOREFONTSIZE)
    FOULNUMBERFONT = pygame.font.Font(BASEFONTTYPE, FOULNUMBERFONTSIZE)
    FOULFONT = pygame.font.Font(BASEFONTTYPE, 50)
    CREDITS1FONT = pygame.font.Font(BASEFONTTYPE, 20)
    CREDITS2FONT = pygame.font.Font(BASEFONTTYPE, 30)
except:
    input("No base font found; please refer to https://github.com/727yubin/Scoreboard")
try:
    SCHOOLFONT = pygame.font.Font(SCHOOLFONTTYPE, 80)
except:
    input("No school font found; please refer to https://github.com/727yubin/Scoreboard")

try:
    if os.stat("backup.txt").st_size == 0:
        os.remove("backup.txt")
except:
    pass

# Check if blackout has occurred(quite frequent in Lebanon)
if os.path.isfile('backup.txt') and os.stat('backup.txt').st_size != 0:
    print('Reloading details from previous game... ')
    reloaded = True
    backup = open('backup.txt', 'r')

    time_a = float(backup.readline().rstrip('\n'))
    time_b = float(backup.readline().rstrip('\n'))
    TEAM1NAME = backup.readline().rstrip('\n').upper()
    TEAM2NAME = backup.readline().rstrip('\n').upper()
    TEAM1SCORE = int(backup.readline().rstrip('\n'))
    TEAM2SCORE = int(backup.readline().rstrip('\n'))
    CURRENTPERIOD = int(backup.readline().rstrip('\n'))
    TEAM1FOULS = int(backup.readline().rstrip('\n'))
    TEAM2FOULS = int(backup.readline().rstrip('\n'))
    POSSESION = bool(backup.readline().rstrip('\n'))

else:
    TEAM1NAME = input('Please enter team 1 name: ').upper()
    TEAM2NAME = input('Please enter team 2 name: ').upper()
    TEAM1SCORE = 0
    TEAM2SCORE = 0
    CURRENTPERIOD = 1
    TEAM1FOULS = 0
    TEAM2FOULS = 0
    POSSESION = False

pygame.display.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT), pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
rect = background.fill(BGCOLOR)
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

backup = open('backup.txt', 'w')


def reset_a():
    global state_a, time_a, start_time_a, timer_txt_a
    state_a = False
    time_a = 0
    start_time_a = 0
    timer_txt_a = 0

def reset_b():
    global state_b, time_b, start_time_b, timer_txt_b
    state_b = False
    time_b = 0
    start_time_b = 0
    timer_txt_b = 0

def WriteToBackup():
    backup = open('backup.txt', 'w')
    backup.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(
        str(timer_txt_a), str(timer_txt_b), TEAM1NAME, TEAM2NAME, str(TEAM1SCORE),
        str(TEAM2SCORE), str(CURRENTPERIOD), str(TEAM1FOULS),
        str(TEAM2FOULS), str(POSSESION)))
    backup.flush()
    os.fsync(backup.fileno())
    backup.close()

if not reloaded:
    reset_a()
    reset_b()

while True:  # Main loop
    for event in pygame.event.get():

        if event.type == USEREVENT:  # Countdown timer
            WriteToBackup()

        if event.type == KEYDOWN:

            if event.key == K_SPACE:  # Pause/Play
                if state_a:
                    time_a = timer_txt_a
                    pygame.time.set_timer(USEREVENT, 0)

                if not state_a:
                    start_time_a = time.time()
                    pygame.time.set_timer(USEREVENT, 100)
                state_a = not state_a

            if event.key == K_0 or event.key == K_KP0:  # Pause/Play
                if state_b:
                    time_b = timer_txt_b

                if not state_b:
                    start_time_b = time.time()
                state_b = not state_b


            if event.key == K_a:
                time_a += 60
            if event.key == K_s:
                time_a += 1
            if event.key == K_d:
                time_a += 0.1

            if event.key == K_z and timer_txt_a >= 60:
                time_a -= 60
            if event.key == K_x and timer_txt_a >= 1:
                time_a -= 1
            if event.key == K_c and timer_txt_a >= 0.1:
                time_a -= 0.1

            if event.key == K_1 or event.key == K_KP1:
                time_b = timer_txt_b = 24
                start_time_b = time.time()
                state_b = True

            if event.key == K_2 or event.key == K_KP2:
                time_b = timer_txt_b = 14
                start_time_b = time.time()
                state_b = True

            if event.key == K_f:
                CURRENTPERIOD += 1
            if event.key == K_v:
                CURRENTPERIOD -= 1
            
            if CURRENTPERIOD < 1:
                CURRENTPERIOD = 1

            if event.key == K_h:
                TEAM1SCORE += 1
            if event.key == K_j:
                TEAM1SCORE += 2
            if event.key == K_k:
                TEAM1SCORE += 3
            if event.key == K_l:
                TEAM1SCORE -= 1

            if TEAM1SCORE < 0:
                TEAM1SCORE = 0

            if event.key == K_SEMICOLON:
                TEAM1FOULS += 1
            if event.key == K_QUOTE:
                TEAM1FOULS -= 1

            if TEAM1FOULS < 0:
                TEAM1FOULS = 0

            if event.key == K_b:
                TEAM2SCORE += 1
            if event.key == K_n:
                TEAM2SCORE += 2
            if event.key == K_m:
                TEAM2SCORE += 3
            if event.key == K_COMMA:
                TEAM2SCORE -= 1

            if TEAM2SCORE < 0:
                TEAM2SCORE = 0

            if event.key == K_PERIOD:
                TEAM2FOULS += 1
            if event.key == K_SLASH:
                TEAM2FOULS -= 1

            if TEAM2FOULS < 0:
                TEAM2FOULS = 0

            if event.key == K_g:
                POSSESION = not POSSESION

            if event.key == K_ESCAPE:
                backup.close()
                print("Purging backup...")
                os.remove('backup.txt')
                sys.exit()

            if not state_a:
                WriteToBackup()

        time_a = round(time_a, 1)
        time_b = round(time_b, 1)

    if state_a and timer_txt_a > 0:
        timer_txt_a = time_a - time.time() + start_time_a
    elif not state_a:
        timer_txt_a = time_a

    if timer_txt_a <= 0:
        reset_a()
        pygame.time.set_timer(USEREVENT, 0)

    if state_b and timer_txt_b > 0:
        timer_txt_b = time_b - time.time() + start_time_b
    elif not state_b:
        timer_txt_b = time_b

    if timer_txt_b <= 0:
        reset_b()

        # Switch between mm:ss and ss.c
    if timer_txt_a > 60:
        time_a_str = '%d:%02d' % (int(timer_txt_a / 60), int(timer_txt_a % 60))
    else:
        time_a_str = '%.1f' % timer_txt_a

    if timer_txt_b < 10:
        time_b_str = '%.1f' % timer_txt_b
    else:
        time_b_str = str(int(timer_txt_b))
    if len(time_b_str) > 3:
        time_b_str = "10"

    # Start rendering
    time_a_txt = TIMEFONT.render(time_a_str, 1, TEXTCOLOR)
    time_a_rect = time_a_txt.get_rect()
    time_a_rect.center = (640, 220)

    time_b_txt = FOULNUMBERFONT.render(time_b_str, 1, TEXTCOLOR)
    time_b_rect = time_b_txt.get_rect()
    time_b_rect.center = (640, 560)

    currenttime_txt = SCHOOLFONT.render(datetime.datetime.now().strftime("%H:%M"), 1, TEXTCOLOR)
    currenttimerect = currenttime_txt.get_rect()
    currenttimerect.center = (100, 50)

    team1name_txt = TEAMFONT.render(TEAM1NAME, 1, TEXTCOLOR)
    team1namerect = team1name_txt.get_rect()
    team1namerect.center = (250, 500)

    team2name_txt = TEAMFONT.render(TEAM2NAME, 1, TEXTCOLOR)
    team2namerect = team2name_txt.get_rect()
    team2namerect.center = (1030, 500)

    team1score_txt = SCOREFONT.render(str(TEAM1SCORE), 1, TEXTCOLOR)
    team1scorerect = team1score_txt.get_rect()
    team1scorerect.center = (210, 350)

    team2score_txt = SCOREFONT.render(str(TEAM2SCORE), 1, TEXTCOLOR)
    team2scorerect = team2score_txt.get_rect()
    team2scorerect.center = (1070, 350)

    period_txt = TEAMFONT.render('PERIOD %i' % CURRENTPERIOD, 1, TEXTCOLOR)
    periodrect = period_txt.get_rect()
    periodrect.center = (640, 390)

    foul_txt = FOULFONT.render('FOULS', 1, TEXTCOLOR)
    foultextrect1 = foul_txt.get_rect()
    foultextrect1.center = (130, 620)
    foultextrect2 = foul_txt.get_rect()
    foultextrect2.center = (950, 620)

    team1fouls_txt = FOULNUMBERFONT.render(str(TEAM1FOULS), 1, TEXTCOLOR)
    team1foulsrect = team1fouls_txt.get_rect()
    team1foulsrect.center = (330, 620)

    team2fouls_txt = FOULNUMBERFONT.render(str(TEAM2FOULS), 1, TEXTCOLOR)
    team2foulsrect = team2fouls_txt.get_rect()
    team2foulsrect.center = (1150, 620)

    if POSSESION:
        possesion_txt = TEAMFONT.render('>', 1, TEXTCOLOR)
        possesionrect = possesion_txt.get_rect()
        possesionrect.center = (920, 390)

    elif not POSSESION:
        possesion_txt = TEAMFONT.render('<', 1, TEXTCOLOR)
        possesionrect = possesion_txt.get_rect()
        possesionrect.center = (350, 390)

    school_txt = SCHOOLFONT.render('LES Loueizeh', 1, TEXTCOLOR)
    schoolrect = school_txt.get_rect()
    schoolrect.center = (690, 50)

    credits1_txt = CREDITS1FONT.render("Programmed by:", 1, TEXTCOLOR)
    credits1rect = credits1_txt.get_rect()
    credits1rect.center = (1200, 45)

    credits2_txt = CREDITS2FONT.render("Yubin Lee '19", 1, TEXTCOLOR)
    credits2rect = credits1_txt.get_rect()
    credits2rect.center = (1170, 65)

    # Blit everything
    screen.blit(background, rect)
    screen.blit(logo, (350, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 90, 1280, 630), 10)
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 200, 90), 10)
    pygame.draw.rect(screen, (255, 255, 255), (330, 110, 620, 230), 5)
    pygame.draw.rect(screen, (255, 255, 255), (520, 470, 240, 180), 5)
    screen.blit(school_txt, schoolrect)
    screen.blit(currenttime_txt, currenttimerect)
    screen.blit(credits1_txt, credits1rect)
    screen.blit(credits2_txt, credits2rect)

    for num in range(TEAM1FOULS):
        if num > 4: # 5 fouls, but num starts from 0
            num = 4
        pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (395, 680 - 30 * num, 50, 20))
    
    for num in range(TEAM2FOULS):
        if num > 4:
            num = 4
        pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (1215, 680 - 30 * num, 50, 20))

    screen.blit(time_a_txt, time_a_rect)
    screen.blit(time_b_txt, time_b_rect)
    screen.blit(team1name_txt, team1namerect)
    screen.blit(team2name_txt, team2namerect)
    screen.blit(team1score_txt, team1scorerect)
    screen.blit(team2score_txt, team2scorerect)
    screen.blit(period_txt, periodrect)
    screen.blit(foul_txt, foultextrect1)
    screen.blit(foul_txt, foultextrect2)
    screen.blit(team1fouls_txt, team1foulsrect)
    screen.blit(team2fouls_txt, team2foulsrect)
    screen.blit(possesion_txt, possesionrect)

    pygame.display.flip()