from django.conf import settings
from django.db import models
from django.utils.text import slugify
# Create your models here.


class Lecturer(models.Model):
    first_name = models.CharField(max_length=55, null=False)
    last_name = models.CharField(max_length=55, null=False)
    picture = models.ImageField(
        upload_to='main/profile_pictures/', default='main/profile_pictures/default_pfp.jpeg')
    slug = models.SlugField(unique=True, blank=True)

    class Meta:
        unique_together = [
            ('first_name', 'last_name')
        ]

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.first_name + ' ' + self.last_name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class Subject(models.Model):
    name = models.CharField(max_length=255, unique=True)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.name)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.name


class LecturerSubject(models.Model):
    lecturer = models.ForeignKey(
        Lecturer, on_delete=models.CASCADE, related_name='subjects')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)

    def save(self, *args, **kwargs) -> None:
        if not self.slug:
            self.slug = slugify(self.lecturer.slug + ' '+self.subject.slug)
        return super().save(*args, **kwargs)

    def __str__(self) -> str:
        return self.slug


class Review(models.Model):

    RATINGS = [(i, i) for i in range(1, 6)]

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.PROTECT)
    lecturer_subject = models.ForeignKey(
        LecturerSubject, on_delete=models.CASCADE)
    rate = models.IntegerField(choices=RATINGS)
    comment = models.TextField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return f'{self.user.username}-{self.rate}'

    class Meta:
        unique_together = (
            ('lecturer_subject', 'user')
        )
