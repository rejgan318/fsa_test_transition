""" Простейший конечный автомат """
from transitions import Machine, State
from enum import Enum, auto
import logging

class AbcClass(object):
    def __init__(self):
        self.symbol = 'а'

    def input(self):
        print('inputting....')
        self.symbol = input('Один символ и Enter:')
        self.symbol = self.symbol[0]

    def output(self):
        print(f'символ {self.symbol=}')


class States(Enum):
    INPUT = auto()
    PROCESS = auto()
    OUTPUT = auto()


if __name__ == '__main__':

    logging.basicConfig(level=logging.DEBUG)
    abc_o = AbcClass()
    abc_m = Machine(model=abc_o, states=States, initial=States.INPUT)
    abc_m.add_transition('ip', States.INPUT, States.PROCESS)
    abc_m.add_transition('po', States.PROCESS, States.OUTPUT)
    abc_m.add_transition('oi', States.OUTPUT, States.INPUT)
    abc_m.on_enter_INPUT('input')
    # abc_m.on_enter_PROCESS('ouput')
    # abc_m.on_enter_INPUT('input')
    # abc_m.on_enter_PROCESS('ouput')
    abc_m.on_enter_OUTPUT('output')

    print('Done.')
