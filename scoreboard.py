#!/usr/bin/python3

# Copyright 2019 Yubin Lee <727yubin@gmail.com>
# Licensed under GPL v3

# Toggleable clock code based on
# https://www.pygame.org/project-Chess+Clock-1991-3512.html
# Used under GPL v3

# A scoreboard for (primarily) basketball games

import pygame
from pygame.locals import *
import os
import sys
from ast import literal_eval  # For getting tuples from config

# Check for config file
try:
    config = open('config.txt', 'r')
except FileNotFoundError:
    print('Configuration file not found.')
    input('Please download https://github.com/727yubin/Scoreboard/blob/master/config.txt')
    sys.exit()

print('')

# School logo
try:
    logo = pygame.image.load('logo.png')
    logo = pygame.transform.scale(logo, (80, 80))
except:
    print('School logo not found.')
    input('Please place your logo as logo.png in the same directory')
    sys.exit()

try:
    if os.stat("backup.txt").st_size == 0:
        os.remove("backup.txt")
except:
    pass

time_a = 0
a_on = False

time_b = 24
b_on = False

# Check if blackout has occurred(quite frequent in Lebanon)
if os.path.isfile('backup.txt') and os.stat('backup.txt').st_size != 0:
    print('Reloading details from previous game... ')
    backup = open('backup.txt', 'r')

    time_a = float(backup.readline().rstrip('\n'))
    time_b = float(backup.readline().rstrip('\n'))
    team1name = backup.readline().rstrip('\n').upper()
    team2name = backup.readline().rstrip('\n').upper()
    team1score = int(backup.readline().rstrip('\n'))
    team2score = int(backup.readline().rstrip('\n'))
    currentperiod = int(backup.readline().rstrip('\n'))
    team1fouls = int(backup.readline().rstrip('\n'))
    team2fouls = int(backup.readline().rstrip('\n'))
    possesion = bool(backup.readline().rstrip('\n'))

else:
    team1name = input('Please enter team 1 name: ').upper()
    team2name = input('Please enter team 2 name: ').upper()
    team1score = 0
    team2score = 0
    currentperiod = 1
    team1fouls = 0
    team2fouls = 0
    possesion = False

# Get values from config file
bgcolor = literal_eval(config.readline().rstrip('\n'))
textcolor = literal_eval(config.readline().rstrip('\n'))
timefontsize = int(config.readline().rstrip('\n'))
teamfontsize = int(config.readline().rstrip('\n'))
scorefontsize = int(config.readline().rstrip('\n'))
foulnumberfontsize = int(config.readline().rstrip('\n'))
basefonttype = config.readline().rstrip('\n')
schoolfonttype = config.readline().rstrip('\n')

# Basic pygame stuff
pygame.init()
pygame.display.init()
screen = pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
background = pygame.Surface(screen.get_size())
rect = background.fill(bgcolor)
clock = pygame.time.Clock()
pygame.mouse.set_visible(0)

backup = open('backup.txt', 'w')

timefont = pygame.font.Font(basefonttype, timefontsize)
teamfont = pygame.font.Font(basefonttype, teamfontsize)
scorefont = pygame.font.Font(basefonttype, scorefontsize)
foulnumberfont = pygame.font.Font(basefonttype, foulnumberfontsize)
foulfont = pygame.font.Font(basefonttype, 50)
schoolfont = pygame.font.Font(schoolfonttype, 80)
credits1font = pygame.font.Font(basefonttype, 20)
credits2font = pygame.font.Font(basefonttype, 30)


def WriteToBackup():
    backup = open('backup.txt', 'w')
    backup.write('{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n{}\n'.format(
        str(time_a), str(time_b), team1name, team2name, str(team1score),
        str(team2score), str(currentperiod), str(team1fouls),
        str(team2fouls), str(possesion)))
    backup.flush()
    os.fsync(backup.fileno())
    backup.close()

