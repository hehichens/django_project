"""
create model
"""

from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse

"""processing time-related transactions"""
from django.utils import timezone

# Create your models here.

class ArticlePost(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE)  # use cascade method to delete data
    title = models.CharField(max_length=100)
    body = models.TextField()
    created = models.DateTimeField(default=timezone.now)  # save the time when post was created
    updated = models.DateTimeField(auto_now=True)  # save the time when post was updated
    total_view = models.PositiveIntegerField(default=0)

    """standardize the behavior of data"""
    class Meta:
        """
        ordering: Specify the order of the data returned by model
        -created: Reverse Order
        """
        ordering = ('-created', )

    def __str__(self):
        """return value when __str__ was called"""
        return self.title

    def get_absolute_url(self):
        return reverse('article:article_detail', args=[self.id])


