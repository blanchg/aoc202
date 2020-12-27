from hex import Hex, Layout, Point, hex_add, hex_direction, hex_distance, hex_neighbor, hex_scale, layout_pointy, polygon_corners
import time
from collections import deque, defaultdict
ms = time.time() * 1000

class HexValue:
    def __init__(self, q, r=None, s=None) -> None:
        if isinstance(q, str):
            q,r,s = q.split(',')
            self.hex = Hex(int(q),int(r),int(s))
        elif isinstance(q, tuple):
            self.hex = q
        else:
            self.hex = Hex(q,r,s)

    def __repr__(self) -> str:
        return self.key()

    def key(self) -> str:
        return f'{self.hex.q:2},{self.hex.r:2},{self.hex.s:2}'

    def add(self, hexdir):
        self.hex = hex_add(self.hex, hexdir)

def apply_instructions():
    
#     instructions = [
# 'sesenwnenenewseeswwswswwnenewsewsw',
# 'neeenesenwnwwswnenewnwwsewnenwseswesw',
# 'seswneswswsenwwnwse',
# 'nwnwneseeswswnenewneswwnewseswneseene',
# 'swweswneswnenwsewnwneneseenw',
# 'eesenwseswswnenwswnwnwsewwnwsene',
# 'sewnenenenesenwsewnenwwwse',
# 'wenwwweseeeweswwwnwwe',
# 'wsweesenenewnwwnwsenewsenwwsesesenwne',
# 'neeswseenwwswnwswswnw',
# 'nenwswwsewswnenenewsenwsenwnesesenew',
# 'enewnwewneswsewnwswenweswnenwsenwsw',
# 'sweneswneswneneenwnewenewwneswswnese',
# 'swwesenesewenwneswnwwneseswwne',
# 'enesenwswwswneneswsenwnewswseenwsese',
# 'wnwnesenesenenwwnenwsewesewsesesew',
# 'nenewswnwewswnenesenwnesewesw',
# 'eneswnwswnwsenenwnwnwwseeswneewsenese',
# 'neswnwewnwnwseenwseesewsenwsweewe',
# 'wseweeenwnesenwwwswnew',
#     ]
    instruction = ''
    layout = defaultdict(bool)

    for path in instructions:
        pos = HexValue(0, 0, 0)
        for letter in path:
            if letter == 'n' or letter == 's':
                instruction = letter
                continue
            else:
                move = None
                instruction += letter
                if instruction == 'e':
                    move = 2
                elif instruction == 'w':
                    move = 5
                elif instruction == 'ne':
                    move = 3
                elif instruction == 'nw':
                    move = 4
                elif instruction == 'se':
                    move = 1
                elif instruction == 'sw':
                    move = 0
                else:
                    raise Exception('Unknown instruction', instruction)
                hexdir = hex_direction(move)
                pos.add(hexdir)
                # print(instruction, pos)
                instruction = ''
        key = str(pos)
        # print(key)
        # if key in layout:
        layout[key] = not layout[key]
        # else:
            # layout[key] = True

    return layout

def run1():
    result = 0
    layout = apply_instructions()
    for k,v in layout.items():
        print(k,v)
        if v:
            result += 1
    return result

def hex_ring(center, radius):
    results = []
    # this code doesn't work for radius == 0; can you see why?
    cube = hex_add(center, hex_scale(hex_direction(4), radius))
    for i in range(0, 6):
        for j in range(0, radius):
            results.append(cube)
            cube = hex_neighbor(cube, i)
    return results

def hex_spiral(center, radius):
    results = [center]
    for k in range(1, radius + 1):
        results.extend(hex_ring(center, k))
    return results

