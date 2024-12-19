import random

from Logic import Symbols

from .SlotCheck import SlotCheck
from .SlotSpin import MIN_BONUS_QUANTITY, ROWS, SlotSpin
from .WinCount import WinCount

quantity_ranges = [(0, 1, 3), (1, 4, 2), (4, 10, 1)]
position_ranges = [(0, 1, 0), (1, 2, 1), (2, 4.5, 2), (4, 7, 3), (7, 10, 4)]


class Bonus:
    __win_total = 0
    __x_win = 0
    __free_spins = 0

    def __init__(self, slot, bet):
        self.__win_total = 0
        self.__x_win = 0
        self.__free_spins = 0
        self.slot = slot

        result = SlotCheck().check_bonus(slot)
        if result is None:
            return

        _, bonus = result
        actions = {
            0: (self.__play_bonus, "=" * 66),
            1: (self.__play_super_bonus, "*" * 66),
            2: (self.__play_mega_bonus, "#" * 66),
        }

        action = actions.get(bonus - MIN_BONUS_QUANTITY)
        if action:
            print(action[1])
            action[0](bet)
            print(action[1])

    @staticmethod
    def __add_fs(slot):
        result = SlotCheck().check_bonus(slot)
        return result[1] if result else 0

    @staticmethod
    def __random_value(ranges):
        random_value = random.uniform(0, 10)
        return next(value for start, end, value in ranges if start <= random_value <= end)

    def __play_bonus(self, bet):
        return self.__play(bet, lambda: SlotSpin(), True)

    def __play_super_bonus(self, bet):
        return self.__play(bet, self.__generate_super_bonus_spin)

    def __play_mega_bonus(self, bet):
        result = self.__play(bet, lambda: SlotSpin(True))
        SlotSpin.delete_coordinate()
        return result

    def __play(self, bet, spin_generator, count=False):
        self.__free_spins = 10
        temp_win = 0
        while self.__free_spins > 0:
            temp_win = self.__process_spin(spin_generator(), bet, temp_win, count)
        print(f"\nTotal win: {self.__win_total}")
        self.__x_win = self.__win_total / bet
        return self.__win_total, self.__x_win

    def __process_spin(self, my_spin, bet, temp_win, count=False):
        print(my_spin)

        check = SlotCheck()
        check.check_win(my_spin.slot)
        print(f"\n{check}")

        my_win = WinCount(bet)
        new_win, _ = my_win.count_win(check)
        self.__free_spins += self.__add_fs(my_spin.slot) - 1

        if count:
            temp_win = max(temp_win, new_win)
            print(f"Temp win: {temp_win}")
            self.__win_total += temp_win
        else:
            self.__win_total += my_win.total_win

        print(f"\nFree spins: {self.__free_spins}")
        return temp_win

    def __generate_super_bonus_spin(self):
        my_spin = SlotSpin()
        quantity = self.__random_value(quantity_ranges)
        for _ in range(quantity):
            position = self.__random_value(position_ranges)
            for row in range(ROWS):
                my_spin.slot[row][position] = Symbols.WILD.emoji
        return my_spin
