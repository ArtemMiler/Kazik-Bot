from decimal import Decimal

from Logic.Settings.validations import Sym


class WinCount:
    __total_win = 0
    __one_win = 0
    __bet = 0

    def __init__(self, bet):
        self.__bet = float(bet)

    @property
    def total_win(self):
        return self.__total_win
    @property
    def bet(self):
        return self.__bet

    def count_win(self, check):
        def find_symbol(_symbol):
            return next(sym for sym in Sym.values() if sym["emoji"] == _symbol)

        if check.ways:
            for symbol, lines in check.dict_for_rows.items():
                price = Decimal(str(find_symbol(symbol)["price"]))
                for line in lines:
                    self.__one_win = Decimal(0)
                    self.__one_win = Decimal(self.__bet) * price * Decimal(line) ** 2
                    self.__total_win += self.__one_win
        return self.__total_win
