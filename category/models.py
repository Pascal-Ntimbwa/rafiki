from django.db import models
from django.urls import reverse

# Create your models here.


class Category(models.Model):
    name = models.CharField(max_length=75, unique=True)
    slug = models.SlugField(max_length=100, unique=True)
    description = models.TextField(max_length=100, blank=True)
    image = models.ImageField(upload_to="photo/category", blank=True)

    class Meta:
        verbose_name_plural = "Categories"
        ordering = ('name',)


    def get_url(self):
        return reverse('product_by_category', args=[self.slug])


    def __str__(self):
        return self.name



