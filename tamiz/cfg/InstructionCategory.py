from enum import Enum

class InstructionCategory(Enum):
    DATA_TRANSFER = 1
    ARITHMETIC = 2
    LOGICAL = 3
    STRING = 4
    OTHER = 5
