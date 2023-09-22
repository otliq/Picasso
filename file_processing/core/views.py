from .models import File
from .tasks import process_file
from .serializers import FileSerializer
from rest_framework.views import APIView
from rest_framework import status, generics
from rest_framework.response import Response


class FileUploadView(APIView):
    """
    API-представление для загрузки файла.

    Обрабатывает POST-запрос для загрузки файла. 
    Ожидает, что данные файла будут переданы в теле запроса. 
    Если сериализатор валиден и файл успешно сохранен, то асинхронно запускается задача `process_file`
    с использованием Celery. 

    Разрешенные методы:
        POST-запрос для загрузки файла.

    Возвращает:
        При успешной передаче:
            Сериализованные данные созданного файла с HTTP статусом 201.
        
        При ошибке:
            Информация об ошибке с HTTP статусом 400.
    """
    def post(self, request):
        serializer = FileSerializer(data=request.data)
        if serializer.is_valid():
            file = serializer.save()
            process_file.delay(file.id)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class FileListView(generics.ListAPIView):
    """
    API-представление для получения списка файлов.

    Это представление предоставляет список всех файлов. Используется метод GET для получения списка.
    Возвращает ответ с сериализованными данными в виде JSON.

    Разрешенные методы:
        GET-запрос для получения списка файлов.
    """
    queryset = File.objects.all()
    serializer_class = FileSerializer