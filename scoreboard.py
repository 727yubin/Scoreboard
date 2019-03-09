#!/usr/bin/python3

# Copyright 2019 Yubin Lee <727yubin@gmail.com>
# Licensed under GPL v3

# A scoreboard for basketball games

import pygame
from pygame.locals import *
import os
from sys import exit
from ast import literal_eval
from time import time
from datetime import datetime

pygame.init()
print("")

state_a = state_b = False
time_a = timer_txt_a = 600
time_b = timer_txt_b = 24
a_len = 5
b_len = 2
score1_len = score2_len = 1


class team:
    pass


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
        str(timer_txt_a), str(timer_txt_b), team1.name, team2.name,
        str(team1.score), str(team2.score), str(CURRENTPERIOD),
        str(team1.fouls), str(team2.fouls), str(POSSESION)))
    backup.flush()
    os.fsync(backup.fileno())
    backup.close()


team1 = team()
team2 = team()

try:
    config = open('config.txt', 'r')
except FileNotFoundError:
    print('Configuration file not found.')
    input("Please refer to https://github.com/727yubin/Scoreboard")
    exit()

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
except pygame.error:
    print('School logo not found.')
    input('Please place your logo as logo.png in the same directory')
    exit()

try:  # Fonts
    TIMEFONT = pygame.font.Font(BASEFONTTYPE, TIMEFONTSIZE)
    TEAMFONT = pygame.font.Font(BASEFONTTYPE, TEAMFONTSIZE)
    SCOREFONT = pygame.font.Font(BASEFONTTYPE, SCOREFONTSIZE)
    FOULNUMBERFONT = pygame.font.Font(BASEFONTTYPE, FOULNUMBERFONTSIZE)
    FOULFONT = pygame.font.Font(BASEFONTTYPE, 50)
    CREDITS1FONT = pygame.font.Font(BASEFONTTYPE, 20)
    CREDITS2FONT = pygame.font.Font(BASEFONTTYPE, 30)
except OSError:
    print("No base font found.")
    input("Please refer to https://github.com/727yubin/Scoreboard")

try:
    SCHOOLFONT = pygame.font.Font(SCHOOLFONTTYPE, 80)
except OSError:
    print("No school font found.")
    input("Please refer to https://github.com/727yubin/Scoreboard")

if os.path.isfile('backup.txt') and os.stat("backup.txt").st_size == 0:
    os.remove("backup.txt")

if os.path.isfile('backup.txt'):
    print('Reloading details from previous game... ')
    reloaded = True
    backup = open('backup.txt', 'r')

    time_a = float(backup.readline().rstrip('\n'))
    time_b = float(backup.readline().rstrip('\n'))
    team1.name = backup.readline().rstrip('\n').upper()
    team2.name = backup.readline().rstrip('\n').upper()
    team1.score = int(backup.readline().rstrip('\n'))
    team2.score = int(backup.readline().rstrip('\n'))
    CURRENTPERIOD = int(backup.readline().rstrip('\n'))
    team1.fouls = int(backup.readline().rstrip('\n'))
    team2.fouls = int(backup.readline().rstrip('\n'))
    POSSESION = bool(backup.readline().rstrip('\n'))
else:
    team1.name = input('Please enter team 1 name: ').upper()
    team2.name = input('Please enter team 2 name: ').upper()
    team1.score = 0
    team2.score = 0
    CURRENTPERIOD = 1
    team1.fouls = 0
    team2.fouls = 0
    POSSESION = False

screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
rect = background.fill(BGCOLOR)
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

backup = open('backup.txt', 'w')

# Static Graphics
team1name_txt = TEAMFONT.render(team1.name, 1, TEXTCOLOR)
team1namerect = team1name_txt.get_rect()
team1namerect.center = (230, 500)

team2name_txt = TEAMFONT.render(team2.name, 1, TEXTCOLOR)
team2namerect = team2name_txt.get_rect()
team2namerect.center = (1050, 500)

team1score_txt = SCOREFONT.render(str(team1.score), 1, TEXTCOLOR)
team1scorerect = team1score_txt.get_rect()
team1scorerect.center = (210, 350)

team2score_txt = SCOREFONT.render(str(team2.score), 1, TEXTCOLOR)
team2scorerect = team2score_txt.get_rect()
team2scorerect.center = (1070, 350)

foul_txt = FOULFONT.render('FOULS', 1, TEXTCOLOR)
foultextrect1 = foul_txt.get_rect()
foultextrect1.center = (130, 620)
foultextrect2 = foul_txt.get_rect()
foultextrect2.center = (950, 620)

school_txt = SCHOOLFONT.render('LES Loueizeh', 1, TEXTCOLOR)
schoolrect = school_txt.get_rect()
schoolrect.center = (690, 50)