def run2():
    result = 0
    layout = apply_instructions()
    max_distance = 1
    center = Hex(0, 0, 0)
    print('Before', len(layout.items()))
    hex_layout = Layout(layout_pointy, Point(10, 10), Point(480,480))
    # c = tk.Canvas(app.root, width=960, heigh=960, bg='lightgrey', highlightthickness=0)
    # c.place(x=0, y=0)
    # hexen = {}
    for k,v in layout.items():
        hex1 = HexValue(k)
        distance = hex_distance(center, hex1.hex)
        if distance > max_distance:
            max_distance = distance + 1
    print('max dist', max_distance)
    for h in hex_spiral(center, max_distance):
        k = str(HexValue(h))
        if k not in layout:
            layout[k] = False
        # c.create_polygon(polygon_corners(hex_layout,h), fill='',outline='grey')
    #     hexen[k] = c.create_polygon(polygon_corners(hex_layout,hex1.hex), fill='white' if not layout[k] else 'black',outline='grey')


    print(bool())
    print('After', len(layout.items()))
    # poly = polygon_corners(hex_layout,center)
    # print(poly)
    # c.create_polygon(poly, fill='black',outline='grey')
    # c.place(x=0, y=0)
    for day in range(1, 101):
        # time.sleep(0.1)
        layout2 = defaultdict(bool)
        items = layout.copy().items()
        for k1,v1 in items:
            hex1 = HexValue(k1)
            neighbours = []
            for move in range(0,6):
                hex2 = HexValue(hex_neighbor(hex1.hex, move))
                k2 = str(hex2)
                if layout[k2]:
                    neighbours.append(1)
                # else:
                # neighbours.append(1 if layout[k2] else 0)
            black_neighbours = sum(neighbours)
            layout2[k1] = v1
            if v1: # True is black
                if black_neighbours == 0 or black_neighbours > 2:
                    layout2[k1] = False
            else:
                if black_neighbours == 2:
                    layout2[k1] = True
                    dist = hex_distance(center, hex1.hex)
                    if dist >= max_distance:
                        max_distance = dist + 1
                        print('New max', max_distance)
                        for h in hex_spiral(center, max_distance):
                            k = str(HexValue(h))
                            if k not in layout2:
                                layout2[k] = False
        layout = layout2
        result = 0
        # c.delete('all')
        # for h in hex_spiral(center, max_distance):
        #     k = str(HexValue(h))
        #     if k not in layout:
        #         layout[k] = False
            # c.create_polygon(polygon_corners(hex_layout,h), fill='',outline='grey')
        for k,v in layout.items():
            # print(k,v)
            if v:
                result += 1
            # hex1 = HexValue(k)
            #c.create_polygon(polygon_corners(hex_layout,hex1.hex), fill='white' if not v else 'black',outline='grey')
            # c.itemconfig(hexen[k], fill='white' if not v else 'black')

        print(f'Day {day}: {result}')


    return result



# import tkinter as tk
# import threading

# class App(threading.Thread):

#     def __init__(self):
#         threading.Thread.__init__(self)
#         self.root = None
#         self.start()

#     def callback(self):
#         self.root.quit()

#     def run(self):
#         self.root = tk.Tk()
#         self.root.protocol("WM_DELETE_WINDOW", self.callback)
#         self.root.geometry("960x960")
#         # label = tk.Label(self.root, text="Day 20")
#         # label.pack()

#         self.root.mainloop()
# app = App()

