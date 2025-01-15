import copy
from itertools import product

from Logic.Settings.validations import (COLS, EMPTY, MIN_BONUS_QUANTITY, ROWS,
                                        Sym)

WILD = Sym.get("WILD").get("emoji")
BONUS = Sym.get("BONUS").get("emoji")


def fill_empty():
    return [[EMPTY for _ in range(COLS)] for _ in range(ROWS)]


class SlotCheck:
    def __init__(self):
        self.__coll_number = 2
        self.__ways = 0
        self.__dict_for_symbols = {}
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

    def check_win(self, spin):
        self.__reset()

        def is_win_condition(_i, _k, _n):
            conditions = [
                spin[_i][1] == spin[_i + _k][0] and spin[_i + _n][2] == WILD,
                spin[_i][1] == spin[_i + _n][2] and spin[_i + _k][0] == WILD,
                spin[_i][1] == spin[_i + _k][0] == WILD,
                spin[_i][1] == spin[_i + _n][2] == WILD,
                spin[_i][1] == spin[_i + _k][0] == spin[_i + _n][2],
                spin[_i + _k][0] == spin[_i + _n][2] == WILD,
                spin[_i][1] == WILD and spin[_i + _k][0] == spin[_i + _n][2],
            ]
            return any(conditions)

        for i, k, n in product(range(ROWS), range(-1, 2), range(-1, 2)):
            if 0 <= i + k < ROWS and 0 <= i + n < ROWS:
                if not any(spin[i + offset][column] == BONUS for offset, column in [(0, 1), (k, 0), (n, 2)]):
                    if is_win_condition(i, k, n):
                        self.__add_element(i, n, k, spin)

        if self.__ways > 0:
            self.__check_more_lines(spin)

        self.check_bonus(spin)
        return self.__ways

    def check_bonus(self, slot, check_only=False):
        bonus_count = sum(row.count(BONUS) for row in slot)

        if bonus_count >= MIN_BONUS_QUANTITY:
            if not check_only:
                for i in range(ROWS):
                    for j in range(COLS):
                        if slot[i][j] == BONUS:
                            self.__win_slot[i][j] = BONUS
                return self.__win_slot, bonus_count
            return bonus_count
        return 0

    def __add_element(self, _i, _n, _k, slot):
        self.__ways += 1

        for offset, column in [(_i, 1), (_i + _k, 0), (_i + _n, 2)]:
            self.__win_slot[offset][column] = slot[offset][column]

        symbols_to_check = [slot[_i + _n][2], slot[_i][1], slot[_i + _k][0]]
        symbol_to_add = (
            WILD if all(symbol == WILD for symbol in symbols_to_check)
            else next((symbol for symbol in symbols_to_check if symbol != WILD), None)
        )

        self.__dict_for_symbols.setdefault(symbol_to_add, []).append([_i + _n, self.__coll_number])
        self.__dict_for_rows.setdefault(symbol_to_add, []).append(self.__coll_number)

    def __reset(self):
        self.__dict_for_rows = {}
        self.__coll_number = 2
        self.__dict_for_symbols = {}
        self.__ways = 0
        self.__win_slot = fill_empty()

    def __check_more_lines(self, slot):
        self.__coll_number += 1
        if self.__coll_number >= COLS:
            return

        dict_copy = copy.deepcopy(self.__dict_for_symbols)
        temp_dict = {}

        def process_coordinate(_symbol, _value, _k, _temp_dict):
            next_value = _value + _k
            if not (0 <= next_value < ROWS):
                return

            current_cell = slot[next_value][self.__coll_number]
            if _symbol == current_cell or current_cell == WILD:
                self.win_slot[next_value][self.__coll_number] = current_cell
                _temp_dict.setdefault(_symbol, []).append((next_value, self.__coll_number))
                update_dict_for_rows(_symbol, self.__coll_number)
            elif current_cell != WILD and _symbol == WILD:

                if current_cell != BONUS:
                    self.win_slot[next_value][self.__coll_number] = current_cell
                    _temp_dict.setdefault(current_cell, []).append((next_value, self.__coll_number))
                    update_dict_for_rows(current_cell, self.__coll_number)

        def update_dict_for_rows(_symbol, coll):
            self.__dict_for_rows.setdefault(_symbol, [])
            self.__dict_for_rows[_symbol].append(coll)
            if coll - 1 in self.__dict_for_rows[_symbol]:
                self.__dict_for_rows[_symbol].remove(coll - 1)

        def remove_wilds():
            if WILD in self.__dict_for_rows:
                self.__dict_for_rows[WILD] = [row for row in self.__dict_for_rows[WILD] if row >= COLS - 1]
                if not self.__dict_for_rows[WILD]:
                    del self.__dict_for_rows[WILD]

        for symbol, coordinates in dict_copy.items():
            for value, coordinate_coll in coordinates:
                if coordinate_coll != self.__coll_number - 1:
                    continue
                for k in range(-1, 2):
                    process_coordinate(symbol, value, k, temp_dict)

        for symbol, new_coordinates in temp_dict.items():
            self.__dict_for_symbols.setdefault(symbol, []).extend(new_coordinates)
        remove_wilds()
        self.__check_more_lines(slot)
        self.__ways = sum(len(values) for values in self.__dict_for_rows.values())

