import random

from Logic import Symbols

ROWS = 3
COLS = 5
MAX_BONUS_QUANTITY = 5
MIN_BONUS_QUANTITY = 3

# if not isinstance(ROWS, int) or ROWS <= 0:
#     raise ValueError("ROWS должно быть целым числом больше 0.")
# if not isinstance(COLS, int) or COLS < 3:
#     raise ValueError("COLS должно быть целым числом больше 3.")
# if not isinstance(MIN_BONUS_QUANTITY, int) or MIN_BONUS_QUANTITY <= 0:
#     raise ValueError("MIN_BONUS_QUANTITY должно быть целым числом больше 0.")
# if not isinstance(MAX_BONUS_QUANTITY, int) or MAX_BONUS_QUANTITY != MIN_BONUS_QUANTITY + 2:
#     raise ValueError("MAX_BONUS_QUANTITY должно быть целым числом, равным MIN_BONUS_QUANTITY + 2.")

BONUS = Symbols.BONUS.emoji
WILD = Symbols.WILD.emoji


class SlotSpin:
    coordinate = []

    def __init__(self, bonus=False):
        self.__slot = self.__generate_slot(bonus)

    def __str__(self):
        return '\n'.join('|' + '|'.join(row) + '|' for row in self.__slot)

    @property
    def slot(self):
        return self.__slot

    @staticmethod
    def delete_coordinate():
        SlotSpin.coordinate = []

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

    def __generate_slot(self, is_super_bonus=False):
        while True:
            slot = [[next(self.__fill_slot()) for _ in range(COLS)] for _ in range(ROWS)]

            if sum(row.count(BONUS) for row in slot) <= MAX_BONUS_QUANTITY:
                if is_super_bonus:
                    self.coordinate = [(row, coll) for row in range(ROWS) for coll in range(COLS)
                                       if slot[row][coll] == WILD]
                    for row, coll in self.coordinate:
                        slot[row][coll] = WILD
                return slot
