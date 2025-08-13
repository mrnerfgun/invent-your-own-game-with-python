#Dragon Realm
import random
import time

def intro():
    print('You are in front of 2 caves: one with a friendly dragon who will give you all of his treasure,')
    print('and the other with an evil dragon who will gobble you up and will not give you his treasure.')
    print('You don\'t know which cave the friendly and evil dragons live in.')
    print()

def chooseCave():
    cave = ''
    while cave != '1' and cave != '2':
        print('Which one will you go into? 1 or 2')
        cave = input()
    return cave

def checkCave(chosen_cave):
    print('You go into the cave......')
    time.sleep(2)
    print('It is dark and spooky.....')
    time.sleep(2)
    print('A gigantic dragon appears. He lifts his jaws and......')
    print()
    time.sleep(2)
    goodCave = random.randint(1,2)

    tmp = int(chosen_cave)
    print(type(tmp))
    print(type(goodCave))
    print(type(chosen_cave))
    print(goodCave)
    print(chosen_cave)
    if tmp == goodCave:
        print('Gives you all of his treasure!')
        
    else:
        print('Gobbles you up in 1 bite!')
    
    
playAgain = 'yes'
while playAgain == 'yes' or playAgain == 'y':

    for i in range(10000000):    
        intro()

        caveNumber = chooseCave()

        checkCave(caveNumber)
    
    print('Do you want to play again? yes or no')
    playAgain = input()
        
