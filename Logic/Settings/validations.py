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

    @classmethod
    @field_validator("MAX_BONUS_QUANTITY")
    def validate_bonus_quantity(cls, value, values):
        if value != values["MIN_BONUS_QUANTITY"] + 2:
            raise ValueError("MAX_BONUS_QUANTITY must be 2 more than MIN_BONUS_QUANTITY.")
        return value

    @classmethod
    @field_validator("QUANTITY_RANGES")
    def validate_quantity_ranges(cls, value, values):
        if len(value) > values["COLS"]:
            raise ValueError("QUANTITY_RANGES length must be <= COLS.")
        for range_set in value:
            if any(val < 0 for val in range_set):
                raise ValueError("All values in QUANTITY_RANGES must be >= 0.")
        return value

    @classmethod
    @field_validator("POSITION_RANGES")
    def validate_position_ranges(cls, value, values):
        if len(value) != values["COLS"]:
            raise ValueError("POSITION_RANGES length must equal COLS.")
        for range_set in value:
            if any(val < 0 for val in range_set):
                raise ValueError("All values in POSITION_RANGES must be >= 0.")
        return value

    @classmethod
    @field_validator("Symbols")
    def validate_symbols(cls, value):
        required_symbols = {"WILD", "BONUS"}
        if not required_symbols.issubset(value.keys()):
            raise ValueError(f"Symbols must include {', '.join(required_symbols)}.")
        return value


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
    total_probability = sum(symbol["probability"] for symbol in Sym.values())
except ValueError as e:
    raise ValueError(f"Validation error: {e}") from e
except KeyError as e:
    raise KeyError(f"Missing required key in data: {e}") from e
