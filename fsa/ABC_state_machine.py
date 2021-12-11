""" Простейший конечный автомат """
from transitions import Machine
from enum import Enum, auto
import logging

class AbcClass(object):
    def __init__(self):
        self.symbol = ''

    def input(self):
        self.symbol = input('Один символ и Enter:')
        self.symbol = self.symbol[0]

    def output(self):
        print(f'{self.symbol=}')

class States(Enum):
    INPUT = auto()
    PROCESS = auto()
    OUTPUT = auto()


if __name__ == '__main__':
    logging.basicConfig(level=logging.DEBUG)
    abc_o = AbcClass()
    abc_m = Machine(model=abc_o, states=States)
    abc_m.add_transition('ip', States.INPUT, States.PROCESS)
    abc_m.add_transition('po', States.PROCESS, States.OUTPUT)

    print('Done.')
