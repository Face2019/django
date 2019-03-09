from base64 import b64encode, b64decode
from io import BytesIO

from PIL import Image
from blog import settings


def convert_pil_to_base64(pil):
    buffer = BytesIO()
    pil.save(buffer, format="JPEG")
    image_in_base64_without_prefix = buffer.getvalue()
    image_in_base64_without_prefix = b64encode(image_in_base64_without_prefix).decode()
    image_in_base64_with_prefix = settings.BASE64_PREFIX + image_in_base64_without_prefix
    return image_in_base64_with_prefix

def replace_special_signs(file_name):
    for key, value in settings.SPECIAL_SIGNS_IN_FILE_NAMES.items():
        file_name = file_name.replace(key, value)
    return file_name

def check_if_row_exists_in_db(db_object, **search_par):
    return db_object.objects.filter(**search_par).exists()

def get_db_row_with_specified_id(db_object, row_id):
    return db_object.objects.get(model_id=row_id)

def convert_PIL_object_to_RGB(PIL_object):
    if PIL_object.mode.upper() != "RGB":
        PIL_object = PIL_object.convert('RGB')
    return PIL_object

def get_rgb_pil_obj_from_base64(image_in_base64):
    decoded_base64 = b64decode(image_in_base64)
    pil = Image.open(BytesIO(decoded_base64))
    pil = convert_PIL_object_to_RGB(PIL_object=pil)
    return pil

def save_row_to_db(db_object, **columns_data):
    db_object.objects.create(**columns_data)

def create_dict_from_django_query_dict(query_dict):
    data = dict(query_dict)
    data_keys = data.keys()
    data_values = [query_dict.get(key, None) for key in data_keys]
    python_dict = dict(zip(data_keys, data_values))
    return python_dict