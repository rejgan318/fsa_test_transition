""" Пузырьковая сортировка своими руками """


def bsort(s: list, inplace: bool = False) -> list:
    """
    Сортировка пузырьковым методом
    :param s: входной список для сортировки
    :param inplace: True - модифицируется входной список
    :return: Отсортированный список
    """
    if not inplace:
        s = s.copy()
    for n in range(len(s) - 1, 0, -1):
        for k in range(n):
            if s[k] > s[k + 1]:
                s[k], s[k + 1] = s[k + 1], s[k]
    return s


if __name__ == '__main__':
    test_list = [5, 4, 0, 17]
    print(f'{test_list} -> ', end='')
    bubble_sorted = bsort(test_list, inplace=True)
    print(f'{bubble_sorted}, (original list: {test_list})')
