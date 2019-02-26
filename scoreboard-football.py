#!/usr/bin/python3

# Copyright 2019 Yubin Lee <727yubin@gmail.com>
# Licensed under GPL v3

# Toggleable clock code based on
# https://www.pygame.org/project-Chess+Clock-1991-3512.html
# Used under GPL v3

# A scoreboard for football games

import pygame
from pygame.locals import *
import os
import sys
import time
import datetime
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
    if os.stat("backup-football.txt").st_size == 0:
        os.remove("backup-football.txt")
except:
    pass

time_a = 0
timer_start = 0
a_on = False
recovered = False

# Check if blackout has occurred(quite frequent in Lebanon)
if os.path.isfile('backup-football.txt') and os.stat('backup-football.txt').st_size != 0:
    print('Reloading details from previous game... ')
    backup = open('backup-football.txt', 'r')

    time_a = float(backup.readline().rstrip('\n'))
    team1name = backup.readline().rstrip('\n').upper()
    team2name = backup.readline().rstrip('\n').upper()
    team1score = int(backup.readline().rstrip('\n'))
    team2score = int(backup.readline().rstrip('\n'))

    recovered = True

else:
    team1name = input('Please enter team 1 name: ').upper()
    team2name = input('Please enter team 2 name: ').upper()
    team1score = 0
    team2score = 0
    
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

backup = open('backup-football.txt', 'w')

try: # Fonts
    timefont = pygame.font.Font(basefonttype, timefontsize)
    teamfont = pygame.font.Font(basefonttype, teamfontsize)
    scorefont = pygame.font.Font(basefonttype, scorefontsize)
    foulnumberfont = pygame.font.Font(basefonttype, foulnumberfontsize)
    foulfont = pygame.font.Font(basefonttype, 50)
    credits1font = pygame.font.Font(basefonttype, 20)
    credits2font = pygame.font.Font(basefonttype, 30)
except:
    input("No base font found; please refer to https://github.com/727yubin/Scoreboard")
try:
    schoolfont = pygame.font.Font(schoolfonttype, 80)
except:
    input("No school font found; please refer to https://github.com/727yubin/Scoreboard")

def WriteToBackup():
    backup = open('backup-football.txt', 'w')
    backup.write('{}\n{}\n{}\n{}\n{}\n'.format(str(time_a), team1name, team2name, str(team1score), str(team2score)))
    backup.flush()
    os.fsync(backup.fileno())
    backup.close()

while True:  # Main loop
    for event in pygame.event.get():

        if event.type == KEYDOWN:

            if event.key == K_SPACE and a_on != True:
                if recovered:
                    timer_start = time.time() - time_a
                    a_on = True
                    recovered = False
                else:
                    timer_start = time.time()
                    a_on = True

            if event.key == K_a:
                team1score += 1
            if event.key == K_s:
                team1score -= 1

            if team1score < 0:
                team1score = 0

            if event.key == K_d:
                team2score += 1
            if event.key == K_f:
                team2score -= 1

            if team2score < 0:
                team2score = 0

            if event.key == K_r:
                timer_start = time.time()
                a_on = False

            if event.key == K_ESCAPE:
                backup.close()
                print("Purging backup...")
                os.remove('backup-football.txt')
                sys.exit()

    # Convert to mm:ss
    if a_on:
        time_a = time.time() - timer_start
    elif not recovered:
        time_a = 0
    time_a_str = '%d:%02d' % (int(time_a / 60), int(time_a % 60))

    if int(time_a % 10) % 2 == 0:
        WriteToBackup()

    # Start rendering
    time_a_txt = timefont.render(time_a_str, 1, textcolor)
    time_a_rect = time_a_txt.get_rect()
    time_a_rect.center = (640, 220)

    currenttime_txt = schoolfont.render(datetime.datetime.now().strftime("%H:%M"), 1, textcolor)
    currenttimerect = currenttime_txt.get_rect()
    currenttimerect.center = (100, 50)

    team1name_txt = teamfont.render(team1name, 1, textcolor)
    team1namerect = team1name_txt.get_rect()
    team1namerect.center = (300, 420)

    team2name_txt = teamfont.render(team2name, 1, textcolor)
    team2namerect = team2name_txt.get_rect()
    team2namerect.center = (980, 420)

    team1score_txt = scorefont.render(str(team1score), 1, textcolor)
    team1scorerect = team1score_txt.get_rect()
    team1scorerect.center = (300, 580)

    team2score_txt = scorefont.render(str(team2score), 1, textcolor)
    team2scorerect = team2score_txt.get_rect()
    team2scorerect.center = (980, 580)

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
    pygame.draw.rect(screen, (255, 255, 255), (0, 0, 200, 90), 10)
    pygame.draw.rect(screen, (255, 255, 255), (330, 110, 620, 230), 5)
    screen.blit(school_txt, schoolrect)
    screen.blit(credits1_txt, credits1rect)
    screen.blit(credits2_txt, credits2rect)
    screen.blit(time_a_txt, time_a_rect)
    screen.blit(currenttime_txt, currenttimerect)
    screen.blit(team1name_txt, team1namerect)
    screen.blit(team2name_txt, team2namerect)
    screen.blit(team1score_txt, team1scorerect)
    screen.blit(team2score_txt, team2scorerect)
    
    pygame.display.flip()