from django.db import models
from django.utils.text import slugify
# Create your models here.


class Lecturer(models.Model):
    first_name = models.CharField(max_length=55, null=False)
    last_name = models.CharField(max_length=55, null=False)
    picture = models.ImageField(
        upload_to='main/profile_pictures/', null=True, blank=True)
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = [
            ('first_name', 'last_name')
        ]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.first_name + ' ' + self.last_name)
        return super().save(*args, **kwargs)
