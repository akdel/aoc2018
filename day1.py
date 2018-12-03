import numpy as np

def parse_input(inpt):
    res = list()
    for elem in inpt.split("\n"):
        if elem.startswith("-"):
            res.append(-1 * int(elem.strip()[1:]))
        elif elem.startswith("+"):
            res.append(int(elem.strip()[1:]))
        else:
            continue
    return res

def do_once(oper_array, start=None, memory=None):
    if not start and not memory:
        start = 0
        memory = set()
    for operation in oper_array:
        start += operation
        if start in memory:
            return start
        else:
            memory.add(start)
    return do_once(oper_array, start=start, memory=memory)

inpt = ""

oper_array = parse_input(inpt)
print(do_once(oper_array))
