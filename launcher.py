#!/usr/bin/python3

from time import sleep

choice = None

while choice != 1 or choice != 2 or choice != 3:
    print("For basketball, please press 1. ")
    print("For football, please press 2. ")
    print("For volleyball, please press 3. ")
    choice = input(": ")

    if choice == '1':
        exec(open("scoreboard.py").read())
    elif choice == '2':
        exec(open("scoreboard-football.py").read())
    elif choice == '3':
        exec(open("scoreboard-volleyball.py").read())
        
    else:
        print("\nInvalid command. \n")
        sleep(0.7)