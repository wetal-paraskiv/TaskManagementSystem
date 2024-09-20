from django.db import models


class Task(models.Model):
    title = models.CharField(max_length=125, db_index=True)
    description = models.CharField(max_length=255, db_index=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title
