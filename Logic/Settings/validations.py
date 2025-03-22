import json
import os
from typing import Dict, List, Tuple

from pydantic import BaseModel, Field, field_validator


class Symbol(BaseModel):
    probability: float = Field(..., ge=0)
    price: float = Field(..., ge=0)
    emoji: str = Field(..., min_length=1)


class Settings(BaseModel):
    ROWS: int = Field(..., gt=0)
    COLS: int = Field(..., gt=2)
    MIN_BONUS_QUANTITY: int = Field(..., gt=0)
    MAX_BONUS_QUANTITY: int = Field(..., gt=0)
    FS_BONUS: int = Field(..., gt=0)
    FS_SUPER: int = Field(..., gt=0)
    FS_MEGA: int = Field(..., gt=0)
    QUANTITY_RANGES: List[Tuple[float, float, int]]
    POSITION_RANGES: List[Tuple[float, float, int]]
    EMPTY: str = Field(...)
    Symbols: Dict[str, Symbol]
    BALANCE: float = Field(..., ge=0)
    MIN_BET: float = Field(..., gt=0)
    MAX_BET: float = Field(..., gt=0)
    BONUS_PRISE: float = Field(..., gt=0)
    SUPER_BONUS_PRISE: float = Field(..., gt=0)
    MEGA_BONUS_PRISE: float = Field(..., gt=0)

    @field_validator('MAX_BET')
    def check_max_bet(cls, max_bet, info):
        min_bet = info.data.get("MIN_BET")
        if max_bet < min_bet:
            raise ValueError(f"Bonus quantity must be greater than {min_bet}")

    @field_validator("MAX_BONUS_QUANTITY")
    def check_bonus_quantity(cls, max_bonus, info):
        min_bonus = info.data.get("MIN_BONUS_QUANTITY")
        if max_bonus is not None and min_bonus is not None:
            if max_bonus != min_bonus + 2:
                raise ValueError("MAX_BONUS_QUANTITY должен быть на 2 больше MIN_BONUS_QUANTITY.")
        return max_bonus

    @field_validator("QUANTITY_RANGES")
    def check_quantity_ranges(cls, quantity_ranges, info):
        cols = info.data.get("COLS")
        if quantity_ranges is not None and cols is not None:
            if len(quantity_ranges) > cols:
                raise ValueError("QUANTITY_RANGES должен быть меньше или равен COLS.")
            for range_set in quantity_ranges:
                if any(val < 0 for val in range_set):
                    raise ValueError("Все значения в QUANTITY_RANGES должны быть >= 0.")
        return quantity_ranges

    @field_validator("POSITION_RANGES")
    def check_position_ranges(cls, position_ranges, info):
        cols = info.data.get("COLS")
        if position_ranges is not None and cols is not None:
            if len(position_ranges) != cols:
                raise ValueError("POSITION_RANGES должен иметь длину, равную COLS.")
            for range_set in position_ranges:
                if any(val < 0 for val in range_set):
                    raise ValueError("Все значения в POSITION_RANGES должны быть >= 0.")
        return position_ranges

    @field_validator("Symbols")
    def check_symbols(cls, symbols):
        required_symbols = {"WILD", "BONUS"}
        if symbols is not None:
            if not required_symbols.issubset(symbols.keys()):
                raise ValueError(f"Symbols должны содержать {', '.join(required_symbols)}.")
        return symbols


file_path = os.path.join(os.path.dirname(__file__), "settings.json")
if not os.path.exists(file_path):
    raise FileNotFoundError(f"File settings.json was not found: {file_path}")
with open(file_path, "r", encoding="utf-8") as file:
    data = json.load(file)

try:
    settings = Settings(**data)
    Sym = data["Symbols"]
    ROWS = data["ROWS"]
    COLS = data["COLS"]
    MIN_BONUS_QUANTITY = data["MIN_BONUS_QUANTITY"]
    MAX_BONUS_QUANTITY = data["MAX_BONUS_QUANTITY"]
    FS_BONUS = data["FS_BONUS"]
    FS_SUPER = data["FS_SUPER"]
    FS_MEGA = data["FS_MEGA"]
    QUANTITY_RANGES = data["QUANTITY_RANGES"]
    POSITION_RANGES = data["POSITION_RANGES"]
    EMPTY = data["EMPTY"]
    BALANCE = data["BALANCE"]
    MIN_BET = data["MIN_BET"]
    MAX_BET = data["MAX_BET"]
    total_probability = sum(symbol["probability"] for symbol in Sym.values())
    BONUS_CONDITIONALS = {
        0: FS_BONUS,
        1: FS_SUPER,
        2: FS_MEGA
    }
    BONUS_PRISE = data["BONUS_PRISE"]
    SUPER_BONUS_PRISE = data["SUPER_BONUS_PRISE"]
    MEGA_BONUS_PRISE = data["MEGA_BONUS_PRISE"]
except ValueError as e:
    raise ValueError(f"Validation error: {e}") from e
except KeyError as e:
    raise KeyError(f"Missing required key in data: {e}") from e
