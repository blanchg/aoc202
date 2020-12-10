import time
from collections import defaultdict
ms = time.time()*1000

x = [
178, 135, 78, 181, 137, 16, 74, 11, 142, 109, 148, 108, 151, 184, 121, 58, 110, 52, 169, 128, 2, 119, 38, 136, 25, 26, 73, 157, 153, 7, 19, 160, 4, 80, 10, 51, 1, 131, 55, 86, 87, 21, 46, 88, 173, 71, 64, 114, 120, 167, 172, 145, 130, 33, 20, 190, 35, 79, 162, 122, 98, 177, 179, 68, 48, 118, 125, 192, 174, 99, 152, 3, 89, 105, 180, 191, 61, 13, 90, 129, 47, 138, 67, 115, 44, 59, 60, 95, 93, 166, 154, 101, 34, 113, 139, 77, 94, 161, 187, 45, 22, 12, 163, 41, 27, 132, 30, 143, 168, 144, 83, 100, 102, 72,
]

# x = [
# 28, 33, 18, 42, 31, 14, 46, 20, 48, 47, 24, 23, 49, 45, 19, 38, 39, 11, 1, 32, 25, 35, 8, 17, 7, 9, 4, 2, 34, 10, 3,
# ]

# x = [
# 16, 10, 15, 5, 1, 11, 7, 19, 6, 12, 4,
# ]
wall = 0
x.append(wall)
laptop = max(x) + 3
x.append(laptop)
x = sorted(x)
print(x)
#print(x)
diffs = defaultdict(int)
last = x[0]
for n in x[1:]:
    diff = n-last
    if diff > 3 or diff < 1:
        print('Failed')
        break
    diffs[diff] += 1
    last = n
print(diffs)
print('Part1:', diffs[1] * diffs[3])

valuemap = {
    3: 2,
    4: 4,
    5: 7,
}
i = 0
contig = 1
count = 0
parts = []
for n in x[1:]:
    if i+1 == n:
        contig += 1
    elif i+3 == n:
        if contig > 2:
            print(contig, valuemap[contig])
            parts.append(valuemap[contig])
        contig = 1
    i = n
print(parts)
import functools, operator
result = functools.reduce(operator.mul, parts)

print('Part2: ', result)
# class Path:
#     def __init__(self, i, parts):
#         self.i = i
#         self.parts = parts

#     def __repr__(self):
#         return f"{self.i} -> {self.parts}"

# x = x[1:-1] # remove first and last one
# print('Wall:', wall, 'Laptop:', laptop)
# count = 0
# paths = []
# xlen = len(x)
# paths.append(Path(-1, [wall]))
# r = 0
# while paths:
#     #print(paths)
#     path = paths.pop()
#     i = path.i

#     a = path.parts[-1]
#     if laptop - a < 4 and laptop - a > 0:
#         count += 1
#        # print("***",path)
#         if i >= xlen:
#             continue
#         #paths.append(path)
#     if i+1 < xlen and x[i+1]-a < 4:
#         a1 = x[i+1]
#         p = path.parts[:]
#         p.append(a1)
#         paths.append(Path(i+1,p))
#     if i+2 < xlen and x[i+2]-a < 4:
#         a2 = x[i+2]
#         p = path.parts[:]
#         p.append(a2)
#         paths.append(Path(i+2,p))
#     if i+3 < xlen and x[i+3]-a < 4:
#         a3 = x[i+3]
#         p = path.parts[:]
#         p.append(a3)
#         paths.append(Path(i+3,p))

#     r += 1
#     if r % 1000000 == 0:
#         print(count, len(paths), path)

# dfs
print(f"Part2: {count}")


print(f"Took {time.time()*1000-ms}ms")