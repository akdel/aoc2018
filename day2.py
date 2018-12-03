import numpy as np
import numba as nb
import string
from collections import defaultdict

### MinHash implementation of day2.

def count_elems(elems):
    elem_set = set(elems)
    values = set()
    for elem in elem_set:
        c = elems.count(elem)
        values.add(c)
    if 3 in values and 2 in values:
        return (1, 1)
    elif 3 in values:
        return (0, 1)
    elif 2 in values:
        return (1, 0)
    else:
        return (0, 0)


def obtain_counts(list_of_ids):
    res = np.zeros(2).astype(int)
    for _id in list_of_ids:
        elems = tuple(_id)
        print(_id)
        res += count_elems(elems)
    return res[0] * res[1]

def to_array(list_of_ids):
    res = np.zeros((len(list_of_ids), len(list_of_ids[0])))
    for i in range(len(list_of_ids)):
        _id = list_of_ids[i]
        res[i] = np.array(tuple(_id), dtype="|S1").view("uint8")
    return res.astype(int)

@nb.njit
def check_similarity(arr1, arr2):
    res = 0
    for i in range(arr1.shape[0]):
        if arr1[i] == arr2[i]:
            res += 1
        else:
            continue
    return res

def create_random_strings(n,l):
    alphabet = tuple(string.ascii_lowercase)
    alphabet = tuple("hhvsdkatysmiqjxunezgwcdprohyqlkatysmiqjxbunezgwcyprohvflkftysmiqjxbunezkwcopr")
    return np.random.choice(alphabet, n*l).reshape((n,l)).astype("|S1").view("uint8")

@nb.njit
def _check_similarities_and_return_argsort(id_array, bins, depth=5):
    res = np.zeros((id_array.shape[0], depth), dtype=np.int64)
    current_bin_res = np.zeros(bins.shape[0], dtype=np.int64)
    for i in range(res.shape[0]):
        current_bin_res[:] = 0
        for j in range(bins.shape[0]):
            current_bin_res[j] = check_similarity(id_array[i], bins[j])
        res[i] = np.argsort(current_bin_res)[::-1][:depth]
    return res

def check_similarities_and_return_argsort(id_array, nbins, depth=4):
    bins = create_random_strings(nbins, id_array.shape[1])
    return _check_similarities_and_return_argsort(id_array, bins, depth=depth)

@nb.njit
def compare(arrays):
    for i in range(arrays.shape[0]-1):
        for j in range(i+1, arrays.shape[0]):
            if check_similarity(arrays[i], arrays[j]) == (arrays.shape[1] - 1):
                return arrays[i], arrays[j]
    return np.zeros(1, dtype=np.int64), np.zeros(1, dtype=np.int64)


if __name__ == "__main__":
    from sys import argv
    f = open(argv[1], "r")
    lines = [x.strip() for x in f.readlines()]
    f.close()
    id_array = to_array(lines)
    
    star1 = obtain_counts(lines)
    star2 = check_similarities_and_return_argsort(id_array, 10, 4)