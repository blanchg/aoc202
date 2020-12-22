import time
from collections import deque, defaultdict
ms = time.time() * 1000

def run1():
    result = 0
    while True:
        if len(p1) == 0 or len(p2) == 0:
            break
        p1c = p1.popleft()
        p2c = p2.popleft()
        if p1c > p2c:
            p1.append(p1c)
            p1.append(p2c)
        else:
            p2.append(p2c)
            p2.append(p1c)

    winner = p1 if p1 else p2
    mul = len(winner)
    for card in winner:
        result += mul * card
        mul -= 1
    print(p1)
    print(p2)
    return result

p1 = deque([7,1,9,10,12,4,38,22,18,3,27,31,43,33,47,42,21,24,50,39,8,6,16,46,11])

p2 = deque([49,41,40,35,44,29,30,19,14,2,34,17,25,5,15,32,20,48,45,26,37,28,36,23,13])

gamestotal = 1

def recursive(p1, p2) -> (bool, deque):
    global gamestotal
    game = gamestotal

    rounds = []
    round = 1
    # print(f'=== Game {game} ===')
    # print()
    while True:
        # print(f'-- Round {round} (Game {game}) --')
        key = ','.join([str(x) for x in p1]) + '|' + ','.join([str(x) for x in p2])
        d1 = ', '.join([str(x) for x in p1])
        d2 = ', '.join([str(x) for x in p2])
        # print(f'Player 1\'s deck: {d1}')
        # print(f'Player 2\'s deck: {d2}')
        if key in rounds:
            # print(f'Player 1 wins repeat round {round} of game {game}!')
            return (1, p1)
        rounds.append(key)
        if len(p1) == 0 or len(p2) == 0:
            break
        p1c = p1.popleft()
        p2c = p2.popleft()
        # print(f'Player 1 plays: {p1c}')
        # print(f'Player 2 plays: {p2c}')
        if p1c <= len(p1) and p2c <= len(p2):
            # print('Playing a sub-game to determine the winner...')
            # print()
            gamestotal += 1
            (winner, _) = recursive(deque(list(p1)[0:p1c]), deque(list(p2)[0:p2c]))
            # print(f'The winner of game {gamestotal} is player {winner}!')
            # print()
            # print(f'...anyway, back to game {game}.')
        elif p1c > p2c:
            winner = 1
        else:
            winner = 2
        # print(f'Player {winner} wins round {round} of game {game}!')
        # print()
        if winner == 1:
            p1.append(p1c)
            p1.append(p2c)
        else:
            p2.append(p2c)
            p2.append(p1c)
        round += 1
    
    if p1:
        return (1, p1)
    else:
        return (2, p2)

def run2():
    result = 0
    # p1 = deque([9, 2, 6, 3, 1])
    # p2 = deque([5, 8, 4, 7, 10])
    winner, cards = recursive(p1, p2)
    print(winner, cards)
    mul = len(cards)
    for card in cards:
        result += mul * card
        mul -= 1
    return result


part1 = run1()
print(f'Part1: {part1}')

p1 = deque([7,1,9,10,12,4,38,22,18,3,27,31,43,33,47,42,21,24,50,39,8,6,16,46,11])

p2 = deque([49,41,40,35,44,29,30,19,14,2,34,17,25,5,15,32,20,48,45,26,37,28,36,23,13])

part2 = run2()
print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')

