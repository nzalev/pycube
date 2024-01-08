# PyCube #

Provides for a simple importable 3x3 Rubik's cube.

```python
from Cube import Cube

cube.execute("R' L U2 D2 F2 B2 L")
cube.turn_R_prime()

print(cube)


# Find the index of a particular Cubee
for idx, cubee in enumerate(cube.cubees):
    if cubee.id == 'BRW':
        print(idx)
        break
```

The cube is split into 27 Cubees. Each Cubee has a unique ID which can be used to find its position.


```

0------2.       0------2       +------+       0------2       .0------2
|`.    | `.     |\     |\      3      5      /|     /|     .' |    .'|
|  `6--+---8    | 6----+-8     +------+     6-+----8 |    6---+--+' 11
|   |  |   |    | |    | |     |      |     | |    | |    |   |  |   |
18--+-20.  |    18+---20 |     +------+     | 18---+20    15 .+-17---+
 `. |    `.|     \|     \|     21    24     |/     |/     |.'    | .'
   `24----26      24----26     +------+     24----26      +------+'




          0          1           2
     3          4           5
6          7           8



          9          10          11
     12         13          14
15         16          17



          18         19          20
     21         22          23
24         25          26

```

Cubee IDs:
```
BOY, BY, BRY, BO, B, BR, BOW, BW, BRW, OY, Y, RY, O, R, OW, W, RW, GOY, GY, GRY, GO, G, GR, GOW, GW, GRW
```