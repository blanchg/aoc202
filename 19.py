import time
from collections import deque, defaultdict
from itertools import combinations, chain
ms = time.time() * 1000

def parse() -> dict:
    rules = {}
    for (key,rule) in rulesinput.items():
        if rule[0] == '"':
            rules[key] = rule[1]

    todo = deque([(0, rulesinput[0])])
    loop_detect = False
    while todo:
        print(len(todo))
        if len(todo) > 10:
            loop_detect = True
        (key, rule) = todo.popleft()
        if key in rules:
            continue
        
        resolved = []
        or_parts = rule.split('|')
        has_resolved = True
        for part in or_parts:
            # single part to resolve
            if part.strip().find(' ') == -1:
                a = int(part)
                if a not in rules:
                    t = (a, rulesinput[a])
                    if t not in todo:
                        todo.append(t)
                    has_resolved = False
                else:
                    ra = rules[a]
                    if isinstance(ra, list):
                        for i in ra:
                            resolved.append(i)
                    else:
                        resolved.append(ra)
                continue
            # multi part to resolve
            part_resolved = []
            join_parts = [int(a) for a in part.strip().split(' ')]
            for a in join_parts:
                if a not in rules:
                    t = (a, rulesinput[a])
                    print('Not Resolved part a', t)
                    if t not in todo:
                        todo.append(t)
                        # print('todo now', todo)
                    has_resolved = False
            # All the individual parts of this OR have been resolved
            if has_resolved:
                # print('Have join parts:', join_parts)
                for a in join_parts:
                    # print('    join part:', a)
                    ra = rules[a]
                    # print('       ', ra)
                    if isinstance(ra, list):

                        if len(part_resolved) == 0:
                            for ia in ra:
                                if isinstance(ia, list):
                                    if len(ia) > 1:
                                        print(a, ra, or_parts)
                                        print('appending list a', ia)
                                        exit(1)
                                    else:
                                        part_resolved.append(ia[0])
                                else:
                                    part_resolved.append(ia)
                        else:
                            next_resolved = []
                            for res in part_resolved:
                                for ia in ra:
                                    if isinstance(ia, list):
                                        if len(ia) > 1:
                                            print('ia is a list', len(ia))
                                            exit(1)
                                        else:
                                            ia = ia[0]
                                    elif isinstance(res, list):
                                        if len(res) > 1:
                                            print('res is a list', len(res))
                                            exit(1)
                                        else:
                                            res = res[0]
                                    # print('    adding', res, ia, '=', res + ia)
                                    next_resolved.append(res + ia)
                            part_resolved = next_resolved
                    else:
                        if len(part_resolved) == 0:
                            if isinstance(ra, list):
                                print('appending list b')
                                exit(1)
                            part_resolved.append(ra)
                        else:
                            for i, res in enumerate(part_resolved):
                                part_resolved[i] = res + ra
                    # print('   ', part_resolved)
                    # print('    ---')
                # for i in part_resolved:
                # print('or Part', part, 'resolving to', part_resolved)
                resolved.append(part_resolved)
        if has_resolved:
            alt = list(chain.from_iterable(resolved))
            # print('Resolved', key,':', alt)
            if len(alt) == 1:
                rules[key] = alt[0]
            else:
                rules[key] = alt
        else:
            print('Not Resolved', key,':', rule)
            todo.append((key, rule))
    return rules

def run1():
    rules = parse()
    zero = rules[0]
    print('Rules done', len(zero), zero)
    if not isinstance(zero, list):
        print('Failed because not a list')
    count = 0
    for m in messages:
        if m in zero:
            count += 1
    return count

def match(m: str, inputstr: str, rules: dict, rule, level = 0, char = 0, states = []) -> (bool, str, int):
    if char >= len(m):
        print(m, inputstr, rule, level, char)
        return (False, '', char)
    if isinstance(rule, str):
        if len(m) > char:
            print('-|' * level,m[0:char] + '_' + m[char] + '_' + m[char+1:])
        if inputstr == rule:
            print(' |' * level,'match', inputstr[0],'=', rule)
            return (True, '', char + len(rule))
        elif len(inputstr) > 0 and inputstr[0] == rule:
            print(' |' * level,'match', inputstr[0],'=', rule)
            return (True, inputstr[len(rule):], char + len(rule))
        else:
            print(' |' * level,'NOT match', inputstr[0] if len(inputstr) > 0 else '""','=', rule)
            return (False, inputstr, char)
    elif isinstance(rule, int):
        print(' |' * level,'int',rule)
        return match(m, inputstr, rules, rules[rule], level, char)
    elif isinstance(rule, list):
        if len(rule) == 1:
            return match(m, inputstr, rules, rule[0], level, char)
        msg = ' |' * level + ' OR ' + str(rule)
        print(msg)
        # OR
        for r in rule:
            (matched, output, used) = match(m, inputstr, rules, r, (level + 1) if len(rule) > 1 else level, char)
            if matched:
                # TODO can't just use first matched... what if others match?
                # if used == len(m):
                    # print(msg, 'True', output)
                    return (matched, output, used)
                # else:
                #     print(msg, 'short', output, used, len(m))
        print(msg, 'False')
        return (False, inputstr, char)
    elif isinstance(rule, tuple):
        if len(rule) == 1:
            return match(m, inputstr, rules, rule[0], level, char)
        msg = ' |' * level + ' AND ' + str(rule)
        print(msg)

        workingstr = inputstr[:]
        # AND
        for r in rule:
            (matched, output, used) = match(m, workingstr, rules, r, (level + 1) if len(rule) > 1 else level, char)
            if not matched:
                print(msg, 'False')
                return (False, inputstr, char)
            char = used
            workingstr = output
        # print(msg, 'True', inputstr)
        return (True, workingstr, char)
    else:
        print('unknown type', rule)
    return (False, inputstr, char)

