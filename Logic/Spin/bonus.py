import random
from decimal import Decimal

from Logic.Settings.validations import (FS_BONUS, FS_MEGA, FS_SUPER,
                                        MIN_BONUS_QUANTITY, POSITION_RANGES,
                                        QUANTITY_RANGES, ROWS, Sym)

from .slot_check import SlotCheck
from .slot_spin import SlotSpin
from .win_count import WinCount


class Bonus:
    __win_total = 0
    __x_win = 0
    __free_spins = 0

    def __init__(self, slot, bet):
        self.__win_total = 0
        self.__x_win = 0
        self.__free_spins = 0
        self.slot = slot

        result = SlotCheck().check_bonus(slot, True)
        if result is None:
            return

        actions = {
            0: (self.play_bonus, "=" * 66),
            1: (self.play_super_bonus, "*" * 66),
            2: (self.play_mega_bonus, "#" * 66),
        }

        action = actions.get(result - MIN_BONUS_QUANTITY)
        if action:
            print(action[1])
            action[0](bet)
            print(action[1])

    @staticmethod
    def __random_value(ranges):
        random_value = random.uniform(0, 10)
        return next(value for start, end, value in ranges if start <= random_value <= end)

    def play_bonus(self, bet):
        return self.__play(bet, FS_BONUS, lambda: SlotSpin(bonus=True), True)

    def play_super_bonus(self, bet):
        return self.__play(bet, FS_SUPER, self.__generate_super_bonus_spin)

    def play_mega_bonus(self, bet):
        SlotSpin.delete_coordinate()
        result = self.__play(bet, FS_MEGA, lambda: SlotSpin(bonus=True, super_bonus=True))
        return result

    def __play(self, bet, fs, spin_generator, count=False):
        self.__free_spins = fs
        temp_win = 0
        while self.__free_spins > 0:
            temp_win = self.__process_spin(spin_generator(), bet, temp_win, count)
        print(f"\nTotal win: {self.__win_total}")
        self.__x_win = self.__win_total / Decimal(bet)
        return self.__win_total, self.__x_win

    def __process_spin(self, my_spin, bet, temp_win, count=False):
        print(my_spin)

        check = SlotCheck()
        check.check_win(my_spin.slot)
        print(f"\n{check}")
        print(f"\nWays: {check.ways}")

        my_win = WinCount(bet)
        new_win = my_win.count_win(check)
        self.__free_spins += check.check_bonus(my_spin.slot, True) - 1
        if count:
            temp_win = max(temp_win, new_win)
            print(f"Temp win: {temp_win}")
            self.__win_total += temp_win
        else:
            self.__win_total += my_win.total_win

        print(f"\nFree spins: {self.__free_spins}")
        return temp_win

    def __generate_super_bonus_spin(self):
        my_spin = SlotSpin(bonus=True)
        quantity = self.__random_value(QUANTITY_RANGES)
        for _ in range(quantity):
            position = self.__random_value(POSITION_RANGES)
            for row in range(ROWS):
                my_spin.slot[row][position] = Sym.get("WILD").get("emoji")
        return my_spin
