import time, math
ms = time.time() * 1000

x = [
'LLL.LLL.LLLLL.LLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL..LLLLLLL..LLLLLLL.LLLL.LLLLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLL.L.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLL.LLLL.LLLLLLLLL.LLLLL.LLL.LLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLL.LLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLL.LLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLLLLLL.LLLL',
'...L..L.L......LL.L.......L...L..LLL....L.LL.L..L.L.LL..L..L............LLL.L..L.L.L..LL..',
'LLLLLLLLLLLLLLL..LLLLL.L.LLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLL.L.LLLLLL.LLLLLLLL',
'.LLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLL.LL.LLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLL.LLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLL.LLL',
'......L.L.L...LLL.LL...........L.....L..L...LL......L..L.L.L.....LL.LL..L..LL.LL......LLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LL.LLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLL.LLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.L.LLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLL..LLLLLLLLLLLLLL',
'LLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLL.LLLL.LLLLLLLLLLLL.L.LLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLLLLLLL.LLLLLLLLL.LLLLLLL..LLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'L....LL.LL.....LLL.......L.....L.L..L.LL.L...L.L..L.....L...L....LL.LLL...L..L.LL.L..L...L',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LL.LLLL.LL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL..LLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLL.LLLLLL.L',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLL.L.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLLLLLL.LLLLL.LL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLL.LLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLL.LLL',
'L....L......L..L..L.........L...LL..L..L.....L....L.LLL.L..L.LL..L..L..LL...L.......L.L...',
'LLLLLLLLLLLLLLLL..LLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLL.LLLL.LLLLLLLLL.LLLL.LL.LLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLL..LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLL.LLLL.LLLLLLL.LLLLLLLLL.LLL.LLLLLLLL.LLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLL..LLLLLLLLLLLL.LLLLLLLLLLLLL.LLL.LLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLL.LLLLLLLL',
'L...LL..L..L..L.LL..L......L..L..LL.....LL...L...LL..L.L........LL.LL..LL.L......L..L..L..',
'LLLLLLL.LLLLLLLLLLLLLLLL.LLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL..LLLLLL.LLLLLL...LLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLL.LLL.LLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLL.LLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLL.LLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLL.L.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL..LLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'..............L.....L..L..L..L...L......L...LL...................LLLLL..L.LL...L.....L.L..',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLL.LL.LLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLL..LLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLL.LLLLLLLLLL.LLLL.LLLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'L.....L..L...LL...L.L...L..L.....L..L...L....L...L...LL...L......LL..L..LL.L.L..L.L.L.L.L.',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL..LLLLLL.LLLLLLLL.L.LLLL.LLLLLLLL',
'LLLLLLL.LLLLLL.L.LLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLL.LLLLL.LLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLL.LLLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLLLLLLLLL..LLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL..LLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLL.LLLLLLLL',
'LLL..L.L.....L.....LL.L..LL.L.L......L..L.L...L.L....L.....LL..LL.L......L...L....L...L...',
'L.LLLLLLLLLLL.LL.LLLLLLL.LLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLLL.LLLLLLL.LLL.LLLLLL.LLLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLL.LLLLLLLLLLLL.L.LLLLLLL.LLLLLL.LL.LLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLL.LLLLLLLLL.LLLL.LLLLLLLLL.LLLLLLL..LLLLLLLL.LLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLL',
'.LL.....L.L.L...L.L.....L..L..LL....LLL.......L.L.......LL...LLL...L...L...LLL.L...LLLL..L',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLL..LLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLL.LLL.LLLLLLL.LLL.LLLLL.LLLLLLL.LLLLLLLL.LL.LLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLL.LLL.LLL.LLLLLLLLL.LLLLLLLLLLLL.LLLLLLLLLLLLLLLLL.L.LLLLLL.L.LLLLLLLLLLLLL',
'LLLLLLL.LLLLLL.L.LLLLLLL.LLLL..LLLLLLLL.LLLLLLLLLLLL.LLLLLLLLLLLL.L.LLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LL.LLLLLLLLLLLLLL.LLL.LLLL.LLLLL..LLLLLLLL',
'.L..LLL..L..LL...L.L..L......L.L.L..L.....L.....L..L....LLL....L.......L.LLL..LL....L..L.L',
'LLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LL.LLLL.LLLLLLLLLLLLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLL.LL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLL.L.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LL...L.L.L..L.L..........L..L..LL.LL....L.L.L.L.LLL.......L.......L.L....L...L..LL........',
'LLLLLLLLLLLL.LLL.LLLLLLLLLLLL.LLLLLLLLL.LLLL..LLLLLLLLLL....LLLLLLLLLLLLLL..LLLLLLLLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLL.LL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLL.LLLLLLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLLL.LLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL.L.LLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLLLL..LLLL.LLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLLLLLL',
'LLLLL.L.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLLLLLLLLLL.LLLL.LLLLLLL.LLLLLLLLLLL.L.LLLLLL.LLLLLLLL',
'.LLL..L...L.L......LL.L..LL.LL.LLLLL...L...LLLL.L..L..LLL......L...LL.....L..LLLL.LL.LL..L',
'LLLLLLL.LLLLLLLLLLL.LLL..LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLLLL.LLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLL.LL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL.LLLLLLLLLLLLLLLLL.LLLLLLLLLLLLLLLLL.L.LLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLLLLLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLL.LLL',
'L...L.......L..LLLL..L.LL...LL....L.....L.L..L...LLLLL.....LL.....L.L.LLL.L..L.LL.....L.L.',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLLL.LLL.LLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLL.LL.LLLLLLL.LLLLLLLLL.LLLLLLLLLLLLL..L.LLLLLLLLLLLLLLL',
'L.LLLLL.LLLLLLLL.LLLLLLLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLL.L.LLLLLLLLLLLL.LLLLLLLLLLLLLLL.L.LLLLLLLLLLLLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLL.LLL.LLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLL.LLLLLLLL.LLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLLL.LLLLLL.LLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLLLLLLLL.LLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLLLL.L',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLL..LLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLL.LLLLLLLL..LLLLL.LLLLLLLL',
'LLLLLLLLL.LLLLLLLLLLLLLLLLLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLL.LL.LLLLLLLL.LLLLLLLLLLLLLLL',
'LLLLLLLLLLLLLLLL.LLLLLLL.LLLL.LLLLLLLLL.LLLLLLLLLLLLLLLLL.LLLLLLL.LLLLLLLLLLLLLLL.LLLLLLL.',
'LLLLLLL.LLLLLLLL.LLLLLLL.LLLLLLLLLLLLLL.LLLLLLL.LLLLLL.LL.LLLLLLL.LLLLLLLL.LLLLLLLLLLLLLLL',
]

