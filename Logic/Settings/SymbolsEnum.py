from enum import Enum


class Symbols(Enum):
    SPADES = ("♠️", 12.5, 0.05)
    CLUBS = ("♣️", 12.5, 0.05)
    HEARTS = ("♥️", 12.5, 0.05)
    DIAMONDS = ("♦️", 12.5, 0.05)
    CLOVERS = ("🍀", 10.5, 0.09)
    EYES = ("🧿", 10.0, 0.11)
    CROWN = ("👑", 8.5, 0.25)
    MAGIC = ("🔮", 8.5, 0.25)
    GOLD = ("⚜️", 7.0, 0.4)
    WILD = ("🎰", 13.4, 1.4)
    BONUS = ("💎", 7.1, 0)

    def __new__(cls, emoji, probability, price):
        obj = object.__new__(cls)
        obj._value_ = emoji  # это будет значение enum
        obj.__emoji = str(emoji)
        obj.__probability = float(probability)
        obj.__price = float(price)
        return obj

    @property
    def emoji(self):
        return self.__emoji

    @property
    def probability(self):
        return self.__probability

    @property
    def price(self):
        return self.__price

    @classmethod
    def total_probability(cls):
        return sum(symbol.probability for symbol in cls)
