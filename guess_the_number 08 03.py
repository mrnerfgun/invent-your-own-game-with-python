#Guess the number
import random

guesses=0

print('Hello! What\'s your name?')
PlayerName=input()
print('Well, '+PlayerName+', let\'s play a game in which you guess a number from 1-25!')
print('You have 5 chances.\n')
number=random.randint(1,25)

for i in range(5):
    print('Give it a guess!')
    guess=input()
    guess=int(guess)
    
    if guess > number:
        guesses+=1
        print('That is too large.\n')

    if guess < number:
        guesses+=1
        print('That is too small.\n')
        
    if guess == number:
        guesses+=1
        print('There you go! You guessed it in ' +str(guesses)+ ' moves. Great job!')
        break

if guess!=number:
    print('Game over.')
    print('The number was '+str(number)+'.')
        
