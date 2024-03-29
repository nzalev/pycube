class Cubee:
    def __init__(self, up=None, down=None, right=None, left=None, front=None, back=None) -> None:
        self.up = up
        self.down = down
        self.right = right
        self.left = left
        self.front = front
        self.back = back

    def _set_id(self) -> str:
        self.id = ''.join(filter(None, (self.up, self.down, self.right, self.left, self.front, self.back)))

    def _turn_R_LP(self):
        self.front, self.up, self.back, self.down = self.down, self.front, self.up, self.back

    def _turn_L_RP(self):
        self.front, self.up, self.back, self.down = self.up, self.back, self.down, self.front

    def _turn_U_DP(self):
        self.front, self.left, self.back, self.right = self.right, self.front, self.left, self.back

    def _turn_D_UP(self):
        self.front, self.right, self.back, self.left = self.left, self.front, self.right, self.back

    def _turn_F_BP(self):
        self.right, self.up, self.left, self.down = self.up, self.left, self.down, self.right

    def _turn_B_FP(self):
        self.left, self.down, self.right, self.up = self.up, self.left, self.down, self.right


class Slice():
    def __init__(self, cube, indices: list, idx_start=None, idx_end=None) -> None:
        self.cube = cube
        self.indices = indices
        self.idx = idx_start - 1 if (idx_start) else -1
        self.idx_end = idx_end if (idx_end) else len(indices)

    def __iter__(self):
        return self

    def __next__(self):
        self.idx += 1
        if self.idx < self.idx_end:
            return self.cube.cubees[self.indices[self.idx]]
        self.idx = -1
        raise StopIteration

    def __getitem__(self, real_slice: slice):
        return Slice(self.cube, self.indices, real_slice.start, real_slice.stop)

    def _rot(self, swaps):
        cubees = self.cube.cubees
        tmp = cubees[self.indices[swaps[0][0]]]
        for a,b in swaps:
            cubees[self.indices[a]] = cubees[self.indices[b]]
        cubees[self.indices[swaps[-1][1]]] = tmp

    def rotate_clockwise(self):
        self._rot([(2,0), (0,6), (6,8), (8,5), (5,1), (1,3), (3,7), (7,8)])

    def rotate_counter_clockwise(self):
        self._rot([(0,2), (2,8), (8,6), (6,1), (1,5), (5,7), (7,3), (3,6)])