def run2():
    # messages = ['b', 'bbbb', 'bab', 'aaa', 'aab']
    # messages = ['aaa']

    rulesinput = {
0: '8 11',
1: '"a"',
2: '1 24 | 14 4',
3: '5 14 | 16 1',
4: '1 1',
5: '1 14 | 15 1',
6: '14 14 | 1 14',
7: '14 5 | 1 21',
8: '42',
9: '14 27 | 1 26',
10: '23 14 | 28 1',
11: '42 31',
12: '24 14 | 19 1',
13: '14 3 | 1 12',
14: '"b"',
15: '1 | 14',
16: '15 1 | 14 14',
17: '14 2 | 1 7',
18: '15 15',
19: '14 1 | 14 14',
20: '14 14 | 1 15',
21: '14 1 | 1 14',
22: '14 14',
23: '25 1 | 22 14',
24: '14 1',
25: '1 1 | 1 14',
26: '14 22 | 1 20',
27: '1 6 | 14 18',
28: '16 1',
31: '14 17 | 1 13',
42: '9 14 | 10 1',
    }
    messages = [
# 'abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa',
# 'bbabbbbaabaabba',
'babbbbaabbbbbabbbbbbaabaaabaaa',
# 'aaabbbbbbaaaabaababaabababbabaaabbababababaaa',
# 'bbbbbbbaaaabbbbaaabbabaaa',
# 'bbbababbbbaaaaaaaabbababaaababaabab',
# 'ababaaaaaabaaab',
# 'ababaaaaabbbaba',
# 'baabbaaaabbaaaababbaababb',
# 'abbbbabbbbaaaababbbbbbaaaababb',
# 'aaaaabbaabaaaaababaa',
# 'aaaabbaaaabbaaa',
# 'aaaabbaabbaaaaaaabbbabbbaaabbaabaaa',
# 'babaaabbbaaabaababbaabababaaab',
# 'aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba',
    ]

    # rulesinput[8] = '42 | 42 8'
    # rulesinput[11] = '42 31 | 42 11 31'
    rulesinput[8] = '42 | 42 42 | 42 42 42 | 42 42 42 42 | 42 42 42 42 42 | 42 42 42 42 42 42 | 42 42 42 42 42 42 42 | 42 42 42 42 42 42 42 42 | 42 42 42 42 42 42 42 42 42'
    rulesinput[11] = '42 31 | 42 42 31 31 | 42 42 42 31 31 31 | 42 42 42 42 31 31 31 31 | 42 42 42 42 42 31 31 31 31 31 | 42 42 42 42 42 42 31 31 31 31 31 31 | 42 42 42 42 42 42 42 31 31 31 31 31 31 31'

    rules = {}
    for key, value in rulesinput.items():
        keyrules = []
        for s in value.split('|'):
            keyrules.append(tuple(r[1] if r[0] == '"' else int(r) for r in s.strip().split(' ')))
        rules[key] = keyrules

    # print(rules[0])
    # print(rules[8])
    # print(rules[114])

    count = 0
    matches = []
    notmatches = []
    for m in messages:
        # print(m)
        (matched, output, used) = match(m, m[:], rules, rules[0], 0, 0)
        if matched:
            count += 1
            # print(m, 'matched', output, used)
            matches.append(m)
        else:
            # print(m, 'not matched', output, used)
            notmatches.append(m)
        # print('----------------------------')

    print(matches)
    print('----------------------------')
    print(notmatches)
    return count


rulesinput = {
0: '8 11',
1: '52 114 | 130 29',
2: '107 29 | 26 114',
3: '29 68 | 114 20',
4: '79 29 | 68 114',
5: '81 29 | 2 114',
6: '132 114 | 79 29',
7: '56 114 | 129 29',
8: '42',
9: '29 125 | 114 63',
10: '29 67 | 114 65',
11: '42 31',
12: '121 29 | 128 114',
13: '114 77 | 29 105',
14: '21 21',
15: '41 114 | 90 29',
16: '29 12 | 114 103',
17: '29 70 | 114 70',
18: '29 122 | 114 110',
19: '21 111',
20: '21 114 | 29 29',
21: '29 | 114',
22: '3 114 | 113 29',
23: '21 40',
24: '20 114 | 50 29',
25: '114 55 | 29 46',
26: '114 50 | 29 64',
27: '111 114 | 132 29',
28: '53 29 | 119 114',
29: '"a"',
30: '20 114 | 40 29',
31: '29 92 | 114 38',
32: '79 114 | 64 29',
33: '116 29 | 84 114',
34: '29 79 | 114 48',
35: '104 29 | 104 114',
36: '114 68 | 29 132',
37: '64 114 | 104 29',
38: '114 9 | 29 57',
39: '114 127 | 29 35',
40: '114 29 | 29 114',
41: '67 114 | 104 29',
42: '73 29 | 93 114',
43: '97 114 | 25 29',
44: '1 114 | 61 29',
45: '64 114 | 48 29',
46: '89 29 | 94 114',
47: '29 86 | 114 60',
48: '29 21 | 114 29',
49: '100 114 | 37 29',
50: '29 29 | 114 29',
51: '19 29 | 129 114',
52: '75 29 | 85 114',
53: '48 29 | 132 114',
54: '65 114 | 79 29',
55: '131 29 | 32 114',
56: '29 132 | 114 40',
57: '117 114 | 82 29',
58: '74 29 | 4 114',
59: '79 29 | 48 114',
60: '114 104',
61: '114 47 | 29 126',
62: '29 33 | 114 72',
63: '29 69 | 114 99',
64: '114 114 | 114 29',
65: '29 114 | 29 29',
66: '114 80 | 29 71',
67: '114 114 | 29 29',
68: '29 114',
69: '114 3 | 29 59',
70: '114 29',
71: '129 114 | 131 29',
72: '29 22 | 114 28',
73: '95 29 | 91 114',
74: '65 114',
75: '50 114 | 20 29',
76: '70 29',
77: '14 114 | 20 29',
78: '29 64 | 114 79',
79: '29 29',
80: '98 29 | 102 114',
81: '29 10 | 114 89',
82: '87 114 | 101 29',
83: '29 132 | 114 111',
84: '24 29 | 17 114',
85: '70 29 | 40 114',
86: '111 29 | 65 114',
87: '36 114 | 32 29',
88: '133 114 | 27 29',
89: '14 21',
90: '114 50 | 29 20',
91: '29 5 | 114 66',
92: '29 43 | 114 62',
93: '29 16 | 114 44',
94: '114 67 | 29 64',
95: '114 96 | 29 123',
96: '18 114 | 13 29',
97: '114 51 | 29 124',
98: '40 29 | 50 114',
99: '83 29 | 53 114',
100: '20 114 | 111 29',
101: '45 29 | 78 114',
102: '70 29 | 50 114',
103: '29 109 | 114 15',
104: '114 114',
105: '114 70 | 29 132',
106: '29 64 | 114 132',
107: '50 29 | 65 114',
108: '29 48 | 114 111',
109: '29 120 | 114 30',
110: '114 50 | 29 65',
111: '114 21 | 29 114',
112: '48 114 | 64 29',
113: '68 114 | 68 29',
114: '"b"',
115: '29 50',
116: '29 17 | 114 6',
117: '7 114 | 49 29',
118: '114 106 | 29 76',
119: '29 111 | 114 70',
120: '114 67 | 29 132',
121: '32 29 | 54 114',
122: '114 111 | 29 65',
123: '118 114 | 39 29',
124: '23 114 | 34 29',
125: '29 58 | 114 88',
126: '29 134 | 114 4',
127: '50 29 | 48 114',
128: '115 29 | 112 114',
129: '14 29 | 104 114',
130: '29 36 | 114 108',
131: '111 114 | 65 29',
132: '114 114 | 29 114 ',
133: '132 29 | 70 114',
134: '114 50 | 29 48',
}