instructions = [
'wwwnwwwwwwwwenwwwwwwww',
'swwwswswswswswswwswswswneswswswwswse',
'nenenesenewnenenesenesenenenenenewnewnene',
'seseswseseswseswwswseswseseseseneswseswse',
'nwnwsenwnwnwnwnenwnenwnwnwsenenwsenwnwnwne',
'swswswwswnewswswsw',
'eneeswnenenweesenenenwneneneeenene',
'wnwwnwwnwsewnwwnwnwwnwwwnwwnwnw',
'nwneswsenewenwnwswneswnenenwenwnenenwnwnw',
'senewnwwwwwwnwwwnwnwnwnwnwwwew',
'eewneneneeeeneeese',
'eneewseeneswnweswnwswsw',
'swwswswseswnwneseswseenwwsesesenewne',
'swswswswswswseswswseswswsenwsesesenwsee',
'esesenwnwnwseseneeswseswnwwewesesee',
'neenenwneswneneneeneneeweneneneswne',
'eeswswwwsesesenwswswsenwneswsenwswnenenw',
'swswswsweswswswseswnwswswswswswswswnesw',
'sewswswswwnwswnwswwwwwwswnwsesewsw',
'newnwseeneneeewseneswnenenenwenesee',
'eseneneneneseeeneweenweswswenwee',
'newswsesewswsewnwwnewneswwswnwsenww',
'eneneneeeewneswsewseeeenwnwnwnee',
'nesenwnweeswswnesesweseseseneswsesesw',
'swswneseswswsewswwswswneswswswseswseswsw',
'eneneeeseeeeeeweeeeeee',
'nenewnwneeneswseneneeswnenwswenenewne',
'swneseeneeeneneeeneeeeeweneeene',
'nwsenwwnwnwnwnwweswwnwsenwsenwnw',
'neeenenewneenese',
'ewsenwseseseeseseneseeeeseswewsese',
'nwnwsenenwnwnwwnwnwnwwsenwnwnwwsenwnw',
'neneseswnwnenwnwnwnenwnwnenwnenenenenenw',
'seseseseswswsenwwswswswswseseee',
'nenenwnwnwswnenenenenwnenwnenenenenene',
'nenesenenewnenwnenenwnwnwnwswnenenenwnenese',
'wswswswswswsweseswswswswswneswswswnwse',
'wwwnwnwnwwwsewnewnwwswsenenwww',
'eswswswsenenwsewseseeswseswnwnwnwswswsw',
'swswnwswewwneswwwwwwweswesww',
'swsweswswswswswswswswswswewneswswsewsw',
'wwsenwnwenwswnwnwnesesenenwnwnwsenenwnw',
'weeneneneenenweeneeseneseeenee',
'swwewwswwswsweswnewseneswwwswww',
'sewnwswnwwneswnwwneesewnewwnwewnw',
'wwwwwswwswwsewswwwswswwnenwww',
'neewneneenewswneeenwneeeneneswne',
'nwnenewnwsenwnesenwnenenwenwnenwnwnenwnw',
'swswswswswwwswsenwswswswwswswswneseswsw',
'wsewwwnwwwwwwwewnewwwnww',
'neeeseeneseseenwseseseeswnewseseseew',
'nwsenwneenwwnwwnwswnwnwwswwnwswneswew',
'wnwnwnewswnwnenwnwsewewwnwnwesenw',
'swwswwswnwswswswswweseswwneswswswsw',
'eeeeewnweseeeeeneeseseeeeenw',
'swneeeweeeseesew',
'wwwwwswswnewswswnenwwseneswwwse',
'nwseseseseseseseseseseeswneesesesesese',
'nwewwwnweneswswewswenwwweeseene',
'nwneneswnwneenenwswenwneswswenwnwnenenene',
'swwwswsenewseswnewnewwwswseswwswsw',
'nenenwnwnenwnwnenwnwneneeswnwnwnwnenene',
'nwnwwnwnwnwnenwnwnwnwnwnwnwnwwnwnwnwnwse',
'esenwnwwswnwneeswswseeenenwswneneene',
'eseseeseseeseseesesenwseseeeesee',
'nwenwwwnwenenwnwenwnwnwswnenwnwnwnwnw',
'eseenwseseseseswenwseseseseseeesesese',
'eeeeeeeeeeeeeswnwneeneene',
'wnwwwnwnwwnenwwwnwwwewswwwwnw',
'senwwneseseeseseseeseswwseenewsesesw',
'senwneseseseewseeweneseeseeeese',
'eeeeesweseswneswnweswnwnwenwneeww',
'nenenwswneeneeeeneeswneeeneeenenwe',
'nenwnenwnwnenwsenwnwnwwnenwnwnwnwnwnenw',
'eswnwenwsesesenwswenwnwswwnesenwswswswsw',
'seseseseseseseeseseseseseseweeeese',
'eswneenenwswewneeneneeneeeneee',
'sweswswswswwnwswsweswswswwswsww',
'swwwswswswwswwwnewwswswsewwsww',
'swsesesesesesesesesesesesesesesene',
'neneneneneneneeneneenewneneenenenene',
'neseswwswwswwwsewwwswswsenewwnew',
'swseneneseseswswswswseseswsesesesesesese',
'eswwswswwnwswenwsweswswswswnwwseswswsw',
'nenenenwnenenenenenwneneneneneneneenesw',
'nwnwewswnwneswseeewnwswseswenenwenw',
'wwwwnwnwwwnwwnwnwwweswnwwnwnww',
'nwnwnwnwnwnwnwnwnewnwswneswnwnenwsenw',
'wseseseseseseseseseesenese',
'senwswneswswswswswseswswswswseswsewswswse',
'eesesweneweeenwneeneeeesweeee',
'seeneseeeseeeenweeweeeewee',
'nenwnenweswneswnwnwne',
'neeneneeneneenewnenenesweeneenwene',
'seseseseseseseseseneseseesewsesesesesese',
'eswswsesenwnenwwnwswnwsenwnenwwnwnenee',
'nwnwnwwnwnwnwenwsewwenenwnwnwwswnw',
'wwnwnwnwwnwneswnw',
'nenwneneswnwnwneneneenenwneneenwnenew',
'swsewneswneswneswnweneese',
'eneeewneswnweneeseeeneneneenenene',
'sesewsewsweeneneeneneesenwewswsesw',
'seeenweseenweeseneeenweewesw',
'eenwwneeeeneeneeweneswnweeswne',
'neswwnewnwswswswweswwswwswsesw',
'sesenesewseseweseseseweneseseseese',
'eeenwneswsenwseswseseeeenwswenwew',
'nwnwneenenenwsweewnwnenwnenenewsewse',
'swswswwswswswswneswswswewswswswnwwww',
'swwnenenesenwesewnwswesesewnwesese',
'eseseseswewesesenweeseswnw',
'wswswswwwwwwswwswswswwwwwnew',
'nwseeseeeseseswseseseseseseesee',
'wsewseeeseeeeeeeneeneeseeeee',
'nenenewneneneneneneneneneneneneneenene',
'enenenwsenweenwswnwswswswswwswenwenwnw',
'nenwneneneswnwnenenenwnenw',
'eeewseseseeneeseeeseeenwswsee',
'enesweneswweeneenweeneneewsenewe',
'seswswswswseswswnwswseswswnwswswswswswsw',
'nwnwnenenenenenwswnenenenw',
'wwswwswwwwwwwwewwwswnwwww',
'eeeneseeweneneneeeneeneeenenee',
'nenewnenewneeneweneeneewnenenenene',
'seswenwseswswswswsewswswswswseneseswswse',
'nwnwnwwnwwwwnwnwnwnwnwnenwnwnwsewwnw',
'eseseseseswwseseeseesewseswseswswswnw',
'newwnenenenenwenenewswneswsenenesenese',
'nwnenesenenenwnesenwnenwnwnwnewnwnenwnenw',
'swesweswswswswswswwswswswswswswswswswswnw',
'nwnwswnenwnenenwnenwnenwnenw',
'nenenenenenenenenenenwneneeswnenenenene',
'nwewnwnwnwnwnesewswnenwnw',
'swswseseseseseswseeseswesesesesenwsenw',
'wwsewnenewnwwswwwwneswsenwwnww',
'neeesenenenenewneneeeneeeeneneene',
'wwwwwswsewnwww',
'seseeseseewneseseseesesesesesesesesese',
'swneweneeswneenwneswnenwneeenenene',
'eneeseeeeenenweeseneeenenwee',
'swnwwnwwsenwnesewswwnwnwnwenwnwnenwnw',
'swseseswseseseswseswsweseswsesesesenwsesw',
'wswnewswswswswwwwseww',
'seseseseseseseeenwseseseswseseseseesese',
'eeneseesenenewwenwsenenenenwenesewse',
'nwewwswswsweeswswwswwseswswwswsww',
'seswswswswswwwswswnewswswwewswswswsw',
'swseenenwnwnenewwsenenenewswneneese',
'wwwswenwwwswnwwseswsewnwseswwswne',
'senwseeeeseseseseseeseeeseswnwsesese',
'wnenewnenenenesenenenenenewsesenwnenene',
'neeeeeeeneseeeeeeenweeee',
'swswneswswswswswswneswswswswswwse',
'enwseswwswnwneswswswneeswswswswsesenwswsw',
'swnwsesewneseseseseseseswwsenesesw',
'seeeeeeenweeeneeeeene',
'eseswswseeswseswswwwse',
'newnenwswsenenweneneseenwsweeeewe',
'nwswseswswseesewseseseseswsenesesesese',
'enwneswseeswnenesewsenwswsenwseswswsw',
'swwsweneeseneenweseeeeeeewee',
'swwsewwwwwnwwwewwwwwwwnw',
'swneswswswswswwwswwnewswswwsewww',
'nenewneseenesewnwneswnenenenwnenenesene',
'neneenewsewseneenenenenenesenenwnenee',
'eseswneseeneneneweneeneneenewene',
'seeseseeseseseswseesenwnweseeeenw',
'enenwwnwswseewsewnwsewseesenesesese',
'nwwsenwwnwnwwwnwwwwwnwsewwnww',
'neeneeenewswneeseenenenenenweeswne',
'wsewneseswnwsenwseseneweseewseene',
'swswswswswswswswwswneswswswswswswswswsw',
'seeeenwseseseeeeseeseeeeseee',
'nwesenenwwnewwnwneenwweswnwsenenw',
'wnenwnenwsweneneseneneeswnenwnwnenesew',
'eeeseeeeeeseeeseeeeenwnwee',
'esenwwswwseweseseswseseseswseneeswnw',
'wnenenenwenwesewneneseseewnewnenese',
'nwnenwnenwnwnwnwnwwenenwnwnenwnwneswnw',
'eneneswnenenenwneneeeenenwneneswene',
'sewwwswswswwsewnwwswswneww',
'wwwswwswwwswwswwwwnewswseswsww',
'swswseseseseswswsewswesewseswseesesesw',
'senwnwwnwnwwwnwnwnwnwnwnwwnwnwswenww',
'wwewnwewsewwnwwnweseswswenesenw',
'neneneeeneeneneneneswneneeneeeswe',
'eeseneewesweeeseeeeeeeenwee',
'esenewnewnwneswneneneneeneneeeeee',
'wwnwwwwwwwsesewnwwwwwwswwsw',
'nenwseneesweneneneneswenenenwwsewnee',
'seswseswswnwnwswswsw',
'swneneenesewnwnwneneneswesewwnenenesw',
'neeneeeeweeneneneneneneneneenene',
'nenweneeeenwneneneseneeeneseneew',
'wswwneswswswsewswswswsenwswnesw',
'nwnwnenwnwnwnwswsenwwnwenwnwnesenwnwnwnw',
'senwnwwnwwswwnwwwnwnwnwwnwwnwwe',
'nenenwnwnwneneneenenenenwseswnwnenwneswnw',
'seeeseeeeseeeeeeeenwsewee',
'seseeseseseeeeeseneeseseewsesee',
'sesesewseseseseswswsweseswsewseswnesenwse',
'nwswnenwnwnwnwnwnwnwnwnwnwnwnwnwnwnw',
'nwnwnwnwnwnenwnwneenwsww',
'nenwneseneswnwneswnenwnenenwnwnenwnenwne',
'eneneneneneneweneneseneneeneneenenee',
'nwnwnwnwswnwnwesenenwneneswnwnwnwenwnenww',
'neneneneneneneneneneneneswnenenenenenesw',
'enwnewwswsesenwsenwsesweeeswnwnwse',
'neswwswswesenenwenenenenwswseeenwe',
'nwwnwnwnwsewnwnwwwwnenwnwnwsenwenw',
'swnwenwenweswswseswswwswwneswneswwwse',
'eeeeneeneneeeneeneeewnee',
'eeswseswseswswwwswneswwsweswswswne',
'swnwswswswswswwenwswswswswenewnwsewsw',
'nwwswnwnwwwneswnwwnwnwnwnewwnwwnww',
'nwswneeneewwewewneseseneseseswse',
'weneneeseneswwswswneeeeenwese',
'seneeseseeeseseewseeseeswsenwsee',
'swswswseswneseswsenwseseseseswsesesesesewse',
'nenenwwswwnwnwenweenwnwswsweswswsenw',
'nwnwnwnwnwnwnwnwnenwnwnwnwnenwnwnwsenwswsw',
'nwwwwnenwnwnwwnwnwwswnwwewnwnwsese',
'nwswseeseswsesesesenwsesesesesesese',
'seswseswswswnwsweswswnewswswnwswseswswsw',
'neseswwsewsewswwsweeswseeswne',
'swwwwnwnwenwwnwwwwwwnwwwwww',
'swwnenweneneewneeseneenenenenwseesene',
'nenenenenenwneneneswneneneneenenenenene',
'wnwnenwesenwnwnwwnwnwnwwnwwnwnwnwnww',
'wsesesesesesesesesesesesene',
'neneswnenwwnwnenwneenwnwnwnwnwnwnenwnw',
'wswsenwswsenenwnwseseseseesesesesenw',
'wwnwnwnwnwwnwneesesenwnwnwnwnwnwnwnw',
'nwenwneneneneswnenwnwnwnwnenwnwnenwnenw',
'eeneneesewneeeesenenenenewsenwene',
'sesesewneswseseseseswseseswse',
'sesenwsesesewseseeseeseseneseswesesese',
'nenwseswseseneseswwsesweseswnwsesesesesene',
'eseeseseeseesesesesesenweeewese',
'nwnenwwnwnwwnwsewnwwnwwwwnwwnww',
'swesenweeseseesewsesesesese',
'eeeneeeeeeneeenesewnenwswee',
'nenenweneeneneeewneseeneneneeenee',
'newswswwwwwwwsewwewswneswww',
'swswneswseswsweswnwwseeseswswswsewswswsw',
'ewwswswswneswwswswnwenwnweewesenw',
'wsenwnwsesewwnwnwwnewnwenenwnwnwwnw',
'nenwnwneneenenenenwnwnwnewsenenene',
'enenweswenwnenwswseeweeswseeeene',
'seeneseeeeeeseeweweeneenwee',
'enwnenweswnwnwswneswnenweseswnw',
'enwsenwswswnenewwseseeswwswnenenene',
'wnwsewenewnwwwwnwenwnwwwenwsenw',
'wswnwswswswswsenenwneneewesewswsewwnw',
'seseeewseeseseseeesesesenwseseseee',
'neeewenenwesenweeswnewwnwswswse',
'neenwnenwenwnwswswnwenewswneneswenwnw',
'nenenenesenenenenenewenee',
'eswseswwwwwnenwswwwsweewnwww',
'nenenenenwwenenenenenenwseswnesenewnwe',
'weeneneseneneneneneneneneneneenenene',
'sewseseswneseseswseswseesewnwseswseswnese',
'swswswswswswseswswseswneswswswwswsesesw',
'eeenwneneeeeeeeeswneneswnenee',
'sesenwsewneswseseweseseseeswswsewsene',
'seseseseseseswseseseeswsewsesenesenwe',
'wwswwswwwsenesww',
'wwnwnwwsenwwnwnenwnwnwnwnwseeswwe',
'swswwwswwwwwwswwwwseneeswwww',
'neswsweswnwswwswswwswswseswswswswswsw',
'sesesesesesewseseseseseesesesee',
'sesenwsweseenweenweswwseeneeesenwe',
'eeeeneeeesweeeeeeeeesweenw',
'esesesesesenwneweneeeseesesewsese',
'seseseneeeeeeweeseeseeesesese',
'wwnewwseswwswwwwswew',
'neswswswseswswseswswseswswwswswswswswswsw',
'seseseseswnesweswseneswsesesesewswsesese',
'seseseseseseseseneseseseseseswsesesewsesw',
'wnwneswswswseswswnwswwwwswswswsweww',
'neeeweeeeseeeeeneeeeneenee',
'nwswwwswnewnwswsenwwwwswwseeewe',
'swwwwwswewwwwnwwwnwwwewwnw',
'nwsenwnwnwnwnwwwnwnwnewnwnwnwnwsewnwnwne',
'wseeeewenesesenwweneeneeesesesww',
'swwwswswwswswneswwsewswwswwwswsw',
'nweeenenenwseewswnewsewenewsewe',
'swswseswswswswswswwswswswswseswswswneswsw',
'eeneeeneeeeeeseeneneweneeee',
'nenwsesenwnwnwnenwnwnwnwnwnwnewnenwnwnwnwnw',
'nwsweswswseseseseseswswswseseseseswswsesw',
'sesesenwenwewseeeseeseseneeeswnw',
'nwnwnenwewnwnwwwnwnwse',
'nwwnenwnwnenenenenwnenwnwnwneneseenewne',
'eseseesesesesenwnesweweneswneswwnw',
'nwnwwwwwenwnwnwsenwwww',
'nwnweneneenwsenenwnwwneneswnwnwwsenwnw',
'swseswsenwswnweseswseswsewseseeesw',
'neneneswnwnwseswwsenwnwwnwnwnenwnene',
'seeesewseneseseswsesesesenwseesesesee',
'senenweweseeneneeneswseeweseneww',
'eeeeeeweeeseeseeeneeeesee',
'eneseeeeeewneeeneeeeenene',
'wwewswsewwwwwnewwwsw',
'neeeeeeseeeeeeeeesweeee',
'swnwnwsewwwwwnwnwnwnenwenwnwneswnw',
'wseswswseseseswnenweswswsweseswseswse',
'wewnwswwswwwswswnewwwnwnewsewsw',
'nwnenwnenenwnwnenesenwneneseswwenenene',
'swenwneswsewenwwnwneswnwenwnwwswnwnwnw',
'senenenenewswneneneweswnenenenenenenwnene',
'swseseseswsesenwnesweseseeswnwsesenwsesw',
'swseseswneswswneswswswswswswnwneswseswse',
'nwwnwnwnwwnwwweswwnwnwwwnesenwenw',
'seeneswswswneenwesenwsenwwweeeswne',
'seseesesenwseeesesesweseseeeesese',
'senwnwswweseswnwneewwneenwnenenwsenw',
'swswwwwnwswwwseswsesewnwenwwwnese',
'neesenwnwnwnenenwnenewnenenenesenenwne',
'seswswswswsesesesesenwswseneswswswswseswsw',
'nenwwnwswneneenwnenenenwseeeswsenwnesw',
'eneneneeneneswnenenenenewsenenenenenene',
'nwswwwwsewnwwnwnenwnwwwewwsw',
'neneneneweeswseneneneenenenenenenenewne',
'ewwwwwwnenwnwwnwnwwesewnwnww',
'nenenenwnenenwneneneswnwnwnwnwnwneseneswne',
'wnwnwwwwsewnwwnwwwwnwsenwwwswe',
'neneeenwneneeneneeneneswnesweneew',
'wwnwnwwnwewnwwswewwwwnwwwww',
'eseeeeseeeenweenwweswseeee',
'nwnwnwwwnwnwnwswnwnwnwnwnewnwnww',
'eeenenenenenenesenenewneenenenenene',
'wswseswswewseneseewswnesenwswswnenw',
'nwwswnwnwnwnwwnwewwwnwnwnenwnwnwwswnw',
'nwsewneswwswswewswswswnwwnwseseswsw',
'seneneeeeeneeswneneswnwneenenenwne',
'sesenwsenwswseseseswseseswseswseseseene',
'eswswnenewweeseswwswneswwnenwseswne',
'wsweneesenewneswsenwnwsweneneneswnenw',
'nwnwnwnwnwenwnesewsenwswnwnwnwnwwnwnw',
'senwsewseseeseseswseswswswnwsenwseseesw',
'wswnwwswewwswswswwswswswswswswswsw',
'wnwneeswwnwnwnwwse',
'swswwswwwswswswwwswswwswswswneww',
'nwnwwnwwswnwwswenwwnewnwwwwnwnwe',
'seseseesesesesewseeeeseseesenesese',
'sesesesenwseeseseseseseseesese',
'swwwwnesenewnesw',
'senwseswwweseswswswseseseswseseswnesw',
'eeeenewewseeneeeeeseeseseese',
'eweeeneeeeeseneee',
'senwseseseswsesenwnesewwseseswsenwese',
'swsewswwwwnwwwwwwwwwwswwew',
'seeeeeseseesewesesesewseesesese',
'nenwnwnenwnwnwnwnwnwnwenwswnenwnw',
'swswswswswneswswswswsesweswswswswnwsww',
'seswsesesesesenwsesese',
'nenenenenesewneneneneswnenenenenenenenwne',
'swseeeeseeeeeeseeweeseesene',
'swsenwsewsenwsewenwseseswwnweseneese',
'nweneesweseesewseseswewsesese',
'neeseneneneneeseenwnenenenweenenee',
'wneeseeneeneeneeeenwneeneeenee',
'swnwnwnwnwnwnwnwswnwwwwwnwnwenewnw',
'esenwsesenesweeeseswsesesesesesesesese',
'seeeneneseeneweneeswnwneneeeewe',
'nesewswnwwweswswwwwswewswwww',
'wwwewenwnwnwnenwwnwnwnwnwswnwwwnwsw',
'nwnenwnwneseswwewswseesewwnwwnwsw',
'eeeneswesenenesweewneenwnenenwe',
'neswswswnwseseswseseseswewswswwneswsw',
'nenenenwnenenwnesenewnenenenenenenenene',
'wwnenwnewwnwnwswwwnwnwswnwnenwsewnw',
'nwneswswswwswswswswswwsewsw',
'seeswsenweesewneeenweneeswseeesw',
'neseswswseswsesesenwseeswsenesesesesww',
'weneeeeeeeeesweee',
'nwwwwwswwwwwwwnwwnwwwnwnew',
'nenewneneneneeewnwseseneneenewseswe',
'neswswwenenenwneswenwneswnwwswseswwswe',
'nwwnwnwnwnenwnwwwnwnwnwnwnwnenwnwsenwse',
'nwswenwwnwenwnwnwnwnwnwnwnwnwnwnwnwnw',
'nwwsewnwwwwsewnewwwwww',
'nenewneneneseneneeneneswnenwnenenwnwne',
'nwwsewnwnwnwnwsenwnwwwwwwnenenwnwwnw',
'seseswswswnwseswswswswswnweseseseswese',
'nwwnwsenwnwwnwwnwnwwnww',
'nenenwnenenwnwneenenwnenwnwnwwnenwnene',
'newewwewnwwsewweeeneswwwww',
'swnenwnwnwwseswsweswneswswesw',
'wwwwnwwnwnwnwwwwwwnwnwenwww',
'seswswwwnewnewwwnewnewwswwsww',
'eseswneweswneeeewnenw',
'eeneenewwweewenwswesenenwseww',
'wwwwwnwwsewwwswewwswswwswew',
'wesenwsesewewnwne',
'ewnwnwnewseswwseneneenenenenenwneenene',
'newwsewwwwwwwwnewneseswww',
'eeeeneneeneneswneneneneenenenee',
'enwwnwwwwnwewewwwwwnwwwww',
'newewnwswswwsenwesenenwewswswesw',
'nenwnwnenwnwnenwewnwwnwnenenwnwnwnwenw',
'neswnwnwnenenenwwswnenesesenenwnewnene',
'wwwnwwnwwwnwwnwnenwnwse',
'eneneneenwseneeweeesweeeewnee',
'swsesesenesenwesesesesesesewsesesesesesew',
'nweseeeeneswnweenweeswneeneee',
'nwnwnwnwnwnwnwseswnewnwnw',
'wnwneseenenwnenenenwnwnenenenenenwnenw',
'seseeeeeseweeseseseseseeseeenw',
'seseneswseseseseseseseseseseseseseseswse',
'eneenenenenenewneneewnenenenene',
'swswenwswswswswswsewswwwswswswwwswe',
'eseseseesenweseseeeswsenweseseee',
'wnwnwnwwnwwwnwnwnwnwnwnwnwwwsenwnw',
'wneeswneneneneeneneneneneneneneneene',
'seneeseswnwenwwnewsweseweseseseee',
'swwwwswewwswwswwwswwwwsww',
'wenwnwswnwwwwwnesenwnwnwsenwnwnenww',
'swswswswnewwenwnwswnewsesweswsesew',
'seswsesesesesesesesesesesesesesesenwnwsesee',
'swseswswswswswswneswswsw',
'swswenewnwnewnenwnwswnenwnwneseeseswesw',
'wwswwnwnwnwenwnwnwwwewwwenesw',
'nwwneeswnenenwneneenw',
'swseswwswswswswswwswswswswswswswswswnw',
'nenwnenwneseneneneneeneneeneswnenenee',
'seseswseseeswswswswswwswswswswswswseswnw',
'seseseeseneseeseseeesesesewseseesese',
'swwwwwwnwswswwwewwsewwwww',
'swwwwswswswswwewswswswsweswswnww',
'swswswseeswswsesewseswseseseswswsesesw',
'wnewsewswwwsewwnenwwsewwwwww',
'swseseswneswswsewswswswswswswswswswseswsw',
'seseseseswneswswneswswswswsesesesesewsesew',
'nwnwneswnenenwneeswneneenenenenenenenene',
'nenenenenwnwwnenenesenenesenwse',
'wneeneeneneneseneneeneneneneswneenene',
'newneneneesewneeneeenenesenenenenene',
'wseseseseseseseseseseseesenwseseseswnwe',
'nwwwswwnwnwnewwwnwwwwww',
'swseseseseseseswnwseseseseseeseseseseseswnw',
'nwnenwnenwenwswenwswnwnwnenwnenenwnenwnw',
'seeswsewwseseswseswseseswesesesesesesw',
'eeeeeeeeeewseenweseneee',
'seswseswswswnweswswswswswnwswswswswswswsw',
'wneeeeneeneneneneeneeeneeneee',
'newneneseeeeeneeeeweeeeeesew',
'wseswseneseeseeeseneseseesesenwse',
'swnweeeseneseenewwswesenwesweenw',
'newnwnenwnwnenwnwnenenenwnwnenenenwnwsene',
'nwswswswnenwsenwsewwneswseweseseww',
'wswwneewwwswww',
'sesesesesewneeseseswwwenesesesese',
'eeseeseeseneesewseseseeeeeesese',
'seeneeweesenesewwseeseeseswne',
'wswsenwsenenewnenewneeswsesesesesew',
'nenwwseneneswnenenenwneneneenwenwnene',
'seseenwseeseseseesenwseseeeeseeee',
'nenenesenweeeneeeneneneneneneneee',
'seseseewseseseseswswseseseseseeseseswnw',
'enwnwswswwswwwsenwneeesenweewswsesw',
'seseseseseneeseseseseseweeeweese',
'swwwswewwswnwswswswswswwswswwswswsw',
'swsesesesenwswsewesesenwseeswsenwsesese',
'neneneneswneeneeeenwneneswnenwnenene',
'senwewwswnweseneneswneeswnweswwe',
'enenwnenenwnewnwnwnenenw',
'swneswswsewwswswnewneeswnesweswswsw',
'seseseswenwnwseeswswneseenwneseeswsw',
'nenwwwwsenwwww',
'wwswswewwwnwnwwsewnweswewnwnww',
'nwnesenwneneneneenenewnenewseneneesene',
'eseeneneneneeeneneewneneeeenee',
'nesesewswseneesesesweseseeeenesewse',
'newswwsenwswswwswwwswewswwwwswne',
'wwswenwswswwswwswswwwewwswswsww',
'wswsweseseesenesenwseeseneseesenwsee',
'wseenweesesesenenwseeseseseeseesesw',
'wnwwsewwwewswwswswwswwwnewsw',
'enesewneenewswnenenesenenenenenenenw',
'wswswswswwnewswnwsweswsw',
'swswseswswswswswswswswswswswswswneswswse',
'wwswswnwswswseswswnewswseswnesw',
'seswsenwswseswnwseswswswswsenwseeeswwse',
'senenenenwnwewnenenwnenwneneneweseswne',
]

part1 = run1()
print(f'Part1: {part1}')

part2 = run2()
print(f'Part2: {part2}')

print(f'Took {time.time()*1000 - ms}ms')