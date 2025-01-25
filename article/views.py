from django.shortcuts import render
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Capital
from .serializers import CapitalSerializer
class GetCapitalInfoView(APIView):
    def get(self, request):
        queryset = Capital.objects.all()
        serializer_for_queryset = CapitalSerializer(
            instance=queryset,
            many=True 
        )
        return Response(serializer_for_queryset.data)
def main_page(request):
    """
    Контроллер для отображения на главной странице списка всех записей.
    """
    list_of_capitals = Capital.objects.all()
    context = {'list_of_capitals': list_of_capitals}
    return render(
        request=request,
        template_name='DRF/main.html',
        context=context
    )