from ...face_element_swaping.helpers import point_dividing_a_line_segment, get_point_relative_to_another_point
from collections import namedtuple

PointsToAdjustNoses = namedtuple('PointsToAdjustNoses',
                                 ["bottom_left_corner",
                                  "bottom_right_corner",
                                  "top_right_corner",
                                  "top_left_corner"])

CutFieldOfNoses = namedtuple("CutFieldOfNoses",
                             ["bottom_left_corner",
                              "bottom_right_corner",
                              "middle_right_point",
                              "top_right_corner",
                              "top_left_corner",
                              "middle_left_point"])

class NoseEndpoints:

    def __init__(self, face_landmarks_list):

        self._face_landmarks_list = face_landmarks_list
        self._left_eyebrow_endpoint = None
        self._right_eyebrow_endpoint = None
        self._bottom_left_corner = None
        self._bottom_right_corner = None

    def _get_points_to_adjust_noses(self):

        self._left_eyebrow_endpoint = self._face_landmarks_list["left_eyebrow"][4]
        self._right_eyebrow_endpoint = self._face_landmarks_list["right_eyebrow"][0]

        left_point_of_the_bottom_straight = point_dividing_a_line_segment(self._face_landmarks_list["nose_tip"][0],
                                                                          self._face_landmarks_list["top_lip"][0],
                                                                          0.55)

        right_point_of_the_bottom_straight = point_dividing_a_line_segment(self._face_landmarks_list["nose_tip"][4],
                                                                           self._face_landmarks_list["top_lip"][6],
                                                                           0.55)

        bottom_left_corner_inside = point_dividing_a_line_segment(left_point_of_the_bottom_straight,
                                                                  right_point_of_the_bottom_straight,
                                                                  0.4)
        bottom_right_corner_inside = point_dividing_a_line_segment(right_point_of_the_bottom_straight,
                                                                   left_point_of_the_bottom_straight,
                                                                   0.4)

        self._bottom_left_corner = get_point_relative_to_another_point(endpoint=bottom_left_corner_inside,
                                                                       midpoint=left_point_of_the_bottom_straight)

        self._bottom_right_corner = get_point_relative_to_another_point(endpoint=bottom_right_corner_inside,
                                                                        midpoint=right_point_of_the_bottom_straight)

        top_left_corner_inside = point_dividing_a_line_segment(self._left_eyebrow_endpoint,
                                                               self._bottom_left_corner,
                                                               0.07)

        top_left_corner_of_adjusting = get_point_relative_to_another_point(endpoint=top_left_corner_inside,
                                                                           midpoint=self._left_eyebrow_endpoint)

        top_right_corner_inside = point_dividing_a_line_segment(self._right_eyebrow_endpoint,
                                                                self._bottom_right_corner,
                                                                0.07)

        top_right_corner_of_adjusting = get_point_relative_to_another_point(endpoint=top_right_corner_inside,
                                                                            midpoint=self._right_eyebrow_endpoint)

        return PointsToAdjustNoses(bottom_left_corner=self._bottom_left_corner,
                                                     bottom_right_corner=self._bottom_right_corner,
                                                     top_right_corner=top_right_corner_of_adjusting,
                                                     top_left_corner=top_left_corner_of_adjusting)

    def _cut_field_of_noses(self):

        middle_left_point_of_cut_field = point_dividing_a_line_segment(self._face_landmarks_list["left_eye"][3],
                                                                       self._face_landmarks_list["right_eye"][0],
                                                                       0.2)

        middle_right_point_of_cut_field = point_dividing_a_line_segment(self._face_landmarks_list["right_eye"][0],
                                                                        self._face_landmarks_list["left_eye"][3],
                                                                        0.2)

        cut_field_of_noses = CutFieldOfNoses(bottom_left_corner=self._bottom_left_corner,
                                             bottom_right_corner=self._bottom_right_corner,
                                             middle_right_point=middle_right_point_of_cut_field,
                                             top_right_corner=self._right_eyebrow_endpoint,
                                             top_left_corner=self._left_eyebrow_endpoint,
                                             middle_left_point=middle_left_point_of_cut_field)
        return cut_field_of_noses

    def _get_nose_endpoints(self, cut_points):
        nose_endpoints = {"points_to_adjust_noses": self._get_points_to_adjust_noses()}
        if not cut_points:
            return nose_endpoints
        nose_endpoints["cut_field"] = self._cut_field_of_noses()
        return nose_endpoints

    @classmethod
    def get_nose_endpoints(cls, face_landmarks_list, cut_points=True):
        nose_endpoints = cls(face_landmarks_list=face_landmarks_list)
        nose_endpoints = nose_endpoints._get_nose_endpoints(cut_points=cut_points)
        return nose_endpoints

get_nose_endpoints = NoseEndpoints.get_nose_endpoints