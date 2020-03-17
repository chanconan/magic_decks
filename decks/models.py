import json
from django.db import models
from django.utils import timezone

# Create your models here.

#Simple class for testing Scrapy
class ScrapyItem(models.Model):
    unique_id = models.CharField(max_length=100, null=True)
    data = models.TextField()
    date = models.DateTimeField()

    @property
    def to_dict(self):
        data = {
            'data': json.loads(self.data),
            'date': self.date
        }
        return data

    def __str__(self):
        return self.unique_id