# x = [
# 'L.LL.LL.LL',
# 'LLLLLLL.LL',
# 'L.L.L..L..',
# 'LLLL.LL.LL',
# 'L.LL.LL.LL',
# 'L.LLLLL.LL',
# '..L.L.....',
# 'LLLLLLLLLL',
# 'L.LLLLLL.L',
# 'L.LLLLL.LL',
# ]

def split_all(x):
    a = []
    for row in x:
        a.append(list(row))
    return a

x = split_all(x)

def count_occupied(x, r, c):
    count = 0
    for r1 in range(max(r-1, 0),min(r+2, len(x))):
        row = x[r1]
        for c1 in range(max(c-1,0), min(c+2, len(row))):
            if r1 == r and c1 == c:
                continue
            col = row[c1]
            if col == '#':
                count += 1
    return count

    

def count_occupied_2(x, r, c):
    count = 0
    dirs = [
        (1, 0),
        (1, 1),
        (0, 1),
        (-1, 1),
        (-1, 0),
        (-1, -1),
        (0, -1),
        (1, -1),
    ]
    for d in dirs:
        found = False
        r1 = r
        c1 = c
        while not found:
            r1 += d[0]
            c1 += d[1]
            if r1 < 0 or r1 >= len(x):
                break
            row = x[r1]
            if c1 < 0 or c1 >= len(row):
                break
            p = row[c1]
            if p == '.':
                continue
            found = True
            if p == '#':
                count += 1
    # for r1 in range(max(r-1, 0),min(r+2, len(x))):
    #     row = x[r1]
    #     for c1 in range(max(c-1,0), min(c+2, len(row))):
    #         if r1 == r and c1 == c:
    #             continue
    #         col = row[c1]
    #         if col == '#':
    #             count += 1
    return count

def copy(x):
    a = []
    for row in x:
        a.append(row[:])
    return a


def how_many_occupied(x):
    count = 0
    for row in x:
        for col in row:
            if col == '#':
                count += 1
    return count

def apply_rules(x):
    a = copy(x)
    changes = 0
    for r in range(0, len(x)):
        row = x[r]
        for c in range(0, len(row)):
            col = row[c]
            if col == '.':
                continue
            occ = count_occupied(x, r, c)
            if col == 'L' and occ == 0:
                a[r][c] = '#'
                changes += 1
            if col == '#' and occ >= 4:
                a[r][c] = 'L'
                changes += 1

    return (a, changes)

def apply_rules_2(x):
    a = copy(x)
    changes = 0
    for r in range(0, len(x)):
        row = x[r]
        for c in range(0, len(row)):
            col = row[c]
            if col == '.':
                continue
            occ = count_occupied_2(x, r, c)
            if col == 'L' and occ == 0:
                a[r][c] = '#'
                changes += 1
            if col == '#' and occ >= 5:
                a[r][c] = 'L'
                changes += 1

    return (a, changes)

def dump(x):
    for row in x:
        print(''.join(row))
a = x
while True:
    (a, changes) = apply_rules(a)
    if changes == 0:
        break

print('Occupied Part 1: ', how_many_occupied(a))

a = x
while True:
    (a, changes) = apply_rules_2(a)
    if changes == 0:
        break
    
print('Occupied Part 2: ', how_many_occupied(a))
print(f'Took {time.time()*1000-ms}ms')