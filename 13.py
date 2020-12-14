import time
ms = time.time() * 1000

import math

arrive = 1006726
busses = [23,'x','x','x','x','x','x','x','x','x','x','x','x',41,'x','x','x','x','x','x','x','x','x',647,'x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x','x',13,19,'x','x','x','x','x','x','x','x','x',29,'x',557,'x','x','x','x','x',37,'x','x','x','x','x','x','x','x','x','x',17]
print(arrive)
earliest = arrive * 2
ebus = -1
for bus in busses:
    if bus == 'x':
        continue
    toa = math.ceil(arrive / bus) * bus
    print(f'{bus}: {toa}')
    if toa < earliest:
        earliest = toa
        ebus = bus

print(earliest)
print(earliest - arrive)
print('Part1:', ebus * (earliest - arrive))



a = [67,'x',7,59,61]
a = [1789,37,47,1889]
a = busses
bus_counter = 0

mul = math.ceil(100000000000000 / a[0])
diff = 1
only_busses = [(val, offset) for offset, val in enumerate(a) if val != 'x']
print(only_busses)
# Start with our initial bus value
val = only_busses[0][0]
i = 1
for (bus_val, bus_diff) in only_busses:
    print('i',i, 'val', val, bus)
    while True:
        # look for value plus offset that equals mod our bus value
        if (val + bus_diff) % bus_val == 0:
            break
        # add on previous increment this increments by our previous cadance
        val += i
    i = i * bus_val
print('Part2:',val)
# while a[bus_counter + diff] == 'x':
#     diff += 1
# print('diff', diff)
# while True:
#     n = a[bus_counter + diff]
#     val = a[bus_counter] * mul
#     result = (val + diff) / n
#     if result == int(result):
#         #print(f'{result} = {val} + {diff} / {n} @ {bus_counter} {mul} {diff}')
#         found = True
#         inner_diff = diff - 1
#         for other in range(bus_counter+diff, len(a)):
#             inner_diff += 1
#             n_inner = a[bus_counter+inner_diff]
#             if n_inner == 'x':
#                 continue
#             result_inner = (val+inner_diff) / n_inner
#             if result_inner != int(result_inner):
#                 #print(f'    {result_inner} != ({val} + {inner_diff}) / {n_inner} @ {bus_counter} {mul} {inner_diff}')
#                 found = False
#                 break
#         if found:
#             print(f'Success Part2: {int(val)}')
#             break
#     mul += 1
#     if mul % 100000 == 0:
#         print(mul, val)

print(f'Took {time.time()*1000 - ms}ms')