from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from rest_framework.renderers import JSONRenderer
from rest_framework.parsers import JSONParser
from snippets.models import CourseTable
from snippets.serializers import CourseSerializer


class JSONResponse(HttpResponse):
    """
    An HttpResponse that renders its content into JSON.
    """
    def __init__(self, data, **kwargs):
        content = JSONRenderer().render(data)
        kwargs['content_type'] = 'application/json'
        super(JSONResponse, self).__init__(content, **kwargs)


@csrf_exempt
def snippet_list(request):
    """
    get all students' class
    """
    if request.method == 'GET':
        snippets = CourseTable.objects.all()
        serializer = CourseSerializer(snippets, many=True)
        return JSONResponse(serializer.data)


@csrf_exempt
def snippet_detail(request, pk):
    """
    get specific student's class
    """
    try:
        # find the student's whose id = student_id class table.
        snippet = CourseTable.objects.get(student_id=pk)
    except CourseTable.DoesNotExist:
        # if cannot find, return 404
        return HttpResponse(status=404)

    if request.method == 'GET':
        # response to 'GET' method
        serializer = CourseSerializer(snippet)
        return JSONResponse(serializer.data)
