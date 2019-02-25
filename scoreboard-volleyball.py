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
    if os.stat("backup-volleyball.txt").st_size == 0:
        os.remove("backup-volleyball.txt")
except:
    pass

currentperiod = 1

scores = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
team1set = 0
team2set = 0

# Check if blackout has occurred(quite frequent in Lebanon)
if os.path.isfile('backup-volleyball.txt') and os.stat('backup-volleyball.txt').st_size != 0:
    print('Reloading details from previous game... ')
    backup = open('backup-volleyball.txt', 'r')

    team1name = backup.readline().rstrip('\n').upper()
    team2name = backup.readline().rstrip('\n').upper()
    scores = literal_eval(backup.readline().rstrip('\n'))
    team1set = int(backup.readline().rstrip('\n'))
    team2set = int(backup.readline().rstrip('\n'))

else:
    team1name = input('Please enter team 1 name: ').upper()
    team2name = input('Please enter team 2 name: ').upper()

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

backup = open('backup-volleyball.txt', 'w')

timefont = pygame.font.Font(basefonttype, timefontsize)
teamfont = pygame.font.Font(basefonttype, teamfontsize)
scorefont = pygame.font.Font(basefonttype, scorefontsize)
foulnumberfont = pygame.font.Font(basefonttype, foulnumberfontsize)
foulfont = pygame.font.Font(basefonttype, 50)
schoolfont = pygame.font.Font(schoolfonttype, 80)
credits1font = pygame.font.Font(basefonttype, 20)
credits2font = pygame.font.Font(basefonttype, 30)


def WriteToBackup():
    backup = open('backup-volleyball.txt', 'w')
    backup.write('{}\n{}\n{}\n{}\n{}\n'.format(team1name, team2name, scores, team1set, team2set))
    backup.flush()
    os.fsync(backup.fileno())
    backup.close()

while True:  # Main loop
    for event in pygame.event.get():

        team1score = scores[currentperiod * 2 - 2]
        team2score = scores[currentperiod * 2 - 1]

        if event.type == KEYDOWN:

            if event.key == K_a:
                team1score += 1
            if event.key == K_z:
                team1score -= 1

            if team1score < 0:
                team1score = 0

            if event.key == K_s:
                team2score += 1
            if event.key == K_x:
                team2score -= 1

            if team2score < 0:
                team2score = 0

            scores[currentperiod * 2 - 2] = team1score
            scores[currentperiod * 2 - 1] = team2score

            if event.key == K_q:
                if team1score > team2score:
                    team1set += 1
                elif team2score > team1score:
                    team2set += 1
                else:
                    currentperiod -= 1
                if currentperiod < 5:
                    currentperiod += 1

            if event.key == K_f:
                team1set += 1
            if event.key == K_v:
                team2set += 1

            if event.key == K_g and team1set > 0:
                team1set -= 1
            if event.key == K_b and team2set > 0:
                team2set -= 1

            if event.key == K_ESCAPE:
                backup.close()
                print("Purging backup...")
                os.remove('backup-volleyball.txt')
                sys.exit()

            WriteToBackup()

    # Start rendering
    team1name_txt = teamfont.render(team1name, 1, textcolor)
    team1namerect = team1name_txt.get_rect()
    team1namerect.center = (250, 180)

    team2name_txt = teamfont.render(team2name, 1, textcolor)
    team2namerect = team2name_txt.get_rect()
    team2namerect.center = (1030, 180)

    team1score_txt = scorefont.render(str(team1score), 1, textcolor)
    team1scorerect = team1score_txt.get_rect()
    team1scorerect.center = (250, 330)

    team2score_txt = scorefont.render(str(team2score), 1, textcolor)
    team2scorerect = team2score_txt.get_rect()
    team2scorerect.center = (1030, 330)

    team1set_txt = foulnumberfont.render(str(team1set), 1, textcolor)
    team1setrect = team1set_txt.get_rect()
    team1setrect.center = (500, 300)

    team2set_txt = foulnumberfont.render(str(team2set), 1, textcolor)
    team2setrect = team2set_txt.get_rect()
    team2setrect.center = (780, 300)

    currenttime_txt = foulnumberfont.render(datetime.datetime.now().strftime("%H:%M"), 1, textcolor)
    currenttimerect = currenttime_txt.get_rect()
    currenttimerect.center = (640, 155)

    set1_txt = foulfont.render("%i:%i" % (scores[0], scores[1]), 1, textcolor)
    set1rect = set1_txt.get_rect()
    set1rect.center = (120, 600)

    set2_txt = foulfont.render("%i:%i" % (scores[2], scores[3]), 1, textcolor)
    set2rect = set2_txt.get_rect()
    set2rect.center = (380, 600)

    set3_txt = foulfont.render("%i:%i" % (scores[4], scores[5]), 1, textcolor)
    set3rect = set3_txt.get_rect()
    set3rect.center = (640, 600)

    set4_txt = foulfont.render("%i:%i" % (scores[6], scores[7]), 1, textcolor)
    set4rect = set4_txt.get_rect()
    set4rect.center = (900, 600)

    set5_txt = foulfont.render("%i:%i" % (scores[8], scores[9]), 1, textcolor)
    set5rect = set5_txt.get_rect()
    set5rect.center = (1160, 600)

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
    pygame.draw.rect(screen, (255, 255, 255), (450, 90, 380, 130), 10)
    screen.blit(school_txt, schoolrect)
    screen.blit(credits1_txt, credits1rect)
    screen.blit(credits2_txt, credits2rect)
    screen.blit(team1name_txt, team1namerect)
    screen.blit(team2name_txt, team2namerect)
    screen.blit(team1score_txt, team1scorerect)
    screen.blit(team2score_txt, team2scorerect)
    screen.blit(team1set_txt, team1setrect)
    screen.blit(team2set_txt, team2setrect)
    screen.blit(set1_txt, set1rect)
    screen.blit(set2_txt, set2rect)
    screen.blit(set3_txt, set3rect)
    screen.blit(set4_txt, set4rect)
    screen.blit(set5_txt, set5rect)
    screen.blit(currenttime_txt, currenttimerect)
    for i in range(5):
        setname_txt = foulfont.render("SET %i" % (i + 1), 1, textcolor)
        setnamerect = setname_txt.get_rect()
        setnamerect.center = (120 + 260 * i, 500)
        screen.blit(setname_txt, setnamerect)
    pygame.display.flip()