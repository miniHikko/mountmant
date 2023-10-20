import django_filters
from django.http import JsonResponse
from rest_framework.response import Response
from rest_framework import viewsets, status, generics
from .serializers import *
from .models import *


class AuthorViewset(viewsets.ModelViewSet):
    queryset = Climber.objects.all()
    serializer_class = AuthorSerializer


class CoordinateViewset(viewsets.ModelViewSet):
    queryset = Coordinate.objects.all()
    serializer_class = CoordinateSerializer


class LevelViewset(viewsets.ModelViewSet):
    queryset = Level.objects.all()
    serializer_class = LevelSerializer


class ImageViewset(viewsets.ModelViewSet):
    queryset = Image.objects.all()
    serializer_class = ImageSerializer


class PeakViewset(viewsets.ModelViewSet):
    queryset = Peak.objects.all()
    serializer_class = PeakSerializer
    filter_backends = [django_filters.rest_framework.DjangoFilterBackend]
    filterset_fields = ('user__email',)
    http_method_names = ['get', 'post', 'head', 'patch', 'options']

    # переопределяю метод, для вывода сообщения о результатах сохранения данных
    def create(self, request, *args, **kwargs):
        serializer = PeakSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(
                {
                    'status': status.HTTP_200_OK,
                    'message': 'Выполнено',
                    'id': serializer.data[id]
                }
            )
        if status.HTTP_400_BAD_REQUEST:
            return Response(
                {
                    'status': status.HTTP_400_BAD_REQUEST,
                    'message': 'Не выполнено',
                    'id': None
                }
            )
        if status.HTTP_500_INTERNAL_SERVER_ERROR:
            return Response(
                {
                    'status': status.HTTP_500_INTERNAL_SERVER_ERROR,
                    'message': 'Ошибка при выполнении операции',
                    'id': None
                }
            )

# редактирование объекта перевала, если статус все еще new и данные о самом пользователе не меняются.
    def partial_update(self, request, *args, **kwargs):
        pereval = self.get_object()
        if pereval.status == 'new':
            serializer = PeakSerializer(pereval, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'state': '1',
                    'message': 'Запись успешно изменена'
                })
            else:
                return Response({
                    'state': '0',
                    'message': serializer.errors
                })
        else:
            return Response({
                'state': '0',
                'message': f"Не удалось обновить запись, так как сведения уже у модератора и имеют статус: {pereval.get_status_display()}"
            })

# список данных обо всех объектах, которые пользователь с почтой <email> отправил на сервер.
class EmailAPIView(generics.ListAPIView):
    serializer_class = PeakSerializer
    def get(self, request, *args, **kwargs):
        email = kwargs.get('email', None)
        if Peak.objects.filter(user__email=email):
            data = PeakSerializer(Peak.objects.filter(user__email=email), many=True).data
        else:
            data = {
                'message': f'Не существует пользователя с таким email - {email}'
            }
        return JsonResponse(data, safe=False)