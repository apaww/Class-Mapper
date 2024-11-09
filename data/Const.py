# Constants

from typing import LiteralString


SEX: list[str] = ['мужской', 'женский']
GROUPS: list[LiteralString] = 'Промробоквантум, Геоквантум, Энерджиквантум, VR/ARквантум, Аэроквантум, Мультимедиа, Основы цифровых технологий, Шахматы, Математика, Английский'.split(', ')
DIFFICULTIES: list[str] = ['вводный', 'углубленный', 'проектный']
RUSSIAN: list[LiteralString] = '«а», «б», «в», «г», «д», «е», «ё», «ж», «з», «и», «й», «к», «л», «м», «н», «о», «п», «р», «с», «т», «у», «ф», «х», «ц», «ч», «ш», «щ», «ъ», «ы», «ь», «э», «ю», «я»'.upper().replace('«', '').replace('»', '').split(', ')
NUMBERS: list[LiteralString] = '1 2 3 4 5 6 7 8 9 0'.split()