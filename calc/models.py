from django.db import models

class SearchResult(models.Model):
    title = models.CharField(max_length=255)
    url = models.URLField()
    content = models.TextField()

    objects = models.Manager()

    def __str__(self):
        return str(self.title)
