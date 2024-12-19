from Logic import Symbols


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

    @property
    def bet(self):
        return self.__bet

    def count_win(self, check):

        def find_symbol(_symbol):
            return next((element for element in Symbols if element.emoji == _symbol))

        if check.ways:
            for symbol, lines in check.dict_for_rows.items():
                price = find_symbol(symbol).price
                for line in lines:
                    self.__one_win = 0
                    self.__one_win += self.__bet * price * line ** 2
                    self.__total_win += self.__one_win

        self.__x_win = self.__total_win / self.__bet
        print(f"\nWin: {self.__total_win}")

        return self.__total_win, self.__x_win
