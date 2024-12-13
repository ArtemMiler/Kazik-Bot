from Logic import Symbols
from .SlotSpin import ROWS, COLS, MIN_BONUS_QUANTITY

def fill_empty():
    return [["✖️" for _ in range(COLS)] for _ in range(ROWS)]

WILD = Symbols.WILD.emoji
BONUS = Symbols.BONUS.emoji

class SlotCheck:
    __coll_number = 2
    __dict_for_symbols = {}

    def __init__(self):
        self.__ways = 0
        self.__win_slot = fill_empty()
        self.__dict_for_rows = {}

    @property
    def win_slot(self):
        return self.__win_slot

    @property
    def ways(self):
        return self.__ways

    @property
    def dict_for_rows(self):
        return self.__dict_for_rows

    def __str__(self):
        return '\n'.join('|' + '|'.join(map(str, row)) + '|' for row in self.__win_slot)

    def check_win(self, spin):
        for i in range(ROWS):
            for k in range(-1, 2):
                if 0 <= i + k < ROWS:
                    for n in range(-1, 2):
                        if 0 <= i + n < ROWS:
                            if spin[i][1] != BONUS and spin[i + k][0] != BONUS and spin[i + n][2] != BONUS:
                                win_conditions = [
                                    spin[i][1] == spin[i + k][0] and spin[i + n][2] == WILD,
                                    spin[i][1] == spin[i + n][2] and spin[i + k][0] == WILD,
                                    spin[i][1] == WILD and spin[i + k][0] == WILD,
                                    spin[i][1] == WILD and spin[i + n][2] == WILD,
                                    spin[i][1] == spin[i + k][0] == spin[i + n][2],
                                    spin[i + k][0] == WILD and spin[i + n][2] == WILD,
                                    spin[i][1] == WILD and spin[i + k][0] == spin[i + n][2],
                                ]

                                if any(win_conditions):
                                    self.__add_element(i, n, k, spin)

        if self.__ways > 0:
            self.__check_more_lines(spin)
            self.check_bonus(spin)
        return self.__ways

    def __add_element(self, o, m, l, slot):
        self.__ways += 1

        self.__win_slot[o][1] = slot[o][1]
        self.__win_slot[o + l][0] = slot[o + l][0]
        self.__win_slot[o + m][2] = slot[o + m][2]

        symbols_to_check = [slot[o + m][2], slot[o][1], slot[o + l][0]]
        all_wild = all(symbol == WILD for symbol in symbols_to_check)

        symbol_to_add = WILD if all_wild else next((symbol for symbol in symbols_to_check if symbol != WILD), None)

        if symbol_to_add not in self.__dict_for_symbols:
            self.__dict_for_symbols[symbol_to_add] = []
        self.__dict_for_symbols[symbol_to_add].append([o + m, self.__coll_number])
        if symbol_to_add not in self.__dict_for_rows:
            self.__dict_for_rows[symbol_to_add] = []
        self.__dict_for_rows[symbol_to_add].append(self.__coll_number)

    def __check_more_lines(self, slot):
        self.__coll_number += 1
        if self.__coll_number >= COLS:
            return

        dict_copy = {key: value[:] for key, value in self.__dict_for_symbols.items()}
        temp_dict = {}

        for symbol, coordinates in dict_copy.items():
            for value, coordinate_coll in coordinates:
                if coordinate_coll != self.__coll_number - 1:
                    continue

                for k in range(-1, 2):
                    if not (0 <= value + k < len(slot)):
                        continue

                    current_value = slot[value + k][self.__coll_number]
                    is_wild = current_value == WILD
                    is_bonus = current_value == BONUS

                    if symbol != WILD:
                        if symbol == current_value or is_wild:
                            self.win_slot[value + k][self.__coll_number] = current_value
                            temp_dict.setdefault(symbol, []).append((value + k, self.__coll_number))

                            self.__dict_for_rows[symbol].append(self.__coll_number)
                            if self.__coll_number - 1 in self.__dict_for_rows[symbol]:
                                self.__dict_for_rows[symbol].remove(self.__coll_number - 1)
                    else:
                        self.win_slot[value + k][self.__coll_number] = current_value
                        if is_wild:
                            temp_dict.setdefault(symbol, []).append((value + k, self.__coll_number))
                        elif not is_bonus:
                            temp_dict.setdefault(current_value, []).append((value + k, self.__coll_number))

                            if current_value not in self.__dict_for_rows:
                                self.__dict_for_rows[current_value] = []
                            self.__dict_for_rows[current_value].append(self.__coll_number)

        for symbol, new_coordinates in temp_dict.items():
            self.__dict_for_symbols.setdefault(symbol, []).extend(new_coordinates)

        self.__check_more_lines(slot)
        self.__ways = sum(len(values) for values in self.__dict_for_rows.values())

    def check_bonus(self, slot):
        bonus_count = sum(row.count(BONUS) for row in slot)

        if bonus_count >= MIN_BONUS_QUANTITY:
            for i in range(ROWS):
                for j in range(COLS):
                    if slot[i][j] == BONUS:
                        self.__win_slot[i][j] = BONUS
            return self.__win_slot, bonus_count
