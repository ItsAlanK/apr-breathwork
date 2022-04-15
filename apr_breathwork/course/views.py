from django.shortcuts import render, get_object_or_404
from .models import CourseInfo, Urls


def course_page(request, course_id):

    """ View which returns detailed view of the requested product """

    course_info = get_object_or_404(CourseInfo, pk=course_id)
    classes = Urls.objects.filter(course=course_info)

    context = {
            'course_info': course_info,
            'classes': classes,
        }

    return render(request, 'course/course.html', context)