while True:  # Main loop
    for event in pygame.event.get():

        if event.type == USEREVENT:  # Countdown timer
            if time_a > 0:
                time_a -= 0.1
                time_a = round(time_a, 1)
            else:
                pygame.time.set_timer(USEREVENT, 0)
            WriteToBackup()

        if event.type == USEREVENT + 1:
            if time_b > 0:
                time_b -= 0.1
                time_b = round(time_b, 1)
            else:
                pygame.time.set_timer(USEREVENT + 1, 0)

        if event.type == KEYDOWN:

            if event.key == K_SPACE:  # Pause/Play
                if not a_on:
                    pygame.time.set_timer(USEREVENT, 100)
                    a_on = True
                else:
                    pygame.time.set_timer(USEREVENT, 0)
                    a_on = False

            if event.key == K_0 or event.key == K_KP0:
                if not b_on:
                    pygame.time.set_timer(USEREVENT + 1, 100)
                    b_on = True
                else:
                    pygame.time.set_timer(USEREVENT + 1, 0)
                    b_on = False

            if event.key == K_a:
                time_a += 60
            if event.key == K_s:
                time_a += 1
            if event.key == K_d:
                time_a += 0.1

            if event.key == K_z:
                time_a -= 60
            if event.key == K_x:
                time_a -= 1
            if event.key == K_c:
                time_a -= 0.1

            if event.key == K_f:
                currentperiod += 1
            if event.key == K_v:
                currentperiod -= 1
            
            if currentperiod < 1:
                currentperiod = 1

            if event.key == K_h:
                team1score += 1
            if event.key == K_j:
                team1score += 2
            if event.key == K_k:
                team1score += 3
            if event.key == K_l:
                team1score -= 1

            if team1score < 0:
                team1score = 0

            if event.key == K_SEMICOLON:
                team1fouls += 1
            if event.key == K_QUOTE:
                team1fouls -= 1

            if team1fouls < 0:
                team1fouls = 0

            if event.key == K_b:
                team2score += 1
            if event.key == K_n:
                team2score += 2
            if event.key == K_m:
                team2score += 3
            if event.key == K_COMMA:
                team2score -= 1

            if team2score < 0:
                team2score = 0

            if event.key == K_PERIOD:
                team2fouls += 1
            if event.key == K_SLASH:
                team2fouls -= 1

            if team2fouls < 0:
                team2fouls = 0

            if event.key == K_g:
                possesion = not possesion

            if event.key == K_1 or event.key == K_KP1:
                time_b = 24
                pygame.time.set_timer(USEREVENT + 1, 100)

            if event.key == K_2 or event.key == K_KP2:
                time_b = 14
                pygame.time.set_timer(USEREVENT + 1, 100)

            if event.key == K_ESCAPE:
                backup.close()
                print("Purging backup...")
                os.remove('backup.txt')
                sys.exit()

            WriteToBackup()

    if time_a <= 0:
        time_a = 0
        a_on = False
        pygame.time.set_timer(USEREVENT, 0)

    # Switch between mm:ss and ss.c
    if time_a > 60:
        time_a_str = '%d:%02d' % (int(time_a / 60), int(time_a % 60))
    else:
        time_a_str = '%.1f' % time_a

    if time_b < 10:
        time_b_str = '%.1f' % time_b
    else:
        time_b_str = str(int(time_b))

    # Start rendering
    time_a_txt = timefont.render(time_a_str, 1, textcolor)
    time_a_rect = time_a_txt.get_rect()
    time_a_rect.center = (640, 220)

    time_b_txt = foulnumberfont.render(time_b_str, 1, textcolor)
    time_b_rect = time_b_txt.get_rect()
    time_b_rect.center = (640, 560)

    team1name_txt = teamfont.render(team1name, 1, textcolor)
    team1namerect = team1name_txt.get_rect()
    team1namerect.center = (250, 500)

    team2name_txt = teamfont.render(team2name, 1, textcolor)
    team2namerect = team2name_txt.get_rect()
    team2namerect.center = (1030, 500)

    team1score_txt = scorefont.render(str(team1score), 1, textcolor)
    team1scorerect = team1score_txt.get_rect()
    team1scorerect.center = (210, 350)

    team2score_txt = scorefont.render(str(team2score), 1, textcolor)
    team2scorerect = team2score_txt.get_rect()
    team2scorerect.center = (1070, 350)

    period_txt = teamfont.render('PERIOD %i' % currentperiod, 1, textcolor)
    periodrect = period_txt.get_rect()
    periodrect.center = (640, 390)

    foul_txt = foulfont.render('FOULS', 1, textcolor)
    foultextrect1 = foul_txt.get_rect()
    foultextrect1.center = (130, 620)
    foultextrect2 = foul_txt.get_rect()
    foultextrect2.center = (950, 620)

    team1fouls_txt = foulnumberfont.render(str(team1fouls), 1, textcolor)
    team1foulsrect = team1fouls_txt.get_rect()
    team1foulsrect.center = (330, 620)

    team2fouls_txt = foulnumberfont.render(str(team2fouls), 1, textcolor)
    team2foulsrect = team2fouls_txt.get_rect()
    team2foulsrect.center = (1150, 620)

    if possesion:
        possesion_txt = teamfont.render('>', 1, textcolor)
        possesionrect = possesion_txt.get_rect()
        possesionrect.center = (920, 390)

    elif not possesion:
        possesion_txt = teamfont.render('<', 1, textcolor)
        possesionrect = possesion_txt.get_rect()
        possesionrect.center = (350, 390)

    school_txt = schoolfont.render('LES Loueizeh', 1, textcolor)
    schoolrect = school_txt.get_rect()
    schoolrect.center = (690, 50)

    credits1_txt = credits1font.render("Programmed by:", 1, textcolor)
    credits1rect = credits1_txt.get_rect()
    credits1rect.center = (1200, 45)

    credits2_txt = credits2font.render("Yubin Lee '19", 1, textcolor)
    credits2rect = credits1_txt.get_rect()
    credits2rect.center = (1170, 65)

    # Blit everything
    screen.blit(background, rect)
    screen.blit(logo, (350, 0))
    pygame.draw.rect(screen, (255, 255, 255), (0, 90, 1280, 630), 10)
    pygame.draw.rect(screen, (255, 255, 255), (330, 110, 620, 230), 5)
    pygame.draw.rect(screen, (255, 255, 255), (520, 470, 240, 180), 5)
    screen.blit(school_txt, schoolrect)
    screen.blit(credits1_txt, credits1rect)
    screen.blit(credits2_txt, credits2rect)

    for num in range(team1fouls):
        if num > 4: # 5 fouls, but num starts from 0
            num = 4
        pygame.draw.rect(screen, (63 * num, 252 - 63 * num, 0), (395, 680 - 30 * num, 50, 20))
    
    for num in range(team2fouls):
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