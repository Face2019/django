from blog import settings
from django.http import JsonResponse
from django.shortcuts import render
from django.utils.decorators import method_decorator
from django.views.decorators.csrf import csrf_exempt
from blog.helpers import create_dict_from_django_query_dict
from .models import Photos, ExampleLips
from .process_user_data.swap_elements_of_face import ProcessUserPhoto


def post_list(request):

    example_lips = [{"id": obj.model_id,
                     "name": obj.image_name,
                     "source": obj.image_in_base_64} for obj in ExampleLips.objects.all()]

    return render(request,
                  'blog/post_list.html',
                  {'example_lips': example_lips})


# Do bazy zapisać obydwa landmarki
# Klucze zwracanych punktów
#Zmienić na activePartOfFace na smo part OF face
# Liczba twarzy zmienic ifa
def check_if_face_exists_in_db(image_in_base64):
    return Photos.objects.filter(input_photo=image_in_base64).exists()

@method_decorator(csrf_exempt, name='dispatch')
def load_faces(request):
    part_of_face = request.POST.get('partOfFace')
    example_faces = [{"id": obj.model_id,
                     "name": obj.image_name,
                     "source": obj.image_in_base_64} for obj in settings.DB_OBJECTS[part_of_face].objects.all()]

    data = {"example_faces": example_faces}
    return JsonResponse(data)



@method_decorator(csrf_exempt, name='dispatch')
def change_part_of_face(request):

    photo_data = create_dict_from_django_query_dict(query_dict=request.POST)
    return ProcessUserPhoto.all(**photo_data)


