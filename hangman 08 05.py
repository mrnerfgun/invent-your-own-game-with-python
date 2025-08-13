import random

HANGMANPICS = ['''
  +---+
      |
      |
      |
     ===''', '''
  +---+
  0   |
      |
      |
     ===''', '''
  +---+
  0   |
  |   |
      |
     ===''', '''
  +---+
  0   |
 /|   |
      |
     ===''', '''
  +---+
  0   |
 /|\  |
      |
     ===''', '''
  +---+
  0   |
 /|\  |
 /    |
     ===''', '''
  +---+
  0   |
 /|\  |
 / \  |
     ===''']

words = 'allay armadillo axolotl bat bee blaze bogged breeze camel cat cave_spider chicken cod cow creaking creeper dolphin donkey drowned elder_guardian ender_dragon enderman endermite evoker fox frog ghast glow_squid goat guardian happy_ghast hoglin horse husk illusioner iron_golem llama magma_cube mooshroom mule ocelot panda parrot phantom pig piglin piglin_brute pillager polar_bear pufferfish rabbit ravager salmon sheep shulker silverfish skeleton skeleton_horse slime sniffer snow_golem spider squid stray strider tadpole trader_llama tropical_fish turtle vex villager vindicator wandering_trader warden witch wither wither_skeleton wolf zoglin zombie zombie_horse zombie_villager zombified_piglin'.split()

def getRandomWord(wordlist):
    wordindex = random.randint(0, len(wordlist) - 1)
    return wordlist[wordindex]

def displayBoard(missedLetters, correctLetters, secretWord):
    print(HANGMANPICS[len(missedLetters)])
    print()

    print('Missed letters:', end=' ')
    for letter in sorted(missedLetters):
        print(letter, end=' ')
    print()

    print('Correct letters:', end=' ')
    for letter in sorted(correctLetters):
        print(letter, end=' ')
    print()
    
    blanks = '_' * len(secretWord)

    
    for i in range(len(secretWord)):
        if secretWord[i] in correctLetters:
            blanks = blanks[:i] + secretWord[i] + blanks[i+1:]

    for letter in blanks:
        print(letter, end=' ')
    print()

def getGuess(alreadyGuessed):
    while True:
        print('Guess a letter.')
        guess = input()
        guess = guess.lower()
        if len(guess) != 1:
            print('You can only guess 1 letter at a time.')
        elif guess in alreadyGuessed:
            print('You already guessed that. Please try again.')
        elif guess not in 'abcdefghijklmnopqrstuvwxyz':
            print('Please guess a letter.')
        else:
            return guess

def giveHint(secretWord, correctLetters):
    #for letter in secretWord:
    unguessedletters=[letter for letter in secretWord if letter not in correctLetters]
    if unguessedletters:
        random_letter = random.choice(unguessedletters)
        print('Hint: one of the letters is: ' + random_letter)
    else:
        print("No hints left! You've guessed all the letters.")



def playAgain():
    print('Do you wanna play again?')
    return input().lower().startswith('y')

print('H A N G M A N')
missedLetters = ''
correctLetters = ''
secretWord = getRandomWord(words)
gameIsDone = False

while True:
    displayBoard(missedLetters, correctLetters, secretWord)

    guess = getGuess(missedLetters + correctLetters)

    if guess in secretWord:
        correctLetters += guess

        foundAllLetters = True
        for i in range(len(secretWord)):
            if secretWord[i] not in correctLetters:
                foundAllLetters = False
                break

        if foundAllLetters:
            print('Yes! The secret word is "' + secretWord + '"! You have won!')
            gameIsDone = True
    else:
        missedLetters += guess

        if len(missedLetters) == len(HANGMANPICS) - 1:
            displayBoard(missedLetters, correctLetters, secretWord)
            print('Oops! You ran out of guesses. Game over. After ' + str(len(missedLetters)) + ' incorrect guesses and ' + str(len(correctLetters)) + ' correct guesses.')
            print('The secret word was "' + secretWord + '".')
            gameIsDone = True


    if len(missedLetters)==3:
        giveHint(secretWord, correctLetters)
    
    if gameIsDone:
        if playAgain():
            missedLetters = ''
            correctLetters = ''
            gameIsDone = False
            secretWord = getRandomWord(words)
        else:
            break
