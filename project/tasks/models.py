from django.conf import settings
from django.db import models


class Task(models.Model):
    owner = models.ForeignKey(settings.AUTH_USER_MODEL,
                              related_name='tasks',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=125, db_index=True)
    description = models.CharField(max_length=255, db_index=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey('tasks.Task', related_name='comments', on_delete=models.CASCADE)
    author = models.ForeignKey(settings.AUTH_USER_MODEL,
                               on_delete=models.CASCADE,
                               null=True)
    body_text = models.CharField(max_length=125, db_index=True)

    def get_author(self):
        if self.author:
            return self.author.username
        else:
            return 'Anonymous'

    def __str__(self):
        return 'Comment {} by {}'.format(self.body_text, self.task)
