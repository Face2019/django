import json

import numpy as np
from PIL import Image
from django.http import JsonResponse

from apps.face_element_swaping import get_faces_landmarks
from apps.face_element_swaping.change_faces import ChangeFaceElement
from blog import settings
from blog.helpers import convert_pil_to_base64, \
    check_if_row_exists_in_db, \
    get_db_row_with_specified_id, \
    get_rgb_pil_obj_from_base64, \
    save_row_to_db
from ..models import Photos


class ProcessUserPhoto:

    def __init__(self, inputPhoto, activePartOfFace, faceId):
        ProcessUserPhoto.validate_data(params_dict=locals())

        self._inputPhoto = inputPhoto
        self._activePartOfFace = activePartOfFace
        self._faceId = faceId
        self._image_in_base64 = None

    @staticmethod
    def validate_data(params_dict):
        all_params_correct = True
        for param_key in params_dict:
            if not params_dict[param_key]:
                print(param_key)

    @staticmethod
    def remove_prefix_from_base64(base64_with_prefix):
        return base64_with_prefix.split(',')[1]

    def _prepare_params_needed_to_face_swaping(self, landmarks):
        endpoints = {}
        if self._activePartOfFace == "lips":
            endpoints["polygon"] = landmarks
            endpoints["cut_field"] = None
        else:
            endpoints["polygon"] = landmarks["points_to_adjust_noses"]
            endpoints["cut_field"] = landmarks["cut_field"]
        return endpoints

    def _process_existing_image(self):

        photo_from_db = Photos.objects.get(input_photo=self._image_in_base64)
        number_of_detected_faces = photo_from_db.number_of_detected_faces
        if number_of_detected_faces < 1:
            data = settings.MESSAGES_REGARDING_THE_NUMBER_OF_DETECTED_FACES["less_than_one"]
            return JsonResponse(data)
        elif number_of_detected_faces > 1:
            data = settings.MESSAGES_REGARDING_THE_NUMBER_OF_DETECTED_FACES["more_than_one"]
            return JsonResponse(data)
        dst_numpy_array = photo_from_db.photo_in_rgb
        landmarks_of_the_face = json.loads(photo_from_db.face_landmarks)[self._activePartOfFace]


        source_file = get_db_row_with_specified_id(db_object=settings.DB_OBJECTS[self._activePartOfFace],
                                                   row_id=self._faceId)

        source_landmarks = json.loads(source_file.face_landmarks)
        source_landmarks = self._prepare_params_needed_to_face_swaping(landmarks=source_landmarks)
        source_numpy_array = source_file.rgb_numpy

        dst_endpoints = self._prepare_params_needed_to_face_swaping(landmarks=landmarks_of_the_face)

        a = ChangeFaceElement.changeFaceElement(src_RGB_array=source_numpy_array,
                                                dst_RGB_array=dst_numpy_array,
                                                src_polygon=source_landmarks["polygon"],
                                                dst_polygon=dst_endpoints["polygon"],
                                                dst_cut_field=dst_endpoints["cut_field"])

        b = convert_pil_to_base64(Image.fromarray(a, 'RGB'))
        data = {"face_detected_successfully": True,
                "img_src": b}
        return JsonResponse(data)

    @staticmethod
    def _get_landmarks_of_all_prepared_parts_of_face(landmarks):
        landmarks_of_parts_of_face = {}
        for part_of_face in settings.LANDMARKS_FUNCTIONS:
            landmarks_of_parts_of_face[part_of_face] = settings.LANDMARKS_FUNCTIONS[part_of_face](landmarks)

        return landmarks_of_parts_of_face

    def _process_new_image(self):

        pil = get_rgb_pil_obj_from_base64(image_in_base64=self._image_in_base64)
        RGB_numpy_array = np.array(pil, dtype=np.uint8)

        faces_landmarks = get_faces_landmarks(RGB_numpy_array=RGB_numpy_array)
        number_of_detected_faces = len(faces_landmarks)

        if number_of_detected_faces < 1:
            save_row_to_db(db_object=Photos,
                           input_photo=self._image_in_base64,
                           photo_in_rgb=None,
                           number_of_detected_faces=number_of_detected_faces,
                           face_landmarks=None)

            data = settings.MESSAGES_REGARDING_THE_NUMBER_OF_DETECTED_FACES["less_than_one"]
            return JsonResponse(data)
        elif number_of_detected_faces > 1:
            save_row_to_db(db_object=Photos,
                           input_photo=self._image_in_base64,
                           photo_in_rgb=None,
                           number_of_detected_faces=number_of_detected_faces,
                           face_landmarks=None)

            data = settings.MESSAGES_REGARDING_THE_NUMBER_OF_DETECTED_FACES["more_than_one"]
            return JsonResponse(data)

        landmarks = ProcessUserPhoto._get_landmarks_of_all_prepared_parts_of_face(faces_landmarks[0])
        save_row_to_db(db_object=Photos,
                       input_photo=self._image_in_base64,
                       photo_in_rgb=RGB_numpy_array,
                       number_of_detected_faces=number_of_detected_faces,
                       face_landmarks=json.dumps(landmarks))

        landmarks_of_the_face = settings.LANDMARKS_FUNCTIONS[self._activePartOfFace](faces_landmarks[0])
        source_file = get_db_row_with_specified_id(db_object=settings.DB_OBJECTS[self._activePartOfFace],
                                                   row_id=self._faceId)

        source_landmarks = json.loads(source_file.face_landmarks)
        source_landmarks = self._prepare_params_needed_to_face_swaping(landmarks=source_landmarks)

        dst_endpoints = self._prepare_params_needed_to_face_swaping(landmarks=landmarks_of_the_face)

        source_numpy_array = source_file.rgb_numpy

        a = ChangeFaceElement.changeFaceElement(src_RGB_array=source_numpy_array,
                                                dst_RGB_array=RGB_numpy_array,
                                                src_polygon=source_landmarks["polygon"],
                                                dst_polygon=dst_endpoints["polygon"],
                                                dst_cut_field=dst_endpoints["cut_field"])
        b = convert_pil_to_base64(Image.fromarray(a))
        data = settings.MESSAGES_REGARDING_THE_NUMBER_OF_DETECTED_FACES["exactly_one"]
        data["img_src"] = b

        return JsonResponse(data)

    def _alll(self):
        self._image_in_base64 = ProcessUserPhoto.remove_prefix_from_base64(base64_with_prefix=self._inputPhoto)
        if check_if_row_exists_in_db(db_object=Photos,
                                     input_photo=self._image_in_base64):
            return self._process_existing_image()
        else:
            return self._process_new_image()

    @classmethod
    def all(cls, inputPhoto, activePartOfFace, faceId):

        photo_processing = cls(inputPhoto=inputPhoto,
                               activePartOfFace=activePartOfFace,
                               faceId=faceId)
        return photo_processing._alll()
