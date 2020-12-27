import time
from collections import deque, defaultdict
ms = time.time() * 1000


def encrypt(sn, loops):
    val = 1
    for l in range(0, loops):
        val = val * sn
        val = val % 20201227
    return val

def run1():
    result = 0
    # cardkey = 5764801
    cardloops = 0
    # doorkey = 17807724
    doorloops = 0
    sn = 7
    cardval = 1
    doorval = 1
    i = 1

    while True:
        cardval = (cardval * sn) % 20201227
        doorval = (doorval * sn) % 20201227
        if cardval == cardkey:
            print('Card key loops found', i)
            cardloops = i
            val = encrypt(doorkey, cardloops)
            print('Card encryption key', val)
            return val
        elif doorval == doorkey:
            print('door key loops found', i)
            doorloops = i
            val = encrypt(cardkey, doorloops)
            print('Door encryption key', val)
            return val
        # print(i)
        i += 1

def run2():
    result = 1
    return result


cardkey = 8987316
doorkey = 14681524

part1 = run1()
print(f'Part1: {part1}')


part2 = run2()
print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')