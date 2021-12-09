import numpy as np
from numba import jit


def order_exists(arr, order):
    arr_size = arr.size
    order_size = order.size
    order_range = np.arange(order_size)
    m = (arr[np.arange(arr_size - order_size + 1)[:, None] + order_range] == order).all(1)

    if m.any() > 0:
        return np.where(np.convolve(m, np.ones(order_size, dtype=int)) > 0)[0]
    else:
        return []


def check_sequence(arr, noise, order):
    sequence_arr = filter_array(arr, noise)
    order_exist = order_exists(sequence_arr, order)
    return len(order_exist) > 0


@jit(nopython=True, cache=True)  # , fastmath = True)
def filter_array(data, noise_level):
    data = np.split(data, np.where(np.diff(data[:]))[0] + 1)
    new_list = []
    element_counter = 0
    previous_appended = -1
    for i in data:
        if i[0] == 0:
            element_counter += i.size
            continue
        if i.size + element_counter < noise_level:
            element_counter += i.size
            continue
        if previous_appended == i[0]:
            continue
        previous_appended = i[0]
        new_list.append(i[0])
        element_counter = 0

    return np.array(new_list)
