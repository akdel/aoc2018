import numpy as np
import matplotlib
matplotlib.use('macosx')
import matplotlib.pyplot as plt


test_data = """"""

class Canvas:
    def __init__(self):
        self.canvas = None
        self.textiles = list()
    
    def load_textile_data(self, lines):
        for line in lines:
            line = line.strip().split(" ")
            _id = line[0]
            location_left, location_top = map(int, (line[2].strip(":").split(",")))
            sizex, sizey = map(int, (line[3].split("x")))
            self.textiles.append((line[0], location_left, location_top, sizex, sizey))

    def create_canvas(self):
        current_max_x = 0
        current_max_y = 0
        for textile in self.textiles:
            _id, from_left, from_top, sizex, sizey = textile
            if current_max_x < from_left + sizex:
                current_max_x = from_left + sizex
            if current_max_y < from_top + sizey:
                current_max_y = from_top + sizey
        self.canvas = np.zeros((current_max_y, current_max_x), dtype=int)

    def add_textiles_to_canvas(self):
        for textile in self.textiles:
            _id, from_left, from_top, sizex, sizey = textile
            self.canvas[from_top:from_top+sizey, from_left:from_left+sizex] += 1

    def check_non_overlapping(self):
        for textile in self.textiles:
            _id, from_left, from_top, sizex, sizey = textile
            unique = np.unique(self.canvas[from_top:from_top+sizey, from_left:from_left+sizex])
            if unique.shape[0] == 1 and unique[0] == 1:
                print(_id)



c = Canvas()
c.load_textile_data(test_data.split("\n"))
c.create_canvas()
c.add_textiles_to_canvas()
print(c.canvas[c.canvas>=2].shape[0])
# plt.imshow(c.canvas)
# plt.show()
print(c.check_non_overlapping(), True)