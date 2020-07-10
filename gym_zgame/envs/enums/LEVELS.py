from enum import IntEnum
import random
import warnings


class LEVELS(IntEnum):
    NONE = 0
    FEW = 1
    MANY = 2

    @staticmethod
    def print():
        for level in LEVELS:
            print('{0} -> {1}'.format(level.value, level.name))

    @classmethod
    def get_random(cls):
        return random.choice(list(LEVELS))

    @staticmethod
    def get_value_from_string(level):
        if level.upper() == 'NONE':
            return LEVELS.NONE.value
        elif level.upper() == 'FEW':
            return LEVELS.FEW.value
        elif level.upper() == 'MANY':
            return LEVELS.MANY.value
        else:
            warnings.warn('Tried to convert string ({}) to LEVELS enum and failed; returned NONE'.format(level))
            return LEVELS.NONE.value

    @staticmethod
    def get_name_from_string(level):
        if level.upper() == 'NONE':
            return LEVELS.NONE.name
        elif level.upper() == 'FEW':
            return LEVELS.FEW.name
        elif level.upper() == 'MANY':
            return LEVELS.MANY.name
        else:
            warnings.warn('Tried to convert string ({}) to LEVELS enum and failed; returned NONE'.format(level))
            return LEVELS.NONE.name
