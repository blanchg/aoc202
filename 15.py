import time
from collections import defaultdict 
ms = time.time() * 1000

x = [2,15,0,9,1,20]

# x = [0,3,6]
# x=[3,2,1]

def run1(x, num):
    spoken = defaultdict(int)
    for i,a in enumerate(x[:-1]):
        spoken[a] = i+1

        print(f'{i+1:4d}: {a}')

    this = x[-1]

    for i in range(len(x), num):
        #print(f'{i:4d}: {this}')
        #print(i, spoken)
        val = spoken[this]
        spoken[this] = i
        if val != 0:
            val = i - val
        this = val
        if i % 1000000 == 0:
            print(f'{i:4d}: {val}')


    return this

part1 = run1(x, 2020)

print(f'Part1: {part1}')

part2 = run1(x, 30000000)

print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')