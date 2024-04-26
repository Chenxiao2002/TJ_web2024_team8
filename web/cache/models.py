from django.db import models

class MyCacheTable(models.Model):
    cache_key = models.CharField(max_length=255, unique=True)
    value = models.TextField()
    expires = models.DateTimeField()

    class Meta:
        db_table = 'my_cache_table'