messages = [
'aaababbaaabababaaabaaabb',
'bbabbababbbabaababbbbbbabababaaa',
'baaaaaabaababbbbbaaaaaababbbbbaababbaaaaaaaaaaaa',
'bababbbbaabaabbaaabababbaabbabab',
'ababbaaabaabbabbbbaaabba',
'aaaabaaaababbbababbaababaabbabbababaaabbaabbbbabaabbabababbbabbbaababbaaabaaabbb',
'ababaababbaabbbaabbaabba',
'abaabbbabbaabbaaaabababaabbbaabaabbbbbaababbaabb',
'abbaaaabbbaabababbabbaabaaababaa',
'aababababaabaaabaabaabba',
'bbaabbbaabbabbaaaaaabbba',
'bbaabbaaabbabbaaaabaaaabababbaababbabbbaabbbaabb',
'abbabbbaabbbbabaabbabbbaaaabaaab',
'aaaabaabaababbbaaaababbb',
'baaaabaabbbbaaaabbaaabba',
'aabbaaaaabbbaababaaabbaaaaababaa',
'abbaababbaaabaaabbaaaaba',
'bbbbbbabaaaaaababbaabababbbaaaabbaaabbba',
'baaaabaaabababbbbaabbbaa',
'ababbbaabaaabaaabaabbaaabaabbbbaaaababab',
'babbbabaabaaaaaaaabbbaba',
'ababaabaabaaaaaabbaaaaab',
'aaaaabbabaaababbaaababbb',
'bbaaaaaaaababbbaaaaabbabbbaaabababaabbbaaaaabbaa',
'baaaabbababaabbbabaabaabaabbabbbaaabbaabbababaab',
'bbaabbabababaababbbbaabbaaababab',
'baaaabbbbaaababbabbbbaaa',
'ababbabababababaaaabaaba',
'abbabababbabaaabbbbbabab',
'ababbbbbaababbbbbbaabbbabbabbaba',
'abaaabbbbbabbaaabaabbbab',
'abbabbaabbbbbbabaababaaa',
'aaaaabaabaababbbaaaaabbaaababbaaaaabbbbbababbbbababbaababaabaaaaabbbbaabbbbbaabbbaabaaba',
'baabbababaabaaabbaaababa',
'bbabaabaabbaaaabbbaabbabbababbababbbbbbbaabaaabb',
'baabbabbaaabbbbbbbabbbba',
'bbaabbaaabaabaaabababbba',
'ababbaaabaabaaabbaabbaaababbaaab',
'baababbabaaaabaababbabaabbbbbbabbbbaabbbbabaaaaabbbabbbbabbaabba',
'abaabbbbababaabbababababaabbabab',
'bbbabbaaaabbbaabaaabaaaa',
'bbabaabbbbbbbbabbabbbaaa',
'abbaaaaaabaaababaabbaaba',
'bbaaabaabbabbbaaaaabbaaababbaaba',
'baabbaabbbaabaabaabaabba',
'aaaabbabaabbbaaabaaabbba',
'bbaaabaabbbaabaabbbbabab',
'babbbbaabbabbaaaabababba',
'bbbaabaabbbaabaabbaaababaaaabbbbaaaabaaabbbaabababbaaabb',
'baaaaabababababbaaaaaababbabbbbbbabbbbbbbabbaaaababbbbabaabaaaaabbababab',
'baabbaababbbbbbbbaaababbabaabbbabaaaaaaaaaaabbaabbabbbab',
'baaabaabbbaaaabbbabbabab',
'aaabaabbbbbabbbaaaaabbaa',
'bbbbbbabbbbababbabaaabbbaaaabbbbbaabbbbb',
'abababbbbaababbbbaaababbaabaabaabbbbabaabbaaaababbababbaabbabaab',
'babaabbabbbababbaababbbababbbbab',
'abaaaababaaababbbbabbabb',
'abaaabbbaabbbbbaabbbaaabbbaaaaabaaabaaaa',
'baaabaaaabbabbabbabbaaba',
'abaaaaaaaabbaaaabaabaabb',
'bbabaaabbaaaabbaabababba',
'aababbbaabaabaaabbbbbbba',
'abbabbabaabbabbabbababba',
'bbbbaabbaababaabaaaabaaabbaaabaa',
'baabbabbbbabaabaaabbabaa',
'aaabbabaabaaabbabbbaabbbbbaababbaaababbb',
'abbaababbaabbabaaabaabab',
'bbbaabbbbabbbbbabaaaaaabaabbaaababbaabba',
'abbabbabaababbbbababbabaabbabababbbbbaabbbbaabab',
'bbabbbbbaaabbababbababab',
'abbabbabaabaaabababaaaba',
'aabbabbaaabaabaaaaababbb',
'aaabbabaabaabaaaabbbbbaabbabaababbaabaabbbaaabbb',
'bbabaabaaaabbababaaaaaabbaaababbbabaabbbbbabbbbbbbbbabbbbbbbabbbbbbabbab',
'bbaaaaaababbbbaaaaaaaaab',
'bbaaabaabaaaabbababbbaab',
'ababbababababbaabbaaababaabbbbababbbaabb',
'ababbaaaabaabaaaaaaaaaab',
'baaaabbbbabbabaabaaabaaabaaaaabb',
'baaaaaabaaabbabaababbbab',
'abbabbaabbaaaaaabbaababbbbbaabbbaaaaaaab',
'baabaabaaababbbabbaababbababbbbbaabaaaaaabaabbabbaaabaabbaaabbbbbbbaaabaabbababa',
'abbbbaabbbbbbaaababbbbbaabababbbbbbbbaab',
'bbbababbbaaaaabaabbabaaababaabbabbaaaaabbabbabab',
'aaabbbbbaaabbbbbbabbaaba',
'bbaabbaaabaaabbbababbbba',
'baabbaaabbabaabbbbabbbbbbbababaaaaaaabbbabaaabaabaaabbabbbbabaaababaabaababbbbaa',
'bbaababbbbaaabbbbababbaabbbaaababbaabbaa',
'babbbbaabaabbaabbabbaabb',
'bbbbbbabaaababbabbbabaab',
'babbbbbaaaababbabbabbaba',
'bbaabbabaaabaabbbabababbbbaabbaababaaaabaaaaaabaaabaaaaabbabbbbabbababaaabbbabbb',
'baaaaabaabbaaaaababbbbab',
'babababaabaababababaabbbabbaabbbaabbaababaababaaabaaabab',
'bbbbbaaaababbbbbbabbabab',
'baabaaabaaabbbabababbbab',
'bbaaaabaaaaabbbababbbaabaaaaabba',
'ababababbbaabbbbbabaaaba',
'bbbabbbabbabaaabbbbabbaa',
'bababbaaabbbbabaabbaabbbbaabbabbbbaababaabbbaaabbbabbabb',
'aabababaabbabbabaababaab',
'babbbababbbaaabaabbaabba',
'bbabaababbaaaaaabbbbbbbb',
'baababbaabaabaabbbbbabab',
'baaabbaabbaabaababbaabbbbaaaabababbbbabbbbbbabba',
'abbabbaaabbbbabaabbbbaabababbbbbaaabbbababbaabaabbbbbaba',
'abbaaaaaababaabbaababababbbaabaabaaaabbabbbbabbababaaababbbbbabaabbaabba',
'aabbabbbabababaabaaabbbb',
'bbbabbbababbbbaabbbbbabb',
'abababaababaabbbbaabaabb',
'aaababbababbabaabbaabaaaabababbbaaababbaababaabaaaabbbbabbabaaaa',
'baabbababbbabbbabbbabaab',
'aaaaaabbbaabbaaaaabbbbbaaababbbabaaaaaaa',
'bbaababbabaaaabbaaabbaaa',
'bbaabbbbbaabaababaabaabbababbbba',
'abbabbaabbaaaabbaaababbabbabaabaaabbbbbabaabaaaa',
'baaaabaabaaabbaaaabaabba',
'aaaabbbbaababbbabbabaaaabbbabaab',
'aaabbbbbbbbbbaaaabbabbbabaaabbbb',
'babbbbaabaabaaaabbabbababababbaaababbabbbbbabaaabaaaabaaaaabaaaabbabaaaa',
'bbabaaaaababbaababbbbbab',
'babababaaaabbbabaaaaabbb',
'abbbbabbababbaabaaaabbabaabaabababbbabba',
'bbabbbbbbaaabaaaababbaabbaababab',
'baaaababbbaaababbaaabbbb',
'bbabbaabaaabbabababbbaaa',
'abbabbaaaabbabbaababbbba',
'bbbabbbaabbaaaabbabbbbab',
'bbaabbbabaaaabbaabbaabbbaabaaaababbaababbbbaabababbbabbabbbbbaba',
'aabbabbabbabbababababbbbabbaabba',
'aabbbaaabbabbaaaabbbbbab',
'baaaabaaabaaaabababaaabb',
'bbaabbbaabbaaabababaaaaa',
'baaaabaabbabbaaababbbaaa',
'bbaabbaabaabbabaaababbab',
'babaabbaabbaaaaaaaaaaaaa',
'bbaaabaabbabbaaaaabbaabb',
'aaabaaababbbabbbaaaababababbaababaabbbba',
'abbaaaabbbaabbbaaabbabaa',
'ababaaabaaaababababbbaaaaaaabbaa',
'babaabbaaaaaabbaaaaaaabbbbaabbaabaabbabbbbbaabab',
'aababbbbaaaabbababaaabbbbaabbaaabbbbbaaaaabbbaabbabaabaa',
'abaabbbbbaabbaaaaababbbaabaaaaaaababaaaa',
'babbabaabbaababbabbaaaabbaaabbbb',
'baaaabaaabaabbbaaaaabbabbbabbaababbbaaaa',
'abbbbababaabbaababaaaaab',
'babaaaaababbbabbabaabbab',
'bbaaaabbaabbaaabbbaaaaba',
'aabbaaaabaabbaaabaabbaabbaababab',
'bbaabbaabaabbabbaaabbbabbbbbabbababaabab',
'bbabaabaaaabbabaabaaaaab',
'bbabababbabaabbabbbabaaaabbbaaaaabaaabaabbababba',
'abbbbabaabaaabbbbabaaaba',
'ababbaaaaabbabbabbbbaaab',
'aaabbbabbbaabaabababaabaabbaaaaaaaaaaabbaaabbbbbbbababba',
'aaabbaaaabbbaababababababababbbbbabbbbabbbaabbbbaabbaaab',
'bbaabaaaababbbaabbbabbaa',
'abbaabaababbbababaabababababbbaa',
'babaabbbaaabbbabaaabbbbbaababbbabaabbbbaabaababb',
'abbabbbaaaaaabbababbbbaabbabaaabbababbaaaaabbabbababbbba',
'aaababbaababaababaaabbab',
'ababaabbbbbbbabbaabbbbab',
'aababbbbbbbbbaaaaaabaaba',
'abaaaaaabbbbaaaababaaabb',
'abbbaabaaabbaaabaaababbbbabaababbbaaaaab',
'bbbbabaabaabbaababbbabbb',
'bababbaaabbaababbabaaaaa',
'ababbababaaabbaababbabbabbaabaabbbbbabaaabababaaaaaabababbbbaaba',
'baabbabbbbabbaabbbbabbaa',
'abababaabbaaababaabaabaaabaabababbabbbba',
'abaaaaaaaaaabbabbababaaa',
'aaabaabbaaaaaabbbbbbabba',
'baaabaaabaababbbaaabbaaa',
'bbbbbabbbaabbabaaabbabaa',
'bbababbbbaabaaabaaabaaba',
'aabbaaabaaaabbabbbabaaabbaaabbba',
'babaabbaaabbaaabbabbbaba',
'abbabbabbaaaabbabbbbbaba',
'aaabaabaabbbababbbababab',
'ababbaabababbaabbbabbabb',
'aabaabaaababaababbaabaababaaabbaababbbbbbbbbbaab',
'bbabaababbaaaaaaaaabbabababaaaaababbbaaa',
'baabaaabaabaabaabaababbaaaaababb',
'abaaaaaaaaabbbabaaaaaaab',
'aaaabaabbbbbaabbabbbaababaaaaaabaababbbaaabbbaabaaaabbba',
'bbabaababbaaababbababbbb',
'abaaabbbbaaabaaababaaaaa',
'abbbaaabbbbabaaabaaaaababaaaaaababbbabbbbabbbbab',
'bbbabaaaabbbbbbbababbabababbaaba',
'babbbbbababbbbbbaabbbabb',
'bbaabaabbbabaababaabbbba',
'bbabbaabbabaaaababbababb',
'babababaabbaaababaaabbbb',
'ababbbaababbaaaaababbabb',
'aaaabbababbaaababaababab',
'baabaababbbabaaabaabbbaaabbababbbbbbabba',
'bbbaabbbbbababbbaaaaabbaaaaababa',
'abbbbaabbbaaaaaababaaaaa',
'bbaaababaabbbaaaaaaabaaa',
'bbababbbaababbbbbabbbabb',
'bbabbaaabaaaaababbaaabaaaabbaaaaaaababaa',
'bbabbaaaabbabbbaabaaaabbaabbabaa',
'baabbabbaababbbbbabbbaab',
'ababbaabaabaaaababbababb',
'babaabbbbbbaabbbbbbbaabbbbabbbaabaabbbaaabbbbbbaabbbbbab',
'abbaaaabbaaaaabaaaaabbababbabbaaababaabbbbbbbbabaaabbbaa',
'aabbbbbaababbababbaaaaba',
'abbababaaabababaabbaaabb',
'bbbaaababbaabbaabbaabbabaaababbbbaabbbbbabbbbaaaaabaaaaa',
'abbabbaaaabbabbabaaabbbb',
'abaabbbbbaabaaababbaaabb',
'aabaabaaabababbbbaabaabb',
'aaababbababaabbaabbabbaaababbbbbabbbbaaa',
'babaabbbaabbbaaaabbabaab',
'baaabbaabaaaabbaabbbabaa',
'bbabbbbbbabaabbbbbbaabbababababbbaaabaabbababbbabaabbbbbbbababaa',
'baabbaaababaaaabbbaaabba',
'bbabbaaaaababbbabaababaa',
'bbbbbbabababbabaaabaabbbbaaaabbaababbaaaaaaababbbaaababa',
'abbbbaabaaaababbaaaabbbaabbbbbab',
'abbabbabaaaaabbaababaabaaaaaaabaabaabbabbaaababa',
'bbbababbabaabaaaababbbaaababbabaabbbabbaabbbaaaa',
'bbbaabaaabaaaabbbabaabaa',
'aaababbaabbbbabaabbaabba',
'baaababbabaaabbbabbabaaabaabaaaaabbbbbba',
'ababbaababbaaaaabbbbabab',
'bbababbbabbbaaabaabbabbbaabaabab',
'ababababbbaabbbabbaaaaba',
'babbabbaaaababbaaabbaaba',
'abaaaabaabbaaaaaaabbbabb',
'babbaaaababbabbabababbbb',
'bbabbbbbbbababbbabbbaabb',
'baabbabaaabbbbabbbaaaabaabaaaaabbbabbbbbaabaaaabbaaaabbaabbaaaaabbbbbabb',
'abaaabbbabaaaabbbbabbbaa',
'bbbabbbabbaababaabbbabab',
'abaabaabaabbbaabababbbab',
'babbaaaabbbbaabbbabbbababbbabbabbaaaaabb',
'baabbaaaaabbabbbbbbbabaaaaababbaaababaaa',
'abbbbabbbaaaabaabbbbbbaa',
'bbbbaaaaaaaaababaabaaaaa',
'baaababbabbbaabaababbbba',
'bbaabbbaabaabaabbbbaaaab',
'abaabbbababaabbbabbbabba',
'baaabbaaabbbbabbbbabbbba',
'aabaaababaaabaaaaaaababb',
'baaabaababaabbbbabbaabbbbababbabbbaaabaabbbbabbb',
'aaaabaabbaabbaabbbaaabbb',
'aaabbbababbbbabaaabbbbbb',
'bababbaabbaabaabbbbbabaabbabbbbbaaabbaabbabaaaaa',
'bbbabaaababaabbabbababba',
'baabbaabaabbaaaabbbaaaab',
'abbaaaabbbbbaabbbaaaabaabababaaa',
'baaaaabababababbaabaaabb',
'abbbabaabbbbabbbbabababbaabaabbabbaaabbbbaabaababaabbabb',
'aabbaaabbbbababaabaaaabbabbaabbbaaaaababbaabbbba',
'baabbaabaaaaaabbbabbabbababbaaaaabbbabbb',
'bbbababbabaabaabaabaaaabbbbaabaababbbabaaaaabbbabbbabaabbbbaaaab',
'abaabaabbaabbababbbbbaba',
'aaabbbbbbbbbbabbababaabaabbbabba',
'bababbaabbbbbabbbbaababbbabbbabaabaabababbabaaabbbabbaba',
'abaabaaabbbbaaaababbbababbbbaaab',
'bbaabbabbaabbaabbabaaabb',
'abaaaababbbaabaaabaaaabbbabbbbabbbbbbaab',
'aabbaaabbbaabbbbaabbabab',
'baaababbbbaababbbaaaaaaa',
'ababbaaabbabaaabaaaababa',
'bbabaabbaaabbbbbabbbbbbbabaabaaaaabaaaaa',
'baabbababaaaababaabaaabaaababbbababbbbbabbabbbab',
'abaaabbaabbaaaaabbbababbaababbab',
'baaaaaabbbbaaaaabbbbbbaaabbabbba',
'ababbaaabbaabbabaabbabaa',
'aabaaababbbaaabaabaabaaaabbaababaababbabaabbabaa',
'abaaaababbabaaaaaababbbbbbababaa',
'babaabbabbbbabaababbabab',
'abaaaaaaabbbbbaababababbbaaabaabbbbbaaaaaaababaaabaaaaab',
'aaaabbabbaabbaabaaabbbbbbabbababababbbba',
'bbbbabaabbaababbbbbbbaba',
'abbabaaabaaababbbbbbabab',
'baabbabbabaaaabbbbbbbaab',
'bbaabaaaaabbabbabababbbb',
'bbabaaaaaaaabaabbbbbbbaa',
'abbbbabbbbaaaaaabababbba',
'bbbbbbabaaaabaabbbbbaaaaaaabbaab',
'babbabbaabbbabbababaabababbbbbbaabaababaaaabbbaaabbbaaba',
'abbbbbaabaaababbaaababbb',
'bbbaababaabbabbababaabaaaaaabaabababbbbaabbbbbababababbbbbbaaababaabaabb',
'baabaaabbababbababbbbbbabbbbaaabababbbab',
'abbabababababbababababba',
'abbabaaaaaabbbbbaababbbbaabaaaababaaaababbabbbba',
'abaaaaaaaaababbababaabaabbbaabbbaaababbbbbbaaaaabaaabbaa',
'bbbbbaaabaababbbbabbbbab',
'bbaaababbabaabbbbabababbabaabaaababbbbbababbaabb',
'aaaabaabbababbaabbabbbaa',
'aaaabbbbabbbaaababbabaaaabbbbabaabbbbabbababbbabbabbbaabaabbababbabaabaa',
'babbabbaaabaaaababbababb',
'aaabaabbabbbbabbbbbaabab',
'ababbbaaabbabaaabababaab',
'abbbbababaaaaabaaaababbb',
'ababbbbbbbabaabbaaabaaaa',
'abaabbbaabbbaabaaabaaaaa',
'bababbaaaaabaabbabaabbab',
'bbabbaaaabaababaaaaababa',
'babaabbaabababbbaabbbaab',
'babbbabaaabbabbbbbaaabbb',
'baaababbbaabaababbabbaaaabaaaaaabaabbbbaabbababb',
'babbbbbbbbabbababbbbaaaabaabaaaaabababaabbbbbbbaaaaaaaaa',
'baaabbaabaabbabababbaaab',
'bbbababbabaabbbbbabbbbab',
'aabbaaababbaaaabbabbaabb',
'bbaaaaaabbbaabaaabbbbabbbbbababbaaabbbbbbbbabaaaabbbabab',
'abbababababababaabaaaaaaaaababab',
'baabbabaaaaaababbabaaaaa',
'aabababaabaabaaaabbbbbba',
'abaaabbaabbabababababbbb',
'abbabbaaabaaaaaabbbababbaababababbbaabaabababbbabbababbaaabbbaba',
'babbbbaaabaaaaaabababbabaaaabbbaabaabbbaaabaabbb',
'baaaaaabbaaabbaaaaabbbbbbbbbbaab',
'abaabbbaaabababaabbbbbbbabbaababbbabbaabaabbabbbbbababaabbbaabab',
'bbaaaabbaaabaabbbbabaaaaabaaabbbbbabaaaaaabbbbaa',
'abaabaabbababababbbbabba',
'babababbbbaabbaababbbbbbbabaabbababbbbbbbaaaaababababbba',
'ababbbbabbabbbaaabbaaaaaabbbabaabbbbbabb',
'baabaaababaaaaaaaabababb',
'aabbbaaaababbbaabbabbaaabbbaaaaaababbbab',
'abbabbbabbaabaaaaaaabaaa',
'aaaaaabaaaabbbabaabbbaab',
'aaaaababbaaabaaabaababbabaaaabbbbaaababababaababaabbaabb',
'babbbababaaaabbbababbbaaabbbaaabaabbaaaaaaaabbabaaabbaab',
'bababbabaabbabbaaabaabab',
'babbbababbabaabababbabab',
'bbabbaabaabaabaaabbabbbb',
'abbbaaabbbaabaababbabbbaabaabbaa',
'aaaaaabbbbbabaabbabbbbabbbbbbbbbabbabbbbbabbabab',
'aababbbaabaabaabbbbbaabbaabaabbbbbbabbbaababaaaa',
'baaabaaababbbbbbaabaabbbaabbabbbabbaaaaabbaaabbaaabbaaba',
'baabbababaababbbabababaabaaabbbaaabbbbaa',
'bbabaabbbaaaaaabbbbabbbabbabbbbbabaaaabbbaabbbbaabbabaab',
'baaaaaababaaaaaaaaaababa',
'aabaaabababbbbbaaaaaaaaa',
'abababaaabaaabbaaaaabaaa',
'baabbaababbaaaababaaaabaabababbaabaababbaabaaabb',
'babbbababbabaaabaabbbbbabbabaaaabaaabbbb',
'abaabababbbabbbaaabbbbab',
'ababaababbababbbabbaaaaaaababbbaaaaabbaaabaababb',
'aaabbbabbbaabaabbbbaaaab',
'baaabbaaabaaaabaaabbbbab',
'bbbaabaabbabaaabaababbbbbabbaaaabbaaabbb',
'bbabaaababaabaaaabbbaaabababaabbabbbabbbabbaabba',
'ababaabbabbaaaaaabbbbbaabbabaabbbbbaabaabbbabaabaaaababb',
'babbbabaabbaaababbaaabba',
'baaaabbaaabbabbbbabbbbabbbabbaba',
'bbbbbaaaaaaaababbaaaabbaabaaabab',
'bbaabbaaabbbbabbbbbbaaab',
'ababaabaabaaabbbabbbabab',
'bbaabbaabaababbababbbaaa',
'bababbaaaabbaaabbaaaababaaaaababbbabbabbbababbbb',
'baaababbbaaaabbaaaabaaba',
'bbbabbbabbaaaabbbbbaabbaabbbaaabbabbabbb',
'bbaabbbbbbaaabaaaabbaaaababbabab',
'abaabbbaabaaaaaaaaaabaaa',
'aababbbbaababababbbabaab',
'aabbaaabaaabbbababbabbabbabbaaaaaaabbbaa',
'baabbabbabaaabbaabaabbaa',
'bbaababaaabbbbbaabbabbababaabbbbababbabbabbbbaaa',
'babababaaaaaababaabbbaba',
'bbababbbbbbbbabbabaabbbbbbababbabbbabbbb',
'aabababbaabaaababbaabbbbbbaaaaaaabbbbaaaababbabbaaaaaaaaabbabababbbbbbbbaaaaaaaaaaaaaaba',
'abbbbbbaaaabbbbababaaaba',
'baabaaabbaaaaaababbbbbba',
'bbaabbaaabbbbbaababababbbaabbbba',
'babbbbaababaaabbaaababaabbbabbaabaaabbabbabaaaaabbabbbba',
'babaaaabbabaaaabbaaaabbaaabbbbab',
'ababbababaaaabbaaabababb',
'bbbbbbababababaabaabbbba',
'bbaababbabbaaababababbba',
'aaababbabbaaabaaaabbabbaaaaabaaabababaaa',
'abaabaaaabaabababbbbaaba',
'ababababaaababbababaaaaa',
'bbabaaabaababaaabbabaaabbababbab',
'baaabbaaaabaaabaaaabaabbbaaaaabaaaaaabaababaababbaaababaabaabbaa',
'babbbbbaaabbabbbbaaaabbaaaabbbbbaaabaaba',
'aababbbaaaabbbaaababbaaabbaaaababbabaabbbaaababababaaaabaabbaaaa',
'bbbaabbbbbaaaabbbbaaabaaaabbabbabababaaa',
'abbaababababbaaabaaaabababbbaababbbaabbbabbabaab',
'aabbbaaaaabbaaabbbbbaaab',
'baaaababaabbabbbaaababab',
'abaabbbababbbbbbbbaaabba',
'babbbbaababababbaaababbb',
'baaababbaabbbababbaaabbbbbaaaaabbaaaaabbabbaaaaa',
'bababbaabbaababaaabbaabbabbaaabbbabbaaabbabbbabbaaabbaaa',
'bbaabbabbabbabaabbaabababaabbabbaabbaaaaaababaaabababbbb',
'baabbaabbbaabbaabbbbbaab',
'babaaaabbbbbabaabbaaabba',
'bbbabababbbaaabaaaaaababaaabbabb',
'bbababbbaabaaaababbbbaabbaaaaababbababbaaabaaabbaabbbbbb',
'aaaaabbaabaaabbbbabbaabb',
'abbbbaabaababbbbabaabaabbbbbbbbb',
'abaaaabaaaabbbabaaabbbbbbbbbaabababbaabb',
'bbbbaabbaabaaaababbabbababbabbabaababaaa',
'abbbaaababbaaabaabbbabba',
'bbaabbaaabababaaabbbabba',
'aabababaabbbbbaaaaaaaababbbbbaabaababbab',
'bbabbaababbaababaabbbbab',
'bbabaaaaaaaaabbababbbbbbbbaaaabbaabaabbbbbbbbabaabbbabbbbababaab',
'aaaaaabbaaababbaaaabbaab',
'bbaababbabaaaababaabaaabaaaaabaa',
'aaababbabbbabaaaabbbaabb',
'babbbbbbbbabbbbbaaaabaabbabaaaaabbbbabbb',
'baaabaabaaabbbabababbbab',
'aabaaabaaabaabaaabbbaaaa',
'abaabbbabbabaababbbbbaaaababbbabaabbaabbbbbabaab',
'aabbabbbababbabaabbbabbb',
'bbbaaabaabababbbbbbbabab',
'bbbbaabbbbbbaaaaaaaabbabbbabbbbabbbaaaab',
'abaabaababaaabbabbabbaba',
'bbbabbbaaaaabaabaaaabbbbaababaabababaaab',
'aaabaaabaabaaaabbbaaaaabbabbabaabbabababbaabbbabbaaaabbbbabbbbaaabaabbaababbbabbaaaabbbb',
'bbbababaabbbbabaababaaab',
'babaabbbabaabbbaabaaaabbabbbbbba',
'bbaaaabbaabaaaababababba',
'abbaaaaababaabaababbbaaabaabbbabaababaaa',
'aabbabbbabbaaababaaaaaabaabaababaabbbabb',
'bbaabbaabbabaaabababbabb',
'baabbaaaaabbabbbaabbaaba',
'aaaabbbabbaabbbbbaaaaabaabaaaabbaabababaabbbbaaaabbaabbababbaabaaabaaaab',
'bbbabbbbaababbabbbbbbbaabbaaaabaaaabbbababbbaabbbaabaabaabaaaababbbbbabbaabbabbb',
'aaabbababbaaaabbbaaaabbabbaabaabbaababab',
'bbaabbbaababaabbbabbaaba',
'abbbaababbabbaababbbbbaaabababbbbbbaaaaabbbbbbbbbbbbaaba',
'ababababbaaaaaabbbbbaaba',
'bbbbbaaabaaaaaabaaababbaaabaaaaa',
'aaaabbababaababaaaabbbabababbaabbbaababbabbbbbbaaaaaaaabbbbabbbbbbbbabab',
'aabaabbbbabbbabaaabaabab',
'aabaabbbababaabbbbaabaabbabbabaaabbbaaaabaabaabb',
'baaaabbabbbabbbabababaaa',
'baabaaabbaaaaababbbabababbaaabbb',
'babababababbaaaabaaabaabbbbbbbbb',
'abbbbaabbaaaababbaaaabbbaababababbbbbbbabababaabaabaabba',
'bbbabaaaaabbbbbaabbaabba',
'abababbbbaaababbaaabbabb',
'abaabaabbabaaaabababbbaaaaababaabbbaaabb',
'aaaababbbaabbaabaaabbaabbbbabbbbaaabbaaabbbaaaab',
'aaababbabbbabbbababababaabbaabaa',
'bbaaaabbaaaaaabaaabababb',
'abbbbaaabbbbbabbbaabaabbaaababaaabaabaaabbaabaaaabbbbbbbbbbbbbabababaaab',
'bbbbaabbaabaabbbaabaaaababaaabaaaaabaaba',
'abbabaaabaaaababbbbbbbababbbbbbbabbbaaaa',
'bbaabbbbababaabbaaababab',
'aabaabaaaaaabaabbbababaa',
'aabaaabaabbbaaabbbbababaababbaab',
'babbbbbaabababaaababaabbaabbbaab',
'bbabbababbaabbbbbbaaabaaaaababbaabbbbbbbaabbbbab',
'bbaababababbbbbabbabbaaababbbabb',
'aabababaaababbbabaaaaabb',
'babbaababaabaaabababbaababababaababbbbbb',
'bbbaabbbbbbaabbaabbbaabb',
'bbabbaaabbaababbaabbabbbbaabaabbaabbbaba',
'abbbbbbbabababaabaaabbab',
'abaaabababbbbbbaabaaabbabaaaaababbbbaaabaaaabaaabbaaabab',
'abbaabbbabbbbabaaabaaabb',
'bbababbbabbabbbabbbabbbbabbabbabbabaaabaaabaabbbbbbaaaaa',
'baaaabaaabaaabbaabbbabbb',
'aababbaaabbbabaaabaaaaabbbbbabbb',
'aaabbbbbaabbabbaaabbaaaaaaabbababbaabaabbbbaababaabbbabbbbabababbabbbabb',
'bbbbbababbabaababbaababaabaababaaaababbbaaabbbaabaabaababbababab',
'aaababaaaabaaabbaaabaaba',
'baababbbaaaabbbbbbbbabab',
'abababbbbbabaaaaaabbbaaaabbabaaaababbbab',
'ababababbbbbbaaabbaabbbaaabbbbbaababbbbbaaaabaaabaaabbbbbbaaaaabbabaaaaa',
'aaaaaaaaabaaabaaabbabaabbaabbaaaabbbabbabbababbbbbababaabbbbabab',
'baaabaaaabaaaabbbbaaaaab',
'babbabbaaaabbabaabbbaaaa',
'abbbaababbbababaaababbbbbabababbbbaabbabbbbbbbaabbbbbaba',
]

# part1 = run1()
# print(f'Part1: {part1}')

part2 = run2()
print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')