"""
Обработка серий сигнал с помощью конечных автоматов
"""

import enum
from pathlib import Path
from transitions import Machine


class States(enum.Enum):
    SIGNAL = enum.auto()
    # NULL = enum.auto()
    PAUSE = enum.auto()
    BEGIN = enum.auto()


class Series(object):

    def __init__(self, s: list, empty_len: int = 0):
        self.s = s
        self.empty = empty_len
        self.series: list = []  # найденные серии
        self.begin: int = 0  # начало серии
        self.i: int = None
        self.n = len(self.s)
        self.type_series = None
        self.machine = Machine(model=self, states=States, initial=States.BEGIN)
        self.machine.add_transition('bs', States.BEGIN, States.SIGNAL)
        self.machine.add_transition('bp', States.BEGIN, States.PAUSE)
        self.machine.add_transition('pp', States.PAUSE, States.PAUSE)
        self.machine.add_transition('ss', States.SIGNAL, States.SIGNAL)
        self.machine.add_transition('ps', States.PAUSE, States.SIGNAL)
        self.machine.add_transition('sp', States.SIGNAL, States.PAUSE)

    def to_dict(self, start, end, type_series):
        duration = end - start + 1
        return {
            'type': type_series.name,
            'start': start,
            'end': end,
            'duration': duration,
        }

    def from_dict(self, d: dict):

        class DictSeries(object):
            def __init__(self, start=None, end=None, type_series=None):
                self.start = start
                self.end = end
                self.type_series = type_series

        saved_series = DictSeries(start=d['start'], end=d['end'], type_series=d['type'])
        return saved_series


    def get_series(self, empty_len: int = 0):

        for i, e in enumerate(self.s):
            state = self.state
            last_point = (i == self.n - 1)

            if state == States.BEGIN:
                self.begin = 0
                if e == 0:
                    self.bp()
                else:
                    self.bs()
                if last_point:  # и единственная
                    self.series.append(self.to_dict(0, 0, States.PAUSE if e == 0 else States.SIGNAL))

            elif state == States.SIGNAL:
                if e == 0 or last_point:
                    self.sp()
                    self.series.append(self.to_dict(self.begin, self.i + (1 if last_point else 0), States.SIGNAL))
                    self.begin = i + 1

            elif state == States.PAUSE:
                big_pause = self.i - self.begin >= empty_len
                # self.series.append(self.to_dict(self.begin, self.i + (1 if last_point else 0), States.PAUSE))
                if last_point:  # для последней точки либо просто сохраним паузу, если она достаточной длины...
                    if big_pause:
                        self.series.append(self.to_dict(self.begin, self.i + 1, States.PAUSE))
                    elif self.series:   # ...либо присоеденим короткую фаузу к предыдущему сигналу, а потом сохраним,
                                        # изменив правую границу последнего сигнала, если он есть
                        prev_signal = self.from_dict(self.series.pop())
                        self.series.append(self.to_dict(prev_signal.start, self.i + 1, States.PAUSE))
                elif e != 0:
                    if big_pause:
                        self.series.append(self.to_dict(self.begin, self.i, States.PAUSE))
                    elif self.series:
                        prev_signal = self.from_dict(self.series.pop())
                        self.series.append(self.to_dict(prev_signal.start, self.i, States.PAUSE))
                    else:
                        self.series.append(self.to_dict(0, self.i, States.PAUSE))

                    self.ps()
                    self.begin = i + 1

            print(f'{i}: {e}  {state.name[0]} --> {self.state.name[0]}')
            self.i = i
        return self.series


if __name__ == '__main__':
    wav_file = 'test.wav'
    wf = Path(wav_file)
    test = [1, 1, 0]
    series = Series(test, empty_len=0)
    s = series.get_series()
    print(test)
    for e in s:
        print(f"{e['type'][0]} {e['start']:2} {e['end']:2}  {e['duration']}")
    print('\nDone.')
