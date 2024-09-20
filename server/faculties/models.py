from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField('user.User', related_name='faculties')

    class Meta:
        db_table = 'faculties'

    def __str__(self):
        return self.name