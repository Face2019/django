from ...face_element_swaping.helpers import point_dividing_a_line_segment, \
                                            find_endpoint, \
                                            get_point_relative_to_another_point
from collections import namedtuple

LipsEndpoints = namedtuple('LipsEndpoints',
                            ["left_endpoint",
                             "top_endpoint",
                             "right_endpoint",
                             "bottom_endpoint"])

def get_lips_endpoints(face_landmarks):

    the_lowest_nose_landmark = face_landmarks["nose_tip"][2]
    the_highest_lips_landmark = face_landmarks["top_lip"][3]

    top_endpoint = point_dividing_a_line_segment(point_A=the_lowest_nose_landmark,
                                                 point_B=the_highest_lips_landmark,
                                                 offset_from_point_A=0.05)

    the_lowest_chin_landmark = face_landmarks["chin"][8]
    the_lowest_lips_landmark = face_landmarks["bottom_lip"][3]
    bottom_endpoint = point_dividing_a_line_segment(point_A=the_lowest_lips_landmark,
                                                    point_B=the_lowest_chin_landmark,
                                                    offset_from_point_A=0.5)

    top_and_bottom_lip = face_landmarks["top_lip"] + face_landmarks["bottom_lip"]
    left_lip = find_endpoint(list_of_coordinates=top_and_bottom_lip,
                             mode="LEFT")
    right_lip = find_endpoint(list_of_coordinates=top_and_bottom_lip,
                              mode="RIGHT")

    left_lip_inside = point_dividing_a_line_segment(point_A=left_lip,
                                                    point_B=right_lip,
                                                    offset_from_point_A=0.25)

    left_lip_outside = get_point_relative_to_another_point(endpoint=left_lip_inside,
                                                           midpoint=left_lip)

    right_lip_inside = point_dividing_a_line_segment(point_A=left_lip,
                                                     point_B=right_lip,
                                                     offset_from_point_A=1 - 0.25)

    right_lip_outside = get_point_relative_to_another_point(endpoint=right_lip_inside,
                                                            midpoint=right_lip)

    return LipsEndpoints(left_endpoint=left_lip_outside,
                         top_endpoint=top_endpoint,
                         right_endpoint=right_lip_outside,
                         bottom_endpoint=bottom_endpoint)
