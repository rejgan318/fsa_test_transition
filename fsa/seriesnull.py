"""
Обработка серий сигнал с помощью конечных автоматов
"""

import enum
from pathlib import Path
from transitions import Machine


class States(enum.Enum):
    SIGNAL = enum.auto()
    NULL = enum.auto()
    PAUSE = enum.auto()
    BEGIN = enum.auto()


class Series(object):

    def __init__(self, s: list, empty_len: int = 0):
        self.s = s
        self.empty = empty_len
        self.series: list = []  # найденные серии
        self.begin: int = None  # начало серии
        self.i: int = None
        self.n = len(self.s)
        self.type_series = None
        self.machine = Machine(model=self, states=States, initial=States.BEGIN)
        self.machine.add_transition('bs', States.BEGIN, States.SIGNAL)
        self.machine.add_transition('bn', States.BEGIN, States.NULL)
        self.machine.add_transition('nn', States.NULL, States.NULL)
        self.machine.add_transition('np', States.NULL, States.PAUSE)
        self.machine.add_transition('ns', States.NULL, States.SIGNAL)
        self.machine.add_transition('ps', States.PAUSE, States.SIGNAL)
        self.machine.add_transition('sn', States.SIGNAL, States.NULL)

    def to_dict(self, start, end, type_series):
        duration = end - start + 1
        return {
            'type': type_series.name,
            'start': start,
            'end': end,
            'duration': duration,
        }

    def get_series(self, empty_len: int = 0):

        for i, e in enumerate(self.s):
            state = self.state
            last_point = i == self.n - 1
            if state == States.BEGIN:
                self.begin = 0
                if e == 0:
                    self.bn()
                    self.type_series = States.NULL
                else:
                    self.bs()
                    self.type_series = States.SIGNAL
            elif state == States.SIGNAL:
                if e == 0 or last_point:
                    self.sn()
                    self.type_series = States.NULL
                    self.series.append(self.to_dict(self.begin, self.i + (1 if last_point else 0), States.SIGNAL))
                    self.begin = self.i + 1
            elif state == States.NULL:  # fixme и последняя точка
                if e != 0:
                    # todo прицепить к предыдущему сигналу
                    self.ns()
                else:
                    if self.i - self.begin >= self.empty:
                        self.np()
            elif state == States.PAUSE:
                if e != 0 or last_point:
                    self.ps()
                    self.series.append(self.to_dict(self.begin, self.i + (1 if last_point else 0), States.PAUSE))
                    self.begin = self.i + 1

            print(f'{i}: {e}  {state.name[0]} --> {self.state.name[0]}')
            self.i = i
        return self.series


if __name__ == '__main__':
    wav_file = 'test.wav'
    wf = Path(wav_file)
    test = [1, 0,  1]
    series = Series(test, empty_len=0)
    s = series.get_series()
    print(test)
    for e in s:
        print(f"{e['type'][0]} {e['start']:2} {e['end']:2}  {e['duration']}")
    print('\nDone.')
