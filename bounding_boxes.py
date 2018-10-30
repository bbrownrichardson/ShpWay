from collections import defaultdict
import math


class BoundingBoxTracker:
    def __init__(self, abs_max, abs_min):
        if abs_min > abs_max:
            temp = abs_min
            abs_min = abs_max
            abs_max = temp

        self.bounding_boxes = defaultdict(list)

        self.absolute_max = abs_max
        self.x_max = self.absolute_max[0]
        self.y_max = self.absolute_max[1]

        self.absolute_min = abs_min
        self.x_min = self.absolute_min[0]
        self.y_min = self.absolute_min[1]

        self.mid_point = self.mid_point_calculation()
        self.x_mid = self.mid_point[0]
        self.y_mid = self.mid_point[1]

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

    def create_bounding_boxes(self, num_rows=2, num_cols=2):
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

    def get_bboxes(self):
        return self.bounding_boxes

    def get_absolute_max(self):
        return self.absolute_max

    def get_absolute_min(self):
        return self.absolute_min

    def get_midpoint(self):
        return self.mid_point
