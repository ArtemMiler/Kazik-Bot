import random

from Logic.Settings.validations import *

WILD = Sym.get("WILD").get("emoji")
BONUS = Sym.get("BONUS").get("emoji")


class SlotSpin:

    def __init__(self, coordinate=None):
        self.__coordinate = coordinate if coordinate else set()
        self.__slot = self.__generate_slot()

    @property
    def slot(self):
        return self.__slot

    @property
    def coordinate(self):
        return self.__coordinate

    @staticmethod
    def __fill_slot():
        while True:
            rand_num = random.uniform(0, total_probability)
            for _, symbol in Sym.items():
                rand_num -= symbol.get("probability")
                if rand_num <= 0:
                    yield symbol.get("emoji")
                    break

    def __generate_slot(self):
        while True:
            slot = [[next(self.__fill_slot()) for _ in range(COLS)] for _ in range(ROWS)]
            if sum(row.count(BONUS) for row in slot) <= MAX_BONUS_QUANTITY:
                return slot

    def coordinate_update(self):
        self.__coordinate.update(
            (row, coll)
            for row in range(ROWS)
            for coll in range(COLS)
            if self.__slot[row][coll] == WILD
        )

        for row, coll in self.__coordinate:
            self.__slot[row][coll] = WILD
