import random

from Logic import Symbols

class SpinSlot:
    ROWS = 3
    COLS = 5

    def __init__(self):
        self.slots = [[next(self.fill_slot()) for _ in range(self.COLS)] for _ in range(self.ROWS)]


    def __str__(self):
        return '\n'.join('|' + '|'.join(row) + '|' for row in self.slots)


    @classmethod
    def fill_slot(cls):
        while True:
            rand_num = random.uniform(0, Symbols.total_probability())
            for symbol in Symbols:
                rand_num -= symbol.probability
                if rand_num <= 0:
                    yield symbol.emoji
                    break
            else:
                yield Symbols.SPADES.emoji