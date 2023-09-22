from django.db import models


class File(models.Model):
    """
    Представляеть загруженные файлы
    Содержит поля:
        file: поле типа FileField, используемое для загрузки файла.
        uploaded_at: поле типа DateTimeField, содержит дату и время загрузки файла.
        processed: поле типа BooleanField, указывает, был ли файл обработан.
    """
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False)