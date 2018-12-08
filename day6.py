import numpy as np
import numba as nb


def parse_input_to_array(lines):
    res = np.zeros((len(lines), 2))
    for i in range(res.shape[0]):
        x,y = lines[i].split(",")
        res[i] = (float(y), float(x))
    return res


class Canvas:
    def __init__(self, points, w=300, h=300):
        self.area = (h, w)
        self.points = points + (w - np.max(points))
        self.closest_to_all = None

    def check_closest_to_all_points(self):
        res = np.zeros(self.points.shape[0])
        res2 = np.zeros(self.points.shape[0])
        self.closest_to_all = _check_closest_to_all_points(self.area, 
                                                           self.points, 
                                                           res, res2)

    def _mask_changed(self, shift=10):
        res = np.zeros(self.points.shape[0])
        res2 = np.zeros(self.points.shape[0])
        second_shot = _check_closest_to_all_points((self.area[0]+shift, self.area[1]+shift), self.points+(shift//2), res, res2)
        self.closest_to_all[np.where((second_shot - self.closest_to_all) != 0)[0]] = 0

    def _check_within_threshold(self, thr):
        res2 = np.zeros(self.points.shape[0])
        return _find_totals_for_each_point(self.area, self.points, thr, res2)

    def return_best(self):
        self._mask_changed()
        best = np.argmax(self.closest_to_all)
        return self.closest_to_all[best], best


@nb.njit
def _check_closest_to_all_points(area, points, res, res2):
    for i in range(area[0]):
        for j in range(area[1]):
            x, y = (j, i)
            _single_point_versus_all(points, x, y, res2)
            sorted = np.argsort(res2)
            _1st, _2nd = res2[sorted[:2]]
            if (_1st - _2nd) != 0:
                res[sorted[0]] += 1
    return res

@nb.njit
def _find_totals_for_each_point(area, points, thr, res2):
    res = 0
    for i in range(area[0]):
        for j in range(area[1]):
            x, y = (j, i)
            _single_point_versus_all(points, x, y, res2)
            if np.sum(res2) < thr:
                res += 1
            else:
                continue
    return res


@nb.njit
def _single_point_versus_all(points, x, y, res):
    for i in range(points.shape[0]):
        x1, y1 = points[i]
        res[i] = abs(x1 - x) + abs(y1 - y)
    return res


if __name__ == "__main__":
    from sys import argv
    import time
    f = open(argv[1], "r")
    lines = [x.strip() for x in f.readlines()]
    f.close()
    arr = parse_input_to_array(lines)
    c = Canvas(arr)
    t = time.time()
    c.check_closest_to_all_points()
    print(c.return_best())
    # print(time.time() - t)
    print(c._check_within_threshold(10000))
    print(time.time() - t)
