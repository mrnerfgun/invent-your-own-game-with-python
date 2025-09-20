import random
import sys

playerHP=100
inventory={"potions":1, "gold":0}
gameIsRunning=True
while gameIsRunning and playerHP>0:
    print("What do you wanna do?")
    actions=input("[explore] [use potion] [stats] [quit] > ").lower()
    if actions=='explore':
        room=random.choice(['monster', 'treasure', 'empty', 'exit'])
        if room=='monster':
            print('You encountered a monster! Prepare to kill it.')
            monsterHP=random.randint(30, 70)
            print(f'Monster\'s HP is {monsterHP}.')
            while monsterHP>0 and playerHP>0:
                player_attack = random.randint(5, 10)
                monsterHP -= player_attack
                print(f"You hit for {player_attack}")

                if monsterHP <= 0:
                    break

                monster_attack = random.randint(5, 15)
                playerHP -= monster_attack
                print(f"Monster hits for {monster_attack}")
            if playerHP<=0:
                print('You died!')
                gameIsRunning=False
                playAgain=input('Do you wanna play again? ').lower()
                if playAgain.startswith('y'):
                    gameIsRunning=True
                    playerHP=100
                    print('You chose to play again.')
                    inventory = {"potions": 1, "gold": 0}
                else:
                    gameIsRunning=False
                    print('You quit. Thanks for playing!')
                    sys.exit()
            elif monsterHP<=0:
                print('You defeated the monster!')
                inventory['gold']+=20
        elif room=='treasure':
            gold_found=random.randint(10, 50)
            potions_found=random.randint(1, 3)
            inventory['gold']+=gold_found
            inventory['potions']+=potions_found
            print(f'You found a treasure chest with {gold_found} gold and {potions_found} potions!')
        elif room=='empty':
            print('The room is empty.')
        else:
            print(f'You found a way out! You leave the dungeon with {inventory["gold"]} gold!')
            playAgain=input('Do you wanna play again? ').lower()
            if playAgain.startswith('y'):
                gameIsRunning=True
                playerHP=100
                print('You chose to play again.')
                inventory = {"potions": 1, "gold": 0}
            else:
                gameIsRunning=False
                print('You quit. Thanks for playing!')
                sys.exit()
    elif actions == 'use potion':
        if inventory['potions'] > 0:
            playerHP += 30
            if playerHP > 100:
                playerHP = 100  
            inventory['potions'] -= 1
            print(f'You used a potion and restored health. HP is now {playerHP}.')
        else:
            print("You don't have any potions!")
    elif actions=='stats':
        print(f"HP: {playerHP} | Potions: {inventory['potions']} | Gold: {inventory['gold']}")
    elif actions=='quit':
        gameIsRunning=False
        print('You quit.')
        sys.exit()
    else:
        print('Invalid command. Try again')