
def parse_input(inpt):
    res = list()
    for elem in inpt:
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


if __name__ == "__main__":
    from sys import argv
    f = open(argv[1], "w")
    lines = [x.strip() for x in f.readlines()]
    f.close()
    oper_array = parse_input(lines)
    print(do_once(oper_array))
