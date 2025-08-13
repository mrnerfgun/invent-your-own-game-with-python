#Caesar Ciphor
SYMBOLS = 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz'
MAX_KEY_SIZE = len(SYMBOLS)

def getMode():
    while True:
        print('Encrypt or Decrypt or brute-force a message?')
        mode = input().lower()
        if mode in ['encrypt', 'e', 'decrypt', 'd', 'brute', 'b']:
            return mode
        else:
            print('Enter e for encrypt, d for decrypt, or b for brute-force.')

def getMessage():
    print('Enter your message:')
    return input()

def getKey():
    while True:
        print('How many letters do you want to shift apart?')
        key = int(input())
        if 1 <= key <= MAX_KEY_SIZE:
            return key

def getTranslatedMessage(mode, message, key):
    if mode[0] == 'd':
        key = -key
    translated = ''
    for symbol in message:
        symbolIndex = SYMBOLS.find(symbol)
        if symbolIndex == -1:
            translated += symbol
        else:
            symbolIndex += key
            if symbolIndex >= len(SYMBOLS):
                symbolIndex -= len(SYMBOLS)
            elif symbolIndex < 0:
                symbolIndex += len(SYMBOLS)
            translated += SYMBOLS[symbolIndex]
    return translated

mode = getMode()
message = getMessage()

if mode[0] != 'b':
    key = getKey()
    print('Your translated text is:')
    print(getTranslatedMessage(mode, message, key))
else:
    print('Brute-force results:')
    for key in range(1, MAX_KEY_SIZE + 1):
        print('Key %s: %s' % (key, getTranslatedMessage('decrypt', message, key)))
