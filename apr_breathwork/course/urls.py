from django.urls import path
from . import views

urlpatterns = [
    path('<course_id>', views.course_page, name='course_page'),
]
