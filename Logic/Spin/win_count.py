from decimal import Decimal

from Logic.Settings.validations import Sym


class WinCount:

    def __init__(self, bet):
        self.__bet = Decimal(str(bet))
        self.__total_win = 0
        self.__one_win = 0

    @property
    def total_win(self):
        return self.__total_win

    def count_win(self, check):
        if check.ways:
            for symbol, lines in check.dict_for_rows.items():
                price = Decimal(str(self.__find_symbol(symbol)["price"]))
                for line in lines:
                    self.__one_win = Decimal(0)
                    self.__one_win = self.__bet * price * Decimal(line) ** 2
                    self.__total_win += self.__one_win
        return self.__total_win

    @staticmethod
    def __find_symbol(symbol):
        return next(sym for sym in Sym.values() if sym["emoji"] == symbol)
