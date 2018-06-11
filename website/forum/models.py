from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Post(models.Model):
    text = models.TextField()
    pub_date = models.DateTimeField('published')
    thread_id = models.ForeignKey('Thread', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return str(id(self))


class Thread(models.Model):
    title = models.CharField(max_length=100)
    timestamp = models.DateTimeField('Date of creation')
    topic_id = models.ForeignKey('Topic', on_delete=models.CASCADE)
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

    def topic(self):
        return Topic.objects.get(id=self.topic_id.id)


class Topic(models.Model):
    name = models.CharField(max_length=100)
    timestamp = models.DateTimeField("Date of creation")
    user_id = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return self.name
