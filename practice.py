import asyncio
import random
"""

async def make_coffee():
    print('making coffee...')
    await asyncio.sleep(3)
    print('ready')

async def make_toast():
    print('making toast...')
    await asyncio.sleep(2)
    print('toast is ready')

async def main():
    c=asyncio.create_task(make_coffee())
    t=asyncio.create_task(make_toast())

    print('both tasks started')
    await c
    await t
asyncio.run(main())

async def download_file(name):
    download_time=random.randint(1, 5)
    print(f'{name} will take {download_time} seconds to download')
    await asyncio.sleep(download_time)
    print(f'{name} is done!')

async def main():
    a=asyncio.create_task(download_file('a'))
    b=asyncio.create_task(download_file('b'))

    await a
    await b

    print('downloaded')

asyncio.run(main())

async def runner(name):
    time=random.randint(1, 5)
    print(f'{name} will take {time} seconds to finish')
    await asyncio.sleep(time)
    print(f'{name} is done')
    return name

async def main():
    runners=['a', 'b']
    task = [asyncio.create_task(runner(name)) for name in runners]
    done, pending = await asyncio.wait(task, return_when=asyncio.FIRST_COMPLETED)
    for task in done:
        winner = task.result()

    print(f'{winner} won!')
    await asyncio.gather(*pending)
    print('The race is completed.')

asyncio.run(main())

def is_palindrome(s):
    s = s.replace(" ", "").lower()
    r_s=s[::-1]
    if r_s.lower()==s.lower():
        return True
    else:
        return False

print(is_palindrome('12 21'))

def count_vowels(s):
    count=0
    vowels=['a', 'e', 'i', 'o', 'u']
    for char in s:
        if char.lower() in vowels:
            count+=1
        else:
            count=count

    return count

print(count_vowels('aeiou'))

def is_unique(s):
    s = s.lower().replace(" ", "")
    if len(set(s)) == len(s):
        return True
    return False

print(is_unique('SIX SEVEN'))

def count_avg():
    x=1
    total=0
    while x<=6:
        score=float(input('Enter a test score: '))
        total+=score
        x+=1
    print(round(total/6))

count_avg()"""

