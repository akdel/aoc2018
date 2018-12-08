import numpy as np
import numba as nb
import time


def compress(seq, seq_pure):
    mask = np.ones(seq.shape, dtype=np.bool)
    diff = seq[:-1] - seq[1:]
    zero_ids = np.where(diff == 0)[0]
    i = 0
    while i < zero_ids.shape[0]:
        current_zero_id = zero_ids[i]
        first = seq[current_zero_id] == seq_pure[current_zero_id]
        second = seq[current_zero_id+1] == seq_pure[current_zero_id+1]
        if (i == zero_ids.shape[0] - 1) and ((first and (not second)) or ((not first) and second)):
            mask[zero_ids[i]] = 0
            mask[zero_ids[i] + 1] = 0
            i += 1
        elif ((first and (not second)) or ((not first) and second)):
            mask[zero_ids[i]] = 0
            mask[zero_ids[i] + 1] = 0
            i += 2
        else:
            i += 1
    return seq[mask], seq_pure[mask], seq[mask].shape[0]


def _recursive_react(seq1, seq2):
    if len(seq1) == 0:
        return [seq2[0]], seq2[1:]
    elif (seq1[-1].lower() == seq2[0].lower()) and (seq1[-1] != seq2[0]):
        return seq1[:-1], seq2[1:]
    else:
        return seq1 + [seq2[0]], seq2[1:]


def recursive(seq2):
    seq1 = []
    while len(seq2) != 0:
        seq1, seq2 = _recursive_react(seq1, seq2)
    return seq1


def do_while(seq, seq_pure):
    last_shape = -1
    current_shape = seq.shape[0]
    while last_shape != current_shape:
        last_shape = int(current_shape)
        seq, seq_pure, current_shape = compress(seq, seq_pure)
    return seq_pure


def remove_letter_and_react(seq, seq_pure, letter):
    mask = np.ones(seq.shape[0], dtype=np.bool)
    upper_case = ord(letter.upper())
    lower_case = ord(letter.lower())
    mask[np.where(seq_pure == upper_case)[0]] = 0
    mask[np.where(seq_pure == lower_case)[0]] = 0
    new_seq = seq[mask]
    new_seq_pure = seq_pure[mask]
    return do_while(new_seq, new_seq_pure)


if __name__ == "__main__":
    from sys import argv
    f = open(argv[1], "r")
    text = f.read().strip()
    f.close()
    # seq = np.array(tuple(text.lower()), dtype="|S1").view("uint8")
    # seq_pure = np.array(tuple(text), dtype="|S1").view("uint8")
    # print(do_while(seq, seq_pure).shape)
    # res = list()
    text = list(tuple(text))
    print(len(recursive(text)))
    

    # for i in range(26):
    #     letter = chr(ord("a") + i)
    #     res.append(remove_letter_and_react(seq, seq_pure, letter).shape[0])
    # print(time.time()-t)
    # print(min(res))