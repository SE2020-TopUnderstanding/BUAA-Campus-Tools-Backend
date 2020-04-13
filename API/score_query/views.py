from rest_framework.response import Response
from rest_framework.views import APIView
from django.http import Http404
from .serializers import *
from .models import *


class ScoreList(APIView):
    @staticmethod
    def get(request):
        req = request.query_params.dict()
        result = Score.objects.all()
        if len(req) > 0:
            for key, value in req.items():
                if key == 'semester':
                    result = result.filter(semester=value)
                elif key == 'student_id':
                    result = result.filter(student_id=value)
                elif key == 'format':
                    pass
                else:
                    raise Http404
        else:
            raise Http404
        score_serializer = ScoreSerializer(result, many=True)
        return Response(score_serializer.data)
