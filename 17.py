import time, numpy as np
from collections import deque, defaultdict

from numpy.core.fromnumeric import ndim, shape
ms = time.time() * 1000

# initial = np.array((1, 8, 8))
# initial.fill('.')
#np.pad(initial, 1, 'constant', '.')
initial = np.array([
[1 if x == '#' else 0 for x in list('#...#...')],
[1 if x == '#' else 0 for x in list('#..#...#')],
[1 if x == '#' else 0 for x in list('..###..#')],
[1 if x == '#' else 0 for x in list('.#..##..')],
[1 if x == '#' else 0 for x in list('####...#')],
[1 if x == '#' else 0 for x in list('######..')],
[1 if x == '#' else 0 for x in list('...#..#.')],
[1 if x == '#' else 0 for x in list('##.#.#.#')],
], dtype=int)

# initial = np.array([
# [1 if x == '#' else 0 for x in list('.#.')],
# [1 if x == '#' else 0 for x in list('..#')],
# [1 if x == '#' else 0 for x in list('###')],
# ], dtype=bool)
ishape = np.shape(initial)
state = np.zeros((1,ishape[0],ishape[1]), dtype=int)
np.copyto(state, initial)
# state[1][1:9,1:9] = initial
print(state)
print(np.shape(state))
# c = np.pad(c, 1, mode='constant', constant_values=0)
# print(np.shape(c))
# def activeNeighbours(x,y,z,state):

#     for z in range(max(z-1,0), min(z+1,len(state))):
#         layer = state[z]
#         for y in range(max(y-1,0), min(y+1,len(state))):
#             row = layer[y]
#             for x in range(max(x-1,0), min(x+1, len(row))):

def expand(a):
    return np.pad(a, 7, constant_values=0)

def run1(initial):
    # so we don't worry about edge cases
    state = expand(initial)
    shape = np.shape(state)
    
    import matplotlib.pyplot as plt
    from mpl_toolkits.mplot3d import Axes3D
    import matplotlib.animation as animation
    fig = plt.figure()
    fig.set_size_inches(20, 20, True)

    ax = fig.add_subplot(111, projection='3d')
    z,x,y = state.nonzero()
    scat = ax.scatter(x,y,z, c='b', marker='s', s=200.0)
    ax.set_xlim((1,shape[2]-2))
    ax.set_ylim((1,shape[1]-2))
    ax.set_zlim((1,shape[0]-2))
    states = []

    def update(i, state, scat, states):
        if len(states) > i:
            state = states[i]
        else:
            newstate = np.copy(state)
            shape = np.shape(state)
            for z in range(1, shape[0]-1):
                for y in range(1, shape[1]-1):
                    for x in range(1, shape[2]-1):
                        me = state[z,y,x]
                        neighbours = state[z-1:z+2,y-1:y+2,x-1:x+2]
                        lit = (neighbours == True).sum()
                        if me:
                            lit -= 1
                        if me and lit != 2 and lit != 3:
                            newstate[z,y,x] = False
                        elif not me and lit == 3:
                            newstate[z,y,x] = True
            np.copyto(state, newstate)
            states.append(state.copy())
        z,x,y = state.nonzero()
        scat._offsets3d = (x,y,z)

    print(animation.writers.avail)
    Writer = animation.writers['html']
    writer = Writer(fps=15, metadata=dict(artist='Me'), bitrate=1800)
    ani = animation.FuncAnimation(fig, update, frames=range(0,6), fargs=(state, scat, states), interval=500, repeat=True)
    ani.save('im.html', writer=writer)
    #plt.show()

    result = (state == True).sum()
    return result

part1 = run1(state)
print(f'Part1: {part1}')



state = np.zeros((1, 1,ishape[0],ishape[1]), dtype=int)
np.copyto(state, initial)


def run2(initial):
    # so we don't worry about edge cases
    state = expand(initial)
    # Stages
    for _ in range(0, 6):
        newstate = np.copy(state)
        shape = np.shape(state)
        for w in range(1, shape[0]-1):
            for z in range(1, shape[1]-1):
                for y in range(1, shape[2]-1):
                    for x in range(1, shape[3]-1):
                        me = state[w,z,y,x]
                        neighbours = state[w-1:w+2,z-1:z+2,y-1:y+2,x-1:x+2]
                        lit = (neighbours == True).sum()
                        if me:
                            lit -= 1
                        if me and lit != 2 and lit != 3:
                            newstate[w,z,y,x] = False
                        elif not me and lit == 3:
                            newstate[w,z,y,x] = True
        state = newstate
    result = (state == True).sum()
    return result

part2 = run2(state)
print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')