class Cube:
    def __init__(self, color=False) -> None:

        w = "■" if color else 'W'
        r = "\033[31m■\033[00m" if color else 'R'
        g = "\033[32m■\033[00m" if color else 'G'
        y = "\033[33m■\033[00m" if color else 'Y'
        b = "\033[34m■\033[00m" if color else 'B'
        o = "\033[38;5;166m■\033[00m" if color else 'O'

        self.cubees = [Cubee() for _ in range(3*3*3)]

        self._slice_u = Slice(self, [i for i in range(9)])
        self._slice_d = Slice(self, [i for i in range(18, 27)])
        self._slice_l = Slice(self, [6, 3, 0, 15, 12, 9, 24, 21, 18])
        self._slice_r = Slice(self, [8, 5, 2, 17, 14, 11, 26, 23, 20])
        self._slice_f = Slice(self, [6, 7, 8, 15, 16, 17, 24, 25, 26])
        self._slice_b = Slice(self, [2, 1, 0, 11, 10, 9, 20, 19, 18])

        for cubee in self._slice_l: cubee.left = o
        for cubee in self._slice_r: cubee.right = r
        for cubee in self._slice_d: cubee.down = g
        for cubee in self._slice_u: cubee.up = b
        for cubee in self._slice_f: cubee.front = w
        for cubee in self._slice_b: cubee.back = y

        for cubee in self.cubees: cubee._set_id()

        self.turn_map = {
            "R"  : lambda: self._turn(self._slice_r, '_turn_R_LP', clockwise=True),
            "R'" : lambda: self._turn(self._slice_r, '_turn_L_RP', clockwise=False),
            "L"  : lambda: self._turn(self._slice_l, '_turn_L_RP', clockwise=False),
            "L'" : lambda: self._turn(self._slice_l, '_turn_R_LP', clockwise=True),
            "U"  : lambda: self._turn(self._slice_u, '_turn_U_DP', clockwise=True),
            "U'" : lambda: self._turn(self._slice_u, '_turn_D_UP', clockwise=False),
            "D"  : lambda: self._turn(self._slice_d, '_turn_D_UP', clockwise=False),
            "D'" : lambda: self._turn(self._slice_d, '_turn_U_DP', clockwise=True),
            "F"  : lambda: self._turn(self._slice_f, '_turn_F_BP', clockwise=True),
            "F'" : lambda: self._turn(self._slice_f, '_turn_B_FP', clockwise=False),
            "B"  : lambda: self._turn(self._slice_b, '_turn_B_FP', clockwise=True),
            "B'" : lambda: self._turn(self._slice_b, '_turn_F_BP', clockwise=False),
            "R2" : lambda: self._turn2(self.turn_map['R']),
            "L2" : lambda: self._turn2(self.turn_map['L']),
            "U2" : lambda: self._turn2(self.turn_map['U']),
            "D2" : lambda: self._turn2(self.turn_map['D']),
            "F2" : lambda: self._turn2(self.turn_map['F']),
            "B2" : lambda: self._turn2(self.turn_map['B'])
        }

    def __repr__(self) -> str:
        return (
            '        +-------+\n'
            '        | {} {} {} |\n'
            '        | {} {} {} |\n'
            '        | {} {} {} |\n'
            '+-------+-------+-------+-------+\n'
            '| {} {} {} | {} {} {} | {} {} {} | {} {} {} |\n'
            '| {} {} {} | {} {} {} | {} {} {} | {} {} {} |\n'
            '| {} {} {} | {} {} {} | {} {} {} | {} {} {} |\n'
            '+-------+-------+-------+-------+\n'
            '        | {} {} {} |\n'
            '        | {} {} {} |\n'
            '        | {} {} {} |\n'
            '        +-------+\n'
            '        | {} {} {} |\n'
            '        | {} {} {} |\n'
            '        | {} {} {} |\n'
            '        +-------+\n'
        ).format(
                     *[c.up    for c in self._slice_u],
            *reversed([c.left  for c in self._slice_l[0:3]]),
                     *[c.front for c in self._slice_f[0:3]],
                     *[c.right for c in self._slice_r[0:3]],
            *reversed([c.back  for c in self._slice_b[0:3]]),
            *reversed([c.left  for c in self._slice_l[3:6]]),
                     *[c.front for c in self._slice_f[3:6]],
                     *[c.right for c in self._slice_r[3:6]],
            *reversed([c.back  for c in self._slice_b[3:6]]),
            *reversed([c.left  for c in self._slice_l[6:9]]),
                     *[c.front for c in self._slice_f[6:9]],
                     *[c.right for c in self._slice_r[6:9]],
            *reversed([c.back  for c in self._slice_b[6:9]]),
                     *[c.down  for c in self._slice_d[6:9]],
                     *[c.down  for c in self._slice_d[3:6]],
                     *[c.down  for c in self._slice_d[0:3]],
            *reversed([c.back  for c in self._slice_b[0:3]]),
            *reversed([c.back  for c in self._slice_b[3:6]]),
            *reversed([c.back  for c in self._slice_b[6:9]])
        )

    def _turn(self, slice, turn_func, clockwise):
        for cubee in slice:
            getattr(cubee, turn_func)()
        slice.rotate_clockwise() if (clockwise) else slice.rotate_counter_clockwise()

    def _turn2(self, turn_func):
        for _ in range(2): turn_func()

    def execute(self, turns: str):
        turns = turns.split(' ')
        for turn in turns:
            self.turn_map[turn]()