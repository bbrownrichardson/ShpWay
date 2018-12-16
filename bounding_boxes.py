from collections import defaultdict
import math
from statistics import median


class BoundingBoxTracker:
    def __init__(self, abs_max, abs_min, heights, widths, num_rows=None, num_cols=None):
        if abs_min > abs_max:
            temp = abs_min
            abs_min = abs_max
            abs_max = temp

        x_max_temp = abs_max[0] + .00000001
        y_max_temp = abs_max[1] + .00000001
        x_min_temp = abs_min[0] + .00000001
        y_min_temp = abs_min[1] + .00000001

        abs_max = (x_max_temp, y_max_temp)
        abs_min = (x_min_temp, y_min_temp)

        self.bounding_boxes = defaultdict(list)
        self.grid = list()

        self.absolute_max = abs_max
        self.x_max = self.absolute_max[0]
        self.y_max = self.absolute_max[1]

        self.absolute_min = abs_min
        self.x_min = self.absolute_min[0]
        self.y_min = self.absolute_min[1]

        self.mid_point = self.mid_point_calculation()
        self.x_mid = self.mid_point[0]
        self.y_mid = self.mid_point[1]

        self.absolute_height = None
        self.absolute_width = None
        self.num_rows = num_rows
        self.num_cols = num_cols
        if self.num_rows is None and self.num_cols is None:
            self.calculate_num_rows_cols(median(widths), median(heights))
        self.create_bbox_grid(self.num_rows, self.num_cols)
        self.create_bounding_boxes(self.num_rows, self.num_cols)

    @staticmethod
    def distance_calculation(coord1, coord2):
        x1 = coord1[0]
        y1 = coord1[1]
        x2 = coord2[0]
        y2 = coord2[1]
        return math.hypot(x2 - x1, y2 - y1)

    def mid_point_calculation(self):
        coord = ((self.x_max + self.x_min) / float(2), (self.y_max + self.y_min) / float(2))
        return coord

    def calculate_abs_len_width(self):
        self.absolute_width = self.distance_calculation(self.absolute_min, (self.x_max, self.y_min))
        self.absolute_height = self.distance_calculation((self.x_max, self.y_min), self.absolute_max)

    def calculate_num_rows_cols(self, median_width, median_height):
        self.calculate_abs_len_width()

        self.num_rows = int(self.absolute_height/median_height)
        self.num_cols = int(self.absolute_width/median_width)

    def create_bounding_boxes(self, num_rows, num_cols):
        bottom_left = (self.x_min, self.y_min)
        top_left = (self.x_min, self.y_max)
        # bottom_right = (self.x_max, self.y_min)
        top_right = (self.x_max, self.y_max)

        col_distance = self.distance_calculation(top_left, top_right)
        col_padding = col_distance/float(num_cols)

        row_distance = self.distance_calculation(bottom_left, top_left)
        row_padding = row_distance/float(num_rows)

        btm_x = bottom_left[0]
        btm_y = bottom_left[1]
        top_x = btm_x + col_padding
        top_y = btm_y + row_padding

        for row in range(num_rows):
            for col in range(num_cols):
                self.bounding_boxes[(btm_x, btm_y), (top_x, top_y)] = list()
                btm_x += col_padding
                top_x += col_padding

            btm_x = bottom_left[0]
            top_x = btm_x + col_padding
            btm_y += row_padding
            top_y = btm_y + row_padding

    def create_bbox_grid(self, num_rows, num_cols):
        self.grid = list()

        for row in range(num_rows):
            temp_row = list()
            for col in range(num_cols):
                temp_col = list()
                temp_row.append(temp_col)
            self.grid.append(temp_row)
