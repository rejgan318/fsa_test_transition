"""
Маленький тест на анализ строки сигнала
"""
from transitions import Machine
import enum
from rich import print


class States(enum.Enum):
    BEGIN = -1
    PAUSE = 0
    SIGNAL = 1
    NULLS = 2

signal_name = {States.BEGIN: 'B', States.PAUSE: 'P', States.SIGNAL: 'S', States.NULLS: 'N', }


class SignalString(object):
    def __init__(self, s: list[int]):
        # self.s = s  # серия
        self.i = 0  # позиция в серии
        self.type_signal = None
        self.begin = 0  # начало серии
        self.series = []

    def ser(self, end: bool = False):
        e = self.i - (0 if end else 1)
        return {
            'type': self.type_signal,
            'start': self.begin,
            'end': e,
            'duration': e - self.begin + 1,
        }

    def add_series(self, end: bool = False):
        self.series.append(self.ser(end))

    def inc(self):
        # сдвиг позиции
        self.i += 1

    def set_begin(self):
        self.begin = self.i

    def set_begin_s(self):
        self.type_signal = States.SIGNAL
        self.set_begin()
        print(f'Сохранили начало сигнала {self.begin}')

    def set_begin_p(self):
        self.type_signal = States.PAUSE
        self.set_begin()
        print(f'Сохранили начало паузы {self.begin}')


test_string = '001111022'
test = [int(i) for i in test_string]
ka = SignalString(test)
ka.machine = Machine(model=ka, states=States, initial=States.BEGIN)
ka.machine.add_transition('bp',  States.BEGIN, States.PAUSE,  after='set_begin_p')
ka.machine.add_transition('bs', States.BEGIN,  States.SIGNAL, after='set_begin_s')
ka.machine.add_transition('sp', States.SIGNAL, States.PAUSE,  after='set_begin_p')
ka.machine.add_transition('ps', States.PAUSE,  States.SIGNAL, after='set_begin_s')
ka.machine.add_transition('ss', States.SIGNAL, States.SIGNAL)
ka.machine.add_transition('pp', States.PAUSE,  States.PAUSE)

n = len(test)
for i, t in enumerate(test):

    if ka.is_BEGIN():
        # print('Начало')
        if t == 0:
            ka.bp()
        else:
            ka.bs()
    elif ka.is_SIGNAL():
        if t == 0:
            ka.add_series()
            ka.sp()
    elif ka.is_PAUSE():
        if t != 0:
            ka.add_series()
            ka.ps()
            # print('Сигнал', i)
    if i == n - 1:
        ka.add_series(end=True)
    ka.inc()

# print(ka.series)
print(f'[red]{test_string}[/red] ({len(test_string)})')
print(' #  Сигнал   С  По Длина  Серия')
for i, s in enumerate(ka.series):
    signal_color = 'blue' if s['type'] == States.SIGNAL else 'yellow'
    print(f"{i:2}: [{signal_color}]{signal_name[s['type']]:>6}[/{signal_color}] {s['start']:3} {s['end']:3} {s['duration']:5}"
          f"  [green]{test_string[s['start']:s['end']+1]}[/green]")
print('Done.')
