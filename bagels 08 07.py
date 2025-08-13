# Bagels
import random

NUM_DIGITS = 3
MAX_GUESSES = 10

def getSecretNum():
    numbers = list(range(10))
    random.shuffle(numbers)
    secretNum = ''
    for i in range(NUM_DIGITS):
        secretNum += str(numbers[i])
    return secretNum

def getClues(guess, secretNum):
    if guess == secretNum:
        return 'You got it!'

    clues = []
    secret_used = [False] * len(secretNum)
    guess_used = [False] * len(guess)

    for i in range(len(secretNum)):
        if guess[i] == secretNum[i]:
            clues.append('Fermi')
            secret_used[i] = True
            guess_used[i] = True

    for i in range(len(guess)):
        if guess_used[i]:
            continue
        for j in range(len(secretNum)):
            if not secret_used[j] and guess[i] == secretNum[j]:
                clues.append('Pico')
                secret_used[j] = True
                break

    if len(clues) == 0:
        return 'Bagels'

    clues.sort()
    return ' '.join(clues)

def isOnlyDigits(num):
    return num.isdigit()

print('I am thinking of a %s-digit number. Try and guess it.' % (NUM_DIGITS))
print('The clues I give are...')
print('When I say:             That means:')
print('Bagels                  None of the guessed digits are correct')
print('Pico                    One digit is correct but in the wrong place')
print('Fermi                   One digit is correct and in the right place')
print()
print('You cannot have repeated digits in a guess.')

while True:
    secretNum = getSecretNum()
    print('\nI have thought up a number. You have %s guesses to get it.' % (MAX_GUESSES))
    guessesTaken = 1

    while guessesTaken <= MAX_GUESSES:
        guess = ''
        while len(guess) != NUM_DIGITS or not isOnlyDigits(guess):
            print('Guess #%s' % (guessesTaken))
            guess = input('> ')

        print(getClues(guess, secretNum))
        guessesTaken += 1

        if guess == secretNum:
            break
        if guessesTaken > MAX_GUESSES:
            print('OOPS! You ran out of guesses. The answer was %s.' % (secretNum))

    print('Do you want to play again? (yes or no)')
    if not input('> ').lower().startswith('y'):
        break
