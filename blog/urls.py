from django.urls import path
from . import views
from django.conf.urls import url

urlpatterns = [
    path('', views.post_list, name='post_list'),
    url(r'^change_part_of_face/$', views.change_part_of_face, name='change_part_of_face'),
    url(r'^load_faces/$', views.load_faces, name='load_faces')
]

