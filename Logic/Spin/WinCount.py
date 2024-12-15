from Logic import Symbols

from .SlotCheck import SlotCheck


class WinCount:
    __total_win = 0
    __one_win = 0
    __x_win = 0
    __bet = 0

    def __init__(self, bet):
        self.__bet = float(bet)

    @property
    def total_win(self):
        return self.__total_win

    @property
    def x_win(self):
        return self.__x_win

    def count_win(self, slot):
        check = SlotCheck()
        check.check_win(slot)
        print(f"\n{check}")
        print(f"\nWays: {check.ways}")
        print(f"\n{check.dict_for_rows}")

        def find_symbol(_symbol):
            for element in Symbols:
                if element.emoji == _symbol:
                    return element

        if SlotCheck.ways:
            for symbol, lines in check.dict_for_rows.items():
                price = find_symbol(symbol).price
                for line in lines:
                    self.__one_win = 0
                    self.__one_win += self.__bet * price * line ** 2
                    self.__total_win += self.__one_win

        self.__x_win = self.__total_win / self.__bet
        print(f"\nTotal win: {self.__total_win}")
        print(f"\nX win: {self.__x_win}")

        return self.__total_win, self.__x_win
