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


class Cube:
    def __init__(self, color=False) -> None:

        w = "■" if color else 'W'
        r = "\033[31m■\033[00m" if color else 'R'
        g = "\033[32m■\033[00m" if color else 'G'
        y = "\033[33m■\033[00m" if color else 'Y'
        b = "\033[34m■\033[00m" if color else 'B'
        o = "\033[38;5;166m■\033[00m" if color else 'O'

        self.cubees = [Cubee() for i in range(3*3*3)]

        self._slice_u = [i for i in range(9)]
        self._slice_d = [i for i in range(18, 27)]
        self._slice_l = [6, 3, 0, 15, 12, 9, 24, 21, 18]
        self._slice_r = [8, 5, 2, 17, 14, 11, 26, 23, 20]
        self._slice_f = [6, 7, 8, 15, 16, 17, 24, 25, 26]
        self._slice_b = [2, 1, 0, 11, 10, 9, 20, 19, 18]

        for cubee in [self.cubees[i] for i in self._slice_l]: cubee.left = o
        for cubee in [self.cubees[i] for i in self._slice_r]: cubee.right = r
        for cubee in [self.cubees[i] for i in self._slice_d]: cubee.down = g
        for cubee in [self.cubees[i] for i in self._slice_u]: cubee.up = b
        for cubee in [self.cubees[i] for i in self._slice_f]: cubee.front = w
        for cubee in [self.cubees[i] for i in self._slice_b]: cubee.back = y

        for cubee in self.cubees: cubee._set_id()

        self.turn_map = {
            "R"  : self.turn_R,
            "R2" : self.turn_R2,
            "R'" : self.turn_R_prime,
            "L"  : self.turn_L,
            "L2" : self.turn_L2,
            "L'" : self.turn_L_prime,
            "U"  : self.turn_U,
            "U2" : self.turn_U2,
            "U'" : self.turn_U_prime,
            "D"  : self.turn_D,
            "D2" : self.turn_D2,
            "D'" : self.turn_D_prime,
            "F"  : self.turn_F,
            "F2" : self.turn_F2,
            "F'" : self.turn_F_prime,
            "B"  : self.turn_B,
            "B2" : self.turn_B2,
            "B'" : self.turn_B_prime
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
            *[self.cubees[i].up for i in self._slice_u],

            *[c.left for c in reversed([self.cubees[i] for i in self._slice_l][0:3])],
            *[c.front for c in [self.cubees[i] for i in self._slice_f][0:3]],
            *[c.right for c in [self.cubees[i] for i in self._slice_r][0:3]],
            *[c.back for c in reversed([self.cubees[i] for i in self._slice_b][0:3])],

            *[c.left for c in reversed([self.cubees[i] for i in self._slice_l][3:6])],
            *[c.front for c in [self.cubees[i] for i in self._slice_f][3:6]],
            *[c.right for c in [self.cubees[i] for i in self._slice_r][3:6]],
            *[c.back for c in reversed([self.cubees[i] for i in self._slice_b][3:6])],

            *[c.left for c in reversed([self.cubees[i] for i in self._slice_l][6:9])],
            *[c.front for c in [self.cubees[i] for i in self._slice_f][6:9]],
            *[c.right for c in [self.cubees[i] for i in self._slice_r][6:9]],
            *[c.back for c in reversed([self.cubees[i] for i in self._slice_b][6:9])],

            *[c.down for c in [self.cubees[i] for i in self._slice_d][6:9]],
            *[c.down for c in [self.cubees[i] for i in self._slice_d][3:6]],
            *[c.down for c in [self.cubees[i] for i in self._slice_d][0:3]],

            *[c.back for c in reversed([self.cubees[i] for i in self._slice_b][0:3])],
            *[c.back for c in reversed([self.cubees[i] for i in self._slice_b][3:6])],
            *[c.back for c in reversed([self.cubees[i] for i in self._slice_b][6:9])]
        )


    def _rotate_clockwise(self, slice):
        tmp = self.cubees[slice[2]]
        self.cubees[slice[2]] = self.cubees[slice[0]]
        self.cubees[slice[0]] = self.cubees[slice[6]]
        self.cubees[slice[6]] = self.cubees[slice[8]]
        self.cubees[slice[8]] = tmp

        tmp = self.cubees[slice[5]]
        self.cubees[slice[5]] = self.cubees[slice[1]]
        self.cubees[slice[1]] = self.cubees[slice[3]]
        self.cubees[slice[3]] = self.cubees[slice[7]]
        self.cubees[slice[7]] = tmp

    def _rotate_counter_clockwise(self, slice):
        tmp = self.cubees[slice[0]]
        self.cubees[slice[0]] = self.cubees[slice[2]]
        self.cubees[slice[2]] = self.cubees[slice[8]]
        self.cubees[slice[8]] = self.cubees[slice[6]]
        self.cubees[slice[6]] = tmp

        tmp = self.cubees[slice[1]]
        self.cubees[slice[1]] = self.cubees[slice[5]]
        self.cubees[slice[5]] = self.cubees[slice[7]]
        self.cubees[slice[7]] = self.cubees[slice[3]]
        self.cubees[slice[3]] = tmp


    def _turn(self, slice, turn_func, rotate_func):
        for cubee in [self.cubees[i] for i in slice]:
            getattr(cubee, turn_func)()
        rotate_func(slice)


    def turn_R(self):
        self._turn(self._slice_r, '_turn_R_LP', self._rotate_clockwise)

    def turn_R_prime(self):
        self._turn(self._slice_r, '_turn_L_RP', self._rotate_counter_clockwise)

    def turn_R2(self):
        self.turn_R()
        self.turn_R()

    def turn_L(self):
        self._turn(self._slice_l, '_turn_L_RP', self._rotate_counter_clockwise)

    def turn_L_prime(self):
        self._turn(self._slice_l, '_turn_R_LP', self._rotate_clockwise)

    def turn_L2(self):
        self.turn_L()
        self.turn_L()

    def turn_U(self):
        self._turn(self._slice_u, '_turn_U_DP', self._rotate_clockwise)

    def turn_U_prime(self):
        self._turn(self._slice_u, '_turn_D_UP', self._rotate_counter_clockwise)

    def turn_U2(self):
        self.turn_U()
        self.turn_U()

    def turn_D(self):
        self._turn(self._slice_d, '_turn_D_UP', self._rotate_counter_clockwise)

    def turn_D_prime(self):
        self._turn(self._slice_d, '_turn_U_DP', self._rotate_clockwise)

    def turn_D2(self):
        self.turn_D()
        self.turn_D()

    def turn_F(self):
        self._turn(self._slice_f, '_turn_F_BP', self._rotate_clockwise)

    def turn_F_prime(self):
        self._turn(self._slice_f, '_turn_B_FP', self._rotate_counter_clockwise)

    def turn_F2(self):
        self.turn_F()
        self.turn_F()

    def turn_B(self):
        self._turn(self._slice_b, '_turn_B_FP', self._rotate_clockwise)

    def turn_B_prime(self):
        self._turn(self._slice_b, '_turn_F_BP', self._rotate_counter_clockwise)

    def turn_B2(self):
        self.turn_B()
        self.turn_B()


    def execute(self, turns: str):
        turns = turns.split(' ')
        for turn in turns:
            self.turn_map[turn]()
