import random

from Logic.Settings.validations import (COLS, MAX_BONUS_QUANTITY, ROWS, Sym,
                                        total_probability, MIN_BONUS_QUANTITY)

WILD = Sym.get("WILD").get("emoji")
BONUS = Sym.get("BONUS").get("emoji")


class SlotSpin:
    coordinate = set()

    def __init__(self, bonus=False, super_bonus=False):
        self.__slot = self.__generate_slot(bonus, super_bonus)

    @property
    def slot(self):
        return self.__slot

    @staticmethod
    def delete_coordinate():
        SlotSpin.coordinate = set()

    @staticmethod
    def __fill_slot():
        while True:
            rand_num = random.uniform(0, total_probability)
            for _, symbol in Sym.items():
                rand_num -= symbol.get("probability")
                if rand_num <= 0:
                    yield symbol.get("emoji")
                    break

    def __generate_slot(self, is_bonus=False, is_super_bonus=False):
        while True:
            slot = [[next(self.__fill_slot()) for _ in range(COLS)] for _ in range(ROWS)]

            if sum(row.count(BONUS) for row in slot) <= MAX_BONUS_QUANTITY:
                if is_bonus and sum(row.count(BONUS) for row in slot) < MIN_BONUS_QUANTITY:
                    if random.uniform(0, 1) < 0.99:
                        while sum(row.count(BONUS) for row in slot) >= MIN_BONUS_QUANTITY:
                            slot = [[next(self.__fill_slot()) for _ in range(COLS)] for _ in range(ROWS)]
                if is_super_bonus:
                    SlotSpin.coordinate.update(
                        (row, coll)
                        for row in range(ROWS)
                        for coll in range(COLS)
                        if slot[row][coll] == WILD
                    )

                    for row, coll in SlotSpin.coordinate:
                        slot[row][coll] = WILD
                return slot
