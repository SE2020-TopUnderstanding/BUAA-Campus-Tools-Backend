from rest_framework.response import Response
from rest_framework.views import APIView


class Ping(APIView):
    @staticmethod
    def get(request):
        return Response(status=200)
