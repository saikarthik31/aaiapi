from django.db import models

class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return str(self.title)


#second model for datble data


class Employee(models.Model):
    name = models.CharField(max_length=100)
    age = models.IntegerField()
    department = models.CharField(max_length=100)

    def __str__(self):
        return str(self.name)
