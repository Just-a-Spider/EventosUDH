from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField('user.Student', through='FacultyStudent', related_name='faculties')

    class Meta:
        db_table = 'faculties'

    def __str__(self):
        return self.name
    
class FacultyStudent(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty_students')
    student = models.ForeignKey('user.Student', on_delete=models.CASCADE, related_name='student_faculties')

    class Meta:
        db_table = 'faculty_students'
        unique_together = ('faculty', 'student')

    def __str__(self):
        return f'{self.faculty} - {self.student}'
