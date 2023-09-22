from django.db import models


class File(models.Model):
    file = models.FileField()
    uploaded_at = models.DateTimeField(auto_now=True)
    processed = models.BooleanField(default=False)