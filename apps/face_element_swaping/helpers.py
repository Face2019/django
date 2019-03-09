from operator import le, gt
import face_recognition
def point_dividing_a_line_segment(point_A, point_B, offset_from_point_A):
    x = (1 - offset_from_point_A) * point_A[0] + offset_from_point_A * point_B[0]
    y = (1 - offset_from_point_A) * point_A[1] + offset_from_point_A * point_B[1]

    return (int(round(x)),int(round(y)))

TYPES_OF_ENDPOINTS = {
    "LEFT": {"INDEX_OF_A_COORDINATE": 0, "COMPARSION_OPERATOR": le},
    "RIGHT": {"INDEX_OF_A_COORDINATE": 0, "COMPARSION_OPERATOR": gt},
    "TOP" : {"INDEX_OF_A_COORDINATE": 1, "COMPARSION_OPERATOR": le},
    "BOTTOM": {"INDEX_OF_A_COORDINATE": 1, "COMPARSION_OPERATOR": gt}
}

def find_endpoint(list_of_coordinates,
                  mode="TOP"):

    endpoint_settings = TYPES_OF_ENDPOINTS.get(mode, TYPES_OF_ENDPOINTS["TOP"])
    index_of_a_coordinate = endpoint_settings["INDEX_OF_A_COORDINATE"]
    comparison_operator = endpoint_settings["COMPARSION_OPERATOR"]

    wanted_point = list_of_coordinates[0]
    for idx in range(1, len(list_of_coordinates)):
        if comparison_operator(list_of_coordinates[idx][index_of_a_coordinate], wanted_point[index_of_a_coordinate]):
            wanted_point = list_of_coordinates[idx]
    return wanted_point

def get_point_relative_to_another_point(endpoint, midpoint):

    return (2 * midpoint[0] - endpoint[0],
            2 * midpoint[1] - endpoint[1])



def get_faces_landmarks(RGB_numpy_array):

    face_landmarks_list = face_recognition.face_landmarks(RGB_numpy_array)
    return face_landmarks_list