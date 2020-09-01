from django.db import models

# Create your models here.


class Subject(models.Model):
    subjectid = models.AutoField('Subject ID', db_column='subjectID', primary_key=True)  # Field name made lowercase.
    subjectname = models.CharField('Subject Name', db_column='subjectName', unique=True, max_length=255,)  # Field name made lowercase.

    def __str__(self):
        return self.subjectname
    