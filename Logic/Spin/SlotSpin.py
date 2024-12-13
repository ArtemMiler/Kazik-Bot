import random
from Logic import Symbols

ROWS = 3
COLS = 5
MAX_BONUS_QUANTITY = 5
MIN_BONUS_QUANTITY = 3

BONUS = Symbols.BONUS.emoji

class SlotSpin:
    def __init__(self):
        self.__slot = self.__generate_slot()

    def __generate_slot(self):
        while True:
            slot = [[next(self.__fill_slot()) for _ in range(COLS)] for _ in range(ROWS)]
            bonus_count = sum(row.count(BONUS) for row in slot)
            if bonus_count <= MAX_BONUS_QUANTITY:
                return slot

    def __str__(self):
        return '\n'.join('|' + '|'.join(row) + '|' for row in self.__slot)

    @property
    def get_slot(self):
        return self.__slot

    @staticmethod
    def __fill_slot():
        while True:
            rand_num = random.uniform(0, Symbols.total_probability())
            for symbol in Symbols:
                rand_num -= symbol.probability
                if rand_num <= 0:
                    yield symbol.emoji
                    break
            else:
                yield Symbols.SPADES.emoji
