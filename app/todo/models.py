from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Category(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Category")
        verbose_name_plural = ("Categories")

    def __str__(self):
        return self.name

class Priority(models.Model):
    name = models.CharField(max_length=100)

    class Meta:
        verbose_name = ("Priority")
        verbose_name_plural = ("Priorities")

    def __str__(self):
        return self.name

class Task(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    title = models.CharField(max_length=250)

    content = models.TextField(blank=True, null=True)

    completed = models.BooleanField(default=False)

    created = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

    due_date = models.DateField(default=timezone.now().strftime("%Y-%m-%d"))

    category = models.ForeignKey(Category,
                                default="general",
                                on_delete=models.PROTECT)

    priority = models.ForeignKey(Priority,
                                default="normal",
                                on_delete=models.PROTECT)

    class Meta:
        verbose_name = ("Task")
        verbose_name_plural = ("Tasks")
        ordering = ["-created"]

    def __str__(self):
        return self.title