credits1_txt = CREDITS1FONT.render("Programmed by:", 1, TEXTCOLOR)
credits1rect = credits1_txt.get_rect()
credits1rect.center = (1200, 45)

credits2_txt = CREDITS2FONT.render("Yubin Lee '19", 1, TEXTCOLOR)
credits2rect = credits1_txt.get_rect()
credits2rect.center = (1170, 65)

screen.blit(background, rect)
screen.blit(logo, (350, 0))
pygame.draw.rect(screen, (255, 255, 255), (0, 90, 1280, 630), 10)
pygame.draw.rect(screen, (255, 255, 255), (0, 0, 200, 90), 10)
pygame.draw.rect(screen, (255, 255, 255), (347, 100, 586, 265), 5)
pygame.draw.rect(screen, (255, 255, 255), (530, 520, 220, 180), 5)
screen.blit(school_txt, schoolrect)
screen.blit(credits1_txt, credits1rect)
screen.blit(credits2_txt, credits2rect)
screen.blit(team1name_txt, team1namerect)
screen.blit(team2name_txt, team2namerect)
screen.blit(foul_txt, foultextrect1)
screen.blit(foul_txt, foultextrect2)

# Dynamic base graphics
if timer_txt_a > 60:
    time_a_str = '%d:%02d' % (int(timer_txt_a / 60), int(timer_txt_a % 60))
else:
    time_a_str = '%.1f' % timer_txt_a

time_a_txt = TIMEFONT.render(time_a_str, 1, TEXTCOLOR)
time_a_rect = time_a_txt.get_rect()
time_a_rect.center = (640, 233)
screen.blit(time_a_txt, time_a_rect)

if state_b and timer_txt_b > 0:
    timer_txt_b = time_b - time() + start_time_b
elif not state_b:
    timer_txt_b = time_b

if timer_txt_b <= 0:
    reset_b()

if timer_txt_b < 10:
    time_b_str = '%.1f' % timer_txt_b
else:
    time_b_str = str(int(timer_txt_b))
if len(time_b_str) > 3:
    time_b_str = "10"

time_b_txt = FOULNUMBERFONT.render(time_b_str, 1, TEXTCOLOR)
time_b_rect = time_b_txt.get_rect()
time_b_rect.center = (640, 610)
screen.blit(time_b_txt, time_b_rect)

team1score_txt = SCOREFONT.render(str(team1.score), 1, TEXTCOLOR)
team1scorerect = team1score_txt.get_rect()
team1scorerect.center = (210, 350)

team2score_txt = SCOREFONT.render(str(team2.score), 1, TEXTCOLOR)
team2scorerect = team2score_txt.get_rect()
team2scorerect.center = (1070, 350)

team1fouls_txt = FOULNUMBERFONT.render(str(team1.fouls), 1, TEXTCOLOR)
team1foulsrect = team1fouls_txt.get_rect()
team1foulsrect.center = (330, 620)

team2fouls_txt = FOULNUMBERFONT.render(str(team2.fouls), 1, TEXTCOLOR)
team2foulsrect = team2fouls_txt.get_rect()
team2foulsrect.center = (1150, 620)

if POSSESION:
    period_txt = TEAMFONT.render('<PERIOD %i  ' % CURRENTPERIOD, 1, TEXTCOLOR)
elif not POSSESION:
    period_txt = TEAMFONT.render('  PERIOD %i>' % CURRENTPERIOD, 1, TEXTCOLOR)
periodrect = period_txt.get_rect()
periodrect.center = (640, 450)

screen.blit(team1score_txt, team1scorerect)
screen.blit(team2score_txt, team2scorerect)
screen.blit(team1fouls_txt, team1foulsrect)
screen.blit(team2fouls_txt, team2foulsrect)
screen.blit(period_txt, periodrect)

for num in range(team1.fouls):
    if num > 4:
        num = 4
    pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (395, 680 - 30 * num, 50, 20))
    for blanks in range(5 - num):
        pygame.draw.rect(screen, BGCOLOR, (395, 680 - 30 * (5 - blanks), 50, 20))
if team1.fouls == 0:
    pygame.draw.rect(screen, BGCOLOR, (395, 680, 50, 20))

for num in range(team2.fouls):
    if num > 4:
        num = 4
    pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (1215, 680 - 30 * num, 50, 20))
    for blanks in range(5 - num):
        pygame.draw.rect(screen, BGCOLOR, (1215, 680 - 30 * (5 - blanks), 50, 20))
if team2.fouls == 0:
    pygame.draw.rect(screen, BGCOLOR, (1215, 680, 50, 20))

pygame.display.flip()

