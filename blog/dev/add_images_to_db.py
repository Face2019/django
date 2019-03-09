"""
    This file enables to searching for images with human faces inside a specified directory.
    The images are converted to base64 as well as to np.array.
    For each image we detect the landmarks of the specified part of face.
    Then we save all this data in the appropriate database.
"""
import django
django.setup()
import os
from PIL import Image
import numpy as np
import json
from blog import settings
from blog.helpers import convert_pil_to_base64, replace_special_signs, check_if_row_exists_in_db
from apps.face_element_swaping import get_faces_landmarks

# Choosing the right part of the face for which we look for photos
# Currently, the following parts of the face are available:
# nose | lips
PART_OF_FACE = "nose"

def load_faces_into_db():

    # We choose a directory which contains photos for the specified part of face(PART_OF_FACE)
    # Remember, when you want to add some image files,
    # put them in the appropriate folder which is specified in 'settings.DIRECTORIES_WITH_FACES'
    directory_with_images = settings.DIRECTORIES_WITH_FACES[PART_OF_FACE]

    image_files = [image for image in os.listdir(directory_with_images)
                   if image.endswith(settings.ACCEPTABLE_FILE_EXTENSIONS)]

    for image in image_files:
        path_to_the_image = os.path.join(directory_with_images, image)

        # When we have the path to the file, we create the 'PIL' object
        pil = Image.open(path_to_the_image)
        image_in_base64 = convert_pil_to_base64(pil=pil)
        image_name = replace_special_signs(file_name=image)
        db_object = settings.DB_OBJECTS[PART_OF_FACE]
        if not check_if_row_exists_in_db(db_object=db_object,
                                         image_name=image_name,
                                         image_in_base_64=image_in_base64):

            rgb_numpy = np.array(pil, dtype=np.uint8)
            face_landmarks = get_faces_landmarks(RGB_numpy_array=rgb_numpy)

            if len(face_landmarks) == 1:
                face_landmarks = settings.LANDMARKS_FUNCTIONS[PART_OF_FACE](face_landmarks[0])
                face_landmarks = json.dumps(face_landmarks)
                db_object.objects.create(image_name=image_name,
                                         image_in_base_64=image_in_base64,
                                         rgb_numpy=rgb_numpy,
                                         face_landmarks=face_landmarks)


# DOdać komentarz o określonym formacie
# dopisać elsy
# ujednolicic landmarks
if __name__ == "__main__":
    load_faces_into_db()