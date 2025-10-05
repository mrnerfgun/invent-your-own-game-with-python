import random
import sys

def playGame():
    playerScore=0
    computerScore=0
    winningScore=100

    print('\nNew game started')
    print(f'First to reach {winningScore} points wins!')
    while playerScore<winningScore and computerScore<winningScore:
        input('\nPress enter to roll the dice.')
        player_roll=random.randint(1, 6)
        computer_roll=random.randint(1, 6)
        print(f'\nYou rolled a {player_roll}.')
        print(f'Computer rolled a {computer_roll}')
        if player_roll>computer_roll:
            playerScore+=1
            print('You win this round')
        elif player_roll<computer_roll:
            computerScore+=1
            print('You lose this round')
        else:
            print('Its a tie')
        
        print(f"Score => You: {playerScore} | Computer: {computerScore}")

    if playerScore==winningScore:
        print('\nYou win!')
    elif computerScore==winningScore:
        print('\nComputer wins!')
    
while True:
    playGame()
    replay=input('\nDo you wanna play again? ')
    if not replay.startswith('y'):
        print('You quit.')
        sys.exit()