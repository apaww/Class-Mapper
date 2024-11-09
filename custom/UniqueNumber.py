import random

from data.Database import getNumbers, getCodes
from data.Const import RUSSIAN, NUMBERS

def createSequence(size=2):
    TAKEN = getNumbers()
    for _ in range((len(RUSSIAN) + len(NUMBERS))**2):
        sequence = ''.join(random.choice(RUSSIAN + NUMBERS) for _ in range(size))
        if sequence not in TAKEN:
            return sequence
        
    if size == 100:
        print('Too big sequence! (./custom/uniqueNumber.py -> size of sequence is greater than 100)')
        raise ValueError
    createSequence(size=size + 1)


def createCode(size=5):
    TAKEN = getCodes()
    for _ in range((len(NUMBERS))**2):
        sequence = ''.join(random.choice(NUMBERS) for _ in range(size))
        if sequence not in TAKEN:
            return sequence
        
    if size == 100:
        print('Too big sequence! (./custom/UniqueNumber.py -> size of sequence is greater than 100)')
        raise ValueError
    createSequence(size=size + 1)