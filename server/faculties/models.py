from django.db import models

class Faculty(models.Model):
    name = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    students = models.ManyToManyField('user.User', through='FacultyStudent', related_name='faculties')

    class Meta:
        db_table = 'faculties'

    def __str__(self):
        return self.name
    
class FacultyStudent(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty_students')
    student = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='student_faculties')

    class Meta:
        db_table = 'faculty_students'

    def __str__(self):
        return f'{self.faculty} - {self.student}'
    
class FacultyCoordinator(models.Model):
    faculty = models.ForeignKey(Faculty, on_delete=models.CASCADE, related_name='faculty_coordinators')
    coordinator = models.ForeignKey('user.User', on_delete=models.CASCADE, related_name='coordinator_faculties')

    class Meta:
        db_table = 'faculty_coordinators'

    def __str__(self):
        return f'{self.faculty} - {self.coordinator}'
