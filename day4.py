import numpy as np
import datetime as dt
import matplotlib
matplotlib.use("macosx")
import matplotlib.pyplot as plt


def parse_guard_lines(lines):
    guard_lines = list()
    for line in lines:
        if "Guard" in line:
            guard_lines.append([line])
        else:
            guard_lines[-1].append(line)
    return guard_lines


class GuardTimes:
    def __init__(self, guard_lines):
        self.lines = guard_lines
        self.guard_id = None
        self.day = None
        self.intervals = None
        self._parse_lines()

    def _parse_lines(self):
        starts = list()
        stops = list()
        first_line = self.lines[0].split()
        self.guard_id = first_line[3]
        self.day = int(first_line[0].split("-")[-1])
        for line in self.lines:
            line = line.split()
            if "falls" in line:
                starts.append(int(line[1].split(":")[1][:-1]))
            elif "wakes" in line:
                stops.append(int(line[1].split(":")[1][:-1]))
        self.intervals = [(starts[i], stops[i]) for i in range(len(starts))]


class Guard:
    def __init__(self, details):
        self.total_hours = 0
        self.guard_id = details[0].guard_id
        self.details = sorted(details, key=(lambda x: x.day))
        self._find_total_hours()
        self.entire_time = None

    def _find_total_hours(self):
        for guard_day in self.details:
            self.total_hours += sum([(stop - start) for (start, stop) in guard_day.intervals])
    
    def reconstruct_entire_time(self):
        self.entire_time = np.zeros((len(self.details), 60), dtype=int)
        for i in range(len(self.details)):
            for (start, stop) in self.details[i].intervals:
                self.entire_time[i, start:stop] = 1


def filter_guards_and_find_max(guards_times):
    ids = set([x.guard_id for x in guards_times])
    total_times = list()
    for guard_id in ids:
        current_guard_details = list(filter((lambda x: True if x.guard_id == guard_id else False), guard_times))
        guard = Guard(current_guard_details)
        total_times.append((guard.total_hours, guard.guard_id))
    return sorted(total_times)[::-1][0]


def filter_single_guard_and_get_max_array(guard_times, guard_id):
    current_guard_details = list(filter((lambda x: True if x.guard_id == guard_id else False), guard_times))
    guard = Guard(current_guard_details)
    guard.reconstruct_entire_time()
    return np.sum(guard.entire_time, axis=0)


def find_most_frequent_day_and_its_guard(guard_times):
    ids = list(set([x.guard_id for x in guard_times]))
    full_array = np.zeros((len(ids), 60))
    for i in range(len(ids)):
        full_array[i] = filter_single_guard_and_get_max_array(guard_times, ids[i])
    idid, _min = np.unravel_index(np.argmax(full_array), full_array.shape)
    plt.imshow(full_array)
    plt.show()
    return ids[idid], _min


def filt_func(line):
    line = line.split()
    year, month, day = line[0].split("-")
    hr, _min = line[1].split(":")
    hr = int(hr)
    _min = int(_min[:-1])
    year = int(year[1:])
    month = int(month)
    day = int(day)
    return dt.datetime(year, month, day, hr, _min)


if __name__ == "__main__":
    from sys import argv
    f = open(argv[1], "r")
    lines = [x.strip() for x in f.readlines()]
    f.close()

    sorted_lines = sorted(lines, key=filt_func)
    guard_lines = parse_guard_lines(sorted_lines)
    guard_times = [GuardTimes(x) for x in guard_lines]
    gtime, gid = filter_guards_and_find_max(guard_times)
    print(np.argmax(filter_single_guard_and_get_max_array(guard_times, gid)) * int(gid[1:]))
    _id, _min = find_most_frequent_day_and_its_guard(guard_times)
    print(int(_id[1:]) * _min)
