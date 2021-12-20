""" Простейший конечный автомат """
from enum import Enum, auto

import logging
from loguru import logger
from transitions import Machine


class States(Enum):
    s001Begin = auto()
    s010GetData = auto()
    s020Analize = auto()
    s030SaveSeries = auto()
    s999Finish = auto()


class Signal(Enum):
    SIGNAL = auto()
    PAUSE = auto()
    NULL = auto()

class Fsa(object):

    def __init__(self, signal):

        self.signal = signal
        self.i = -1  # позиция входных данных
        self.x = None  # текущий элемент данных
        self.n = len(signal)
        self.early: Signal = None   # тип сигнала на прошлом шаге
        self.current: Signal = None   # тип сигнала на текущем шаге

        self.last_item = self.n - 1
        self.result = []

        self.machine = Machine(model=self, states=States, initial=States.s001Begin,
                               auto_transitions=False)
        self.machine.add_transition('t001', States.s001Begin, States.s010GetData)
        self.machine.add_transition('t010', States.s010GetData, States.s999Finish, conditions=self.nodata)
        self.machine.add_transition('t010', States.s010GetData, States.s020Analize)
        self.machine.add_transition('t020', States.s020Analize, States.s030SaveSeries, conditions=self.needsave)
        self.machine.add_transition('t020', States.s020Analize, States.s010GetData)
        self.machine.add_transition('t030', States.s030SaveSeries, States.s010GetData)

        self.machine.on_enter_s010GetData(self.get_data)
        self.machine.on_enter_s030SaveSeries(self.save_series)

        self.poll()

    def get_data(self):
        self.i += 1     # для первого раза будет 0, т.к. при инициализации = -1
        if self.i == self.n:    # данных больше нет
            self.x = None
            return
        self.x = self.signal[self.i]
        self.early = self.current
        self.current = Signal.SIGNAL if self.x else Signal.NULL

    def nodata(self):
        return self.i == self.n

    def needsave(self):
        return not self.x == 0

    def save_series(self):
        self.result.append(self.x)

    def poll(self):
        """
        Основной движок. По единожды построенной таблице переходов сделать переход для текущего состояния.
        Используется только первое имя перехода, чтобы сиключить попутку перехода по служебным, сгенерированным,
        типа на себя. Отсяда условия - прописывать переходы для состояния только с одним именем и разными conditional
        Переходы без условий располагаются последними
        """
        # словарь переходов для всех состояний
        trs = {st: self.machine.get_triggers(st) for st in States}

        while not self.is_s999Finish():
            logger.info(f'{self.state.name:15} --> {trs[self.state][0]} ({len(trs[self.state])})')
            self.trigger(trs[self.state][0])

        return self.result


if __name__ == '__main__':
    import sys

    def get_test_list(test_string: str) -> list[int]:
        return [int(s) if s.isdigit() else 0 for s in list(test_string)]

    logger.remove()
    logger.add(sys.stdout, level='INFO')
    # logging.basicConfig(level=logging.INFO)
    # todo тесты

    result = Fsa(get_test_list('4_5__'))
    print(f'Done, {result.result=}')
