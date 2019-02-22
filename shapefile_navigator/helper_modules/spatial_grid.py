from collections import defaultdict
import math
from statistics import median


# TODO: CLEAN UP!!!!
class SpatialGrid:
    def __init__(self, abs_max, abs_min, heights, widths, num_rows=None, num_cols=None, create_bboxes=False):
        self.__absolute_max = None
        self.__absolute_min = None

        self.__absolute_height = None
        self.__absolute_width = None

        self.bounding_boxes = defaultdict(list)
        self.__grid = list()

        self.__grid_padding(abs_max, abs_min)

        self.__x_max = self.__absolute_max[0]
        self.__y_max = self.__absolute_max[1]

        self.__x_min = self.__absolute_min[0]
        self.__y_min = self.__absolute_min[1]

        self.__mid_point = self.mid_point_calculation()
        self.__x_mid = self.__mid_point[0]
        self.__y_mid = self.__mid_point[1]

        if (isinstance(num_rows, int) and num_rows > 1) and (isinstance(num_cols, int) and num_cols > 1):
            self.__num_rows = num_rows
            self.__num_cols = num_cols
        else:
            self.calculate_num_rows_cols(median(widths), median(heights))
        self.create_spatial_grid(self.__num_rows, self.__num_cols)

        if create_bboxes is True:
            self.create_bounding_boxes(self.__num_rows, self.__num_cols)

    @property
    def grid(self):
        return self.__grid

    @property
    def absolute_max(self):
        return self.__absolute_max

    @property
    def absolute_min(self):
        return self.__absolute_min

    @property
    def num_rows(self):
        return self.__num_rows

    @property
    def num_cols(self):
        return self.__num_cols

    def __grid_padding(self, abs_max, abs_min):
        abs_min = min(abs_max, abs_min)
        abs_max = max(abs_max, abs_min)

        x_max_temp = abs_max[0] + .00000001
        y_max_temp = abs_max[1] + .00000001
        x_min_temp = abs_min[0] + .00000001
        y_min_temp = abs_min[1] + .00000001

        self.__absolute_max = (x_max_temp, y_max_temp)
        self.__absolute_min = (x_min_temp, y_min_temp)

    @staticmethod
    def distance_calculation(coord1, coord2):
        x1 = coord1[0]
        y1 = coord1[1]
        x2 = coord2[0]
        y2 = coord2[1]
        return math.hypot(x2 - x1, y2 - y1)

    def mid_point_calculation(self):
        coord = ((self.__x_max + self.__x_min) / float(2), (self.__y_max + self.__y_min) / float(2))
        return coord

    def calculate_abs_len_width(self):
        self.__absolute_width = self.distance_calculation(self.__absolute_min, (self.__x_max, self.__y_min))
        self.__absolute_height = self.distance_calculation((self.__x_max, self.__y_min), self.__absolute_max)

    def calculate_num_rows_cols(self, median_width, median_height):
        self.calculate_abs_len_width()

        self.__num_rows = int(self.__absolute_height / median_height)
        self.__num_cols = int(self.__absolute_width / median_width)

    def create_bounding_boxes(self, num_rows, num_cols):
        bottom_left = (self.__x_min, self.__y_min)
        top_left = (self.__x_min, self.__y_max)
        # bottom_right = (self.x_max, self.y_min)
        top_right = (self.__x_max, self.__y_max)

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

    def create_spatial_grid(self, num_rows, num_cols):
        self.__grid = list()

        for row in range(num_rows):
            temp_row = list()
            for col in range(num_cols):
                temp_col = list()
                temp_row.append(temp_col)
            self.__grid.append(temp_row)
