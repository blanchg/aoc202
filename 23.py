import time
from collections import deque, defaultdict
ms = time.time() * 1000

def printcups(currenti, cups):
    out = [f'({cups[i]})' if currenti == i else str(cup) for i,cup in enumerate(cups)]
    return ' '.join(out)

def pickcups(currenti, cups):
    out = []
    for i in range(currenti + 1, currenti + 4):
        out.append(cups[i % len(cups)])
    return out

def get_destination(currenti, cups: list, pickup):
    maxcup = max(cups)
    current = cups[currenti]
    target = current - 1
    while True:
        if target <= 0:
            target = maxcup
        if target not in pickup:
            break
        target -= 1
        
    return cups.index(target)

def movecups(cups, currenti, desti, pickup):
    current = cups[currenti]
    dest = cups[desti]
    b = cups[0:currenti]
    a = [current] + cups[currenti + 4:]
    # print(a)
    # print(b)
    working = a + b
    # print('working', working)

    desti = working.index(dest)

    out = working[0:desti+1] + pickup + working[desti+1:]
    return out


def run1():
    working = cups[:]
    # working = [3,8,9,1,2,5,4,6,7]
    currenti = 0
    for move in range(1, 101):
        current = working[currenti]
        # print(f'-- move {move} --')
        # print(f'cups: {printcups(currenti, working)}')
        pickup = pickcups(currenti, working)
        # print(f'pick up: {pickup}')
        desti = get_destination(currenti, working, pickup)
        # print(f'destination: {working[desti]}')
        working = movecups(working, currenti, desti, pickup)
        currenti = (working.index(current) + 1) % len(working)
        # print()

    offset = working.index(1)
    out = ''
    for i in range(1, len(working)):
        out += str(working[(i + offset) % len(working)])

    return out

class RingItem:
    clockwise = None
    def __init__(self, value) -> None:
        super().__init__()
        self.value = value

class LinkedRing:
    head: RingItem = None
    def __init__(self, iterable):
        self.index = {}
        self.maxvalue = 0
        prev:RingItem = None
        for i in iterable:
            if i > self.maxvalue:
                self.maxvalue = i
            current = RingItem(i)
            self.index[i] = current
            if prev == None:
                self.head = current
            else:
                prev.clockwise = current
            prev = current
        prev.clockwise = self.head
        print('max', self.maxvalue)
        print('head', self.head.value)
        print('tail', prev.value, prev)
        print('index', self.index[prev.value])

    def __getitem__(self, value) -> RingItem:
        return self.index[value]

    def __repr__(self):
        out = []
        out.append(str(self.head.value))
        current = self.head.clockwise
        while current != self.head:
            val = str(current.value)
            if val in out:
                raise Exception(f"Broken ring ({val})" + str(out))
            out.append(str(current.value))
            # print(out)
            current = current.clockwise

        return ' '.join(out)

    def insert_after(self, value, iterable):
        prev = self.index[value]
        rightmost = prev.clockwise
        # print('Inserting between', prev.value, rightmost.value)
        for i in iterable:
            current = self.index[i]
            # print('  ', prev.value, '->', current.value)
            prev.clockwise = current
            prev = current
        prev.clockwise = rightmost
        # print('joining', prev.value, '->', rightmost.value)
        # print('rightmost ->', rightmost.clockwise.value)

    def remove_after(self, value, num):
        values = []
        first = self.index[value]
        prev = self.index[value]
        # print('removing',num,'after',value)
        for i in range(0, num):
            current = prev.clockwise
            prev.clockwise = None
            values.append(current.value)
            prev = current
        # print('removed', values)
        # print('linking', first.value, '->', prev.clockwise.value)
        first.clockwise = prev.clockwise
        return values

    def clockwise(self, value):
        return self.index[value].clockwise.value


def movecupsll(cups: LinkedRing, dest, pickup):
    cups.insert_after(dest, pickup)
    return cups

def pickcupsll(value, cups: LinkedRing):
    out = cups.remove_after(value, 3)
    return out

def get_destinationll(current, cups: LinkedRing, pickup):
    maxcup = cups.maxvalue
    target = current - 1
    while True:
        if target <= 0:
            target = maxcup
        if target not in pickup:
            break
        target -= 1
    return target

def run2():
    working = cups[:]
    largest = max(working)
    for i in range(largest + 1,1000000+1):
        working.append(i)
    # working = [3,8,9,1,2,5,4,6,7]
    working = LinkedRing(working)
    current = cups[0]
    for move in range(1, 10000001):
        # print(f'-- move {move} --')
        # print(f'cups: {current}, {working}')
        pickup = pickcupsll(current, working)
        # print(f'pick up: {pickup}')
        dest = get_destinationll(current, working, pickup)
        # print(f'destination: {dest}')
        working = movecupsll(working, dest, pickup)
        current = working.clockwise(current)
        # print()
        if move % 100000 == 0:
            print(move)

    # print(working)

    c1 = working.clockwise(1)
    c2 = working.clockwise(c1)
    print('Values clockwise of 1', c1, c2)

    return c1 * c2

cups = [1,5,7,6,2,3,9,8,4]

part1 = run1()
print(f'Part1: {part1}')


part2 = run2()
print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')