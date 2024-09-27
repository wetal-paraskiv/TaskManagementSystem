from django.db import models


class Task(models.Model):
    owner = models.ForeignKey('users.CustomUser',
                              related_name='tasks',
                              on_delete=models.CASCADE)
    title = models.CharField(max_length=125, db_index=True)
    description = models.CharField(max_length=255, db_index=True)
    status = models.BooleanField(default=True)

    def __str__(self):
        return self.title


class Comment(models.Model):
    task = models.ForeignKey('tasks.Task', related_name='comments', on_delete=models.CASCADE)
    # author = models.CharField(max_length=25, db_index=True)
    author = models.ForeignKey('users.CustomUser',
                              related_name='comments',
                              on_delete=models.CASCADE)
    body_text = models.CharField(max_length=125, db_index=True)

    def __str__(self):
        return 'Comment {} by {}'.format(self.body_text, self.task)