maintimecontrol = [K_a, K_s, K_d, K_z, K_x, K_c]
subtimecontrol = [K_0, K_KP0, K_1, K_KP1, K_2, K_KP2]
gamecontrol = [K_f, K_v, K_g]
team1scorecontrol = [K_h, K_j, K_k, K_l]
team2scorecontrol = [K_b, K_n, K_m, K_COMMA]
team1foulcontrol = [K_SEMICOLON, K_QUOTE]
team2foulcontrol = [K_PERIOD, K_SLASH]

foul1region = pygame.Rect(389, 553, 58, 151)
foul2region = pygame.Rect(1211, 553, 58, 151)

while True:  # Event loop
    if state_a and timer_txt_a > 0:
        timer_txt_a = time_a - time() + start_time_a
    elif not state_a:
        timer_txt_a = time_a

    if timer_txt_a <= 0:
        reset_a()
        pygame.time.set_timer(USEREVENT, 0)

    if timer_txt_a > 60:
        time_a_str = '%d:%02d' % (int(timer_txt_a / 60), int(timer_txt_a % 60))
    else:
        time_a_str = '%.1f' % timer_txt_a

    old_a_len = a_len
    a_len = len(time_a_str)

    if a_len < old_a_len:
        pygame.draw.rect(screen, BGCOLOR, (350, 103, 580, 258), 0)
        pygame.display.update()

    time_a_txt = TIMEFONT.render(time_a_str, 1, TEXTCOLOR)
    time_a_rect = time_a_txt.get_rect()
    time_a_rect.center = (640, 233)
    pygame.draw.rect(screen, BGCOLOR, time_a_rect, 0)
    screen.blit(time_a_txt, time_a_rect)

    if state_b and timer_txt_b > 0:
        timer_txt_b = time_b - time() + start_time_b
    elif not state_b:
        timer_txt_b = time_b

    if timer_txt_b <= 0:
        reset_b()

    if timer_txt_b < 10:
        time_b_str = '%.1f' % timer_txt_b
    else:
        time_b_str = str(int(timer_txt_b))
    if len(time_b_str) > 3:
        time_b_str = "10"

    old_b_len = b_len
    b_len = len(time_b_str)

    if b_len < old_b_len:
        pygame.draw.rect(screen, BGCOLOR, (533, 523, 214, 172), 0)
        pygame.display.update()

    time_b_txt = FOULNUMBERFONT.render(time_b_str, 1, TEXTCOLOR)
    time_b_rect = time_b_txt.get_rect()
    time_b_rect.center = (640, 610)
    pygame.draw.rect(screen, BGCOLOR, time_b_rect, 0)
    screen.blit(time_b_txt, time_b_rect)

    old_score1_len = score1_len
    score1_len = len(str(team1.score))

    if score1_len < old_score1_len:
        pygame.draw.rect(screen, BGCOLOR, (99, 238, 222, 225), 0)
        team1score_txt = SCOREFONT.render(str(team1.score), 1, TEXTCOLOR)
        team1scorerect = team1score_txt.get_rect()
        team1scorerect.center = (210, 350)
        screen.blit(team1score_txt, team1scorerect)
        pygame.display.update()

    old_score2_len = score2_len
    score2_len = len(str(team2.score))

    if score2_len < old_score2_len:
        pygame.draw.rect(screen, BGCOLOR, (959, 238, 222, 225), 0)
        team2score_txt = SCOREFONT.render(str(team2.score), 1, TEXTCOLOR)
        team2scorerect = team2score_txt.get_rect()
        team2scorerect.center = (1070, 350)
        screen.blit(team2score_txt, team2scorerect)
        pygame.display.update()

    currenttime_txt = SCHOOLFONT.render(datetime.now().strftime("%H:%M"), 1, TEXTCOLOR)
    currenttimerect = currenttime_txt.get_rect()
    currenttimerect.center = (100, 45)
    pygame.draw.rect(screen, BGCOLOR, currenttimerect, 0)
    screen.blit(currenttime_txt, currenttimerect)

    updatelist = [time_a_rect, time_b_rect, currenttimerect]

    for event in pygame.event.get():

        if event.type == USEREVENT:
            WriteToBackup()

        elif event.type == KEYDOWN:
            if event.key == K_ESCAPE:
                backup.close()
                print("Purging backup...")
                os.remove('backup.txt')
                exit()

            if event.key == K_SPACE:  # Pause/Play
                if state_a:
                    time_a = timer_txt_a
                    pygame.time.set_timer(USEREVENT, 0)

                if not state_a:
                    start_time_a = time()
                    pygame.time.set_timer(USEREVENT, 100)
                state_a = not state_a

            if event.key in team1scorecontrol:
                if event.key == K_h:
                    team1.score += 1
                elif event.key == K_j:
                    team1.score += 2
                elif event.key == K_k:
                    team1.score += 3
                elif event.key == K_l and team1.score >= 1:
                    team1.score -= 1

                team1score_txt = SCOREFONT.render(str(team1.score), 1, TEXTCOLOR)
                team1scorerect = team1score_txt.get_rect()
                team1scorerect.center = (210, 350)
                pygame.draw.rect(screen, BGCOLOR, team1scorerect, 0)
                screen.blit(team1score_txt, team1scorerect)
                updatelist.append(team1scorerect)

            elif event.key in team2scorecontrol:
                if event.key == K_b:
                    team2.score += 1
                elif event.key == K_n:
                    team2.score += 2
                elif event.key == K_m:
                    team2.score += 3
                elif event.key == K_COMMA and team2.score >= 1:
                    team2.score -= 1

                team2score_txt = SCOREFONT.render(str(team2.score), 1, TEXTCOLOR)
                team2scorerect = team2score_txt.get_rect()
                team2scorerect.center = (1070, 350)
                pygame.draw.rect(screen, BGCOLOR, team2scorerect, 0)
                screen.blit(team2score_txt, team2scorerect)
                updatelist.append(team2scorerect)

            elif event.key in team1foulcontrol:
                if event.key == K_SEMICOLON:
                    team1.fouls += 1
                elif event.key == K_QUOTE and team1.fouls >= 1:
                    team1.fouls -= 1

                team1fouls_txt = FOULNUMBERFONT.render(str(team1.fouls), 1, TEXTCOLOR)
                team1foulsrect = team1fouls_txt.get_rect()
                team1foulsrect.center = (330, 620)
                pygame.draw.rect(screen, BGCOLOR, team1foulsrect, 0)
                screen.blit(team1fouls_txt, team1foulsrect)
                updatelist.append(team1foulsrect)

                for num in range(team1.fouls):
                    if num > 4:
                        num = 4
                    pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (395, 680 - 30 * num, 50, 20))
                    for blanks in range(5 - num):
                        pygame.draw.rect(screen, BGCOLOR, (395, 680 - 30 * (5 - blanks), 50, 20))
                if team1.fouls == 0:
                    pygame.draw.rect(screen, BGCOLOR, (395, 680, 50, 20))
                updatelist.append(foul1region)

            elif event.key in team2foulcontrol:
                if event.key == K_PERIOD:
                    team2.fouls += 1
                elif event.key == K_SLASH and team2.fouls >= 1:
                    team2.fouls -= 1
                team2fouls_txt = FOULNUMBERFONT.render(str(team2.fouls), 1, TEXTCOLOR)
                team2foulsrect = team2fouls_txt.get_rect()
                team2foulsrect.center = (1150, 620)
                pygame.draw.rect(screen, BGCOLOR, team2foulsrect, 0)
                screen.blit(team2fouls_txt, team2foulsrect)
                updatelist.append(team2foulsrect)

                for num in range(team2.fouls):
                    if num > 4:
                        num = 4
                    pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (1215, 680 - 30 * num, 50, 20))
                    for blanks in range(5 - num):
                        pygame.draw.rect(screen, BGCOLOR, (1215, 680 - 30 * (5 - blanks), 50, 20))
                if team2.fouls == 0:
                    pygame.draw.rect(screen, BGCOLOR, (1215, 680, 50, 20))
                updatelist.append(foul2region)

            elif event.key in maintimecontrol:
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

            elif event.key in subtimecontrol:

                if event.key == K_0 or event.key == K_KP0:  # Pause/Play
                    if state_b:
                        time_b = timer_txt_b

                    if not state_b:
                        start_time_b = time()
                    state_b = not state_b

                if event.key == K_1 or event.key == K_KP1:
                    time_b = timer_txt_b = 24
                    start_time_b = time()
                    state_b = True

                if event.key == K_2 or event.key == K_KP2:
                    time_b = timer_txt_b = 14
                    start_time_b = time()
                    state_b = True

            elif event.key in gamecontrol:
                if event.key == K_f:
                    CURRENTPERIOD += 1
                elif event.key == K_v and CURRENTPERIOD >= 2:
                    CURRENTPERIOD -= 1
                elif event.key == K_g:
                    POSSESION = not POSSESION

                if POSSESION:
                    period_txt = TEAMFONT.render('<PERIOD %i  ' % CURRENTPERIOD, 1, TEXTCOLOR)
                elif not POSSESION:
                    period_txt = TEAMFONT.render('  PERIOD %i>' % CURRENTPERIOD, 1, TEXTCOLOR)
                periodrect = period_txt.get_rect()
                periodrect.center = (640, 450)
                pygame.draw.rect(screen, BGCOLOR, periodrect, 0)
                screen.blit(period_txt, periodrect)
                updatelist.append(periodrect)

        WriteToBackup()

    if not state_a:
        updatelist.remove(time_a_rect)
    if not state_b:
        updatelist.remove(time_b_rect)

    pygame.display.update(updatelist)
    clock.tick(20)