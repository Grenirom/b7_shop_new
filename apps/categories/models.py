from django.db import models
from django.utils.text import slugify
from multiupload.fields import MultiFileField


class Category(models.Model):
    name = models.CharField(max_length=150, unique=True, verbose_name='Имя категории')
    image = models.ImageField(upload_to='category-images/')
    parent = models.ForeignKey('self', on_delete=models.SET_NULL,
                               related_name='children', blank=True, null=True,
                               verbose_name='Родительская категория')

    def __str__(self):
        return f'{self.name}'

    class Meta:
        verbose_name = 'Категория'
        verbose_name_plural = 'Категории'
