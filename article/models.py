from django.db import models
class Author(models.Model):
    name = models.CharField("Имя", max_length=100)
    age = models.PositiveSmallIntegerField("Возраст", default=0)
    description = models.TextField("Описание", null=True, blank=True)
    image = models.ImageField("Изображение", upload_to="actors/", null=True, blank=True)
    def __str__(self):
        return self.name
class Article(models.Model):
    title = models.CharField(max_length=120)
    description = models.TextField()
    body = models.TextField()
    author = models.ForeignKey('Author', related_name='articles', on_delete=models.CASCADE)
    def __str__(self):
        return self.title