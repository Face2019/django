from .models import Post, Photos, ExampleLips, ExampleNoses

from apps.face_element_swaping.endpoints.lips import get_lips_endpoints
from apps.face_element_swaping.endpoints.nose import get_nose_endpoints

DB_OBJECTS = {
    "lips": ExampleLips,
    "nose": ExampleNoses
}

LANDMARKS_FUNCTIONS = {
    "lips": get_lips_endpoints,
    "nose": get_nose_endpoints
}


SPECIAL_SIGNS_IN_FILE_NAMES = {
    "<space>": " ",
    ".jpg": "",
    ".jpeg": ""
}

BASE64_PREFIX = "data:image/jpeg;base64,"


DIRECTORIES_WITH_FACES = {
    "lips":  "./blog/dev/lips",
    "nose": "./blog/dev/noses"
}

ACCEPTABLE_FILE_EXTENSIONS = (".jpg", ".jpeg")


MESSAGES_REGARDING_THE_NUMBER_OF_DETECTED_FACES = {
    "less_than_one": {"face_detected_successfully": False,
                      "message": "Less than one face have been detected."},
    "more_than_one": {"face_detected_successfully": False,
                      "message": "More than one face have been detected."},
    "exactly_one": {"face_detected_successfully": True,
                    "img_src": None}
}
