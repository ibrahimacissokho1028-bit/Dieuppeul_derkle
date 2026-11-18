from django.urls import path

from . import views


app_name = "teachers"

urlpatterns = [
    path("", views.teacher_list, name="list"),
    path("new/", views.teacher_create, name="create"),
    path("<int:id>/", views.teacher_detail, name="detail"),
    path("<int:id>/edit/", views.teacher_update, name="update"),
    path("<int:id>/delete/", views.teacher_delete, name="delete"),
]
