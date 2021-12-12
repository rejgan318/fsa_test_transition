""" Простейший конечный автомат """
from transitions import Machine, State
from enum import Enum, auto
import logging
import time

class AbcClass(object):
    def __init__(self):
        self.symbol = 'а'

    def input(self):
        self.symbol = input('Один символ и Enter (Q - выход):')
        self.symbol = self.symbol[0]

    def output(self):
        print(f'Обработан символ {self.symbol=}')
        if self.symbol == 'q':
            self.finish()

    def c_upper(self):
        return self.symbol[0].isupper()

    def tolower(self):
        print(f'Уменьшаем "{self.symbol}" -> "{self.symbol.lower()}"')
        self.symbol = self.symbol.lower()

    def poll(self):
        while not abc_o.is_FINISH():
            trs = abc_m.get_triggers(abc_o.state)
            print(f'Текущее состояние {abc_o.state=}, переход {trs[0]}')
            abc_o.trigger(trs[0])
            # time.sleep(0.2)


class States(Enum):
    INIT = auto()
    INPUT = auto()
    PROCESS = auto()
    UPPER = auto()
    OUTPUT = auto()
    FINISH = auto()


if __name__ == '__main__':

    # logging.basicConfig(level=logging.DEBUG)
    logging.basicConfig(level=logging.WARNING)
    abc_o = AbcClass()
    abc_m = Machine(model=abc_o, states=States, initial=States.INIT,
                    ignore_invalid_triggers=True, auto_transitions=False)
    abc_m.add_transition('ii', States.INIT, States.INPUT)
    abc_m.add_transition('ip', States.INPUT, States.PROCESS)
    abc_m.add_transition('po', States.PROCESS, States.UPPER, conditions='c_upper')
    abc_m.add_transition('po', States.PROCESS, States.OUTPUT)
    abc_m.add_transition('uo', States.UPPER, States.OUTPUT)
    abc_m.add_transition('oi', States.OUTPUT, States.INPUT)
    abc_m.add_transition('finish', '*', States.FINISH)
    abc_m.on_enter_INPUT('input')
    abc_m.on_enter_OUTPUT('output')
    abc_m.on_enter_UPPER('tolower')

    abc_o.ii()
    abc_o.poll()

    print('Done.')
