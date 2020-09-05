from django.db import models

# Create your models here.


class Subject(models.Model):
    subjectid = models.AutoField('Subject ID', db_column='subjectID', primary_key=True)  # Field name made lowercase.
    subjectname = models.CharField('Subject Name', db_column='subjectName', unique=True, max_length=255,)  # Field name made lowercase.

    def __str__(self):
        return self.subjectname

class Topic(models.Model):
    topicid = models.AutoField('Topic ID',db_column='topicID', primary_key=True)  # Field name made lowercase.
    topicname = models.CharField('Topic Name', db_column='topicName', unique=True, max_length=255)  # Field name made lowercase.

    class Meta:       
        verbose_name = "Topic"
        verbose_name_plural = "Topics"
        

    def __str__(self):
        return self.topicname    
    

class Question(models.Model):
    questionid = models.AutoField("Question ID", db_column='questionID', primary_key=True)  # Field name made lowercase.
    questiontext = models.CharField("Question Text", db_column='questionText', max_length=500)  # Field name made lowercase.
    questionanswer = models.CharField("Question Answer", db_column='questionAnswer', max_length=1000)  # Field name made lowercase.
    topicid = models.ForeignKey('Topic', on_delete=models.PROTECT, db_column='topicID', verbose_name='Topic')  # Field name made lowercase.
    subjectid = models.ForeignKey('Subject', on_delete=models.PROTECT, db_column='subjectID', verbose_name='Subject')  # Field name made lowercase.
    # topicid = models.IntegerField("Topic ID", db_column='topicID')  # Field name made lowercase.
    # subjectid = models.IntegerField("Subject ID", db_column='subjectID')  # Field name made lowercase.


    class Meta:
        managed = True
        db_table = 'questions'
        unique_together = (('questiontext', 'topicid', 'subjectid'),)
        verbose_name = "Question"
        verbose_name_plural = "Questions"

    def __str__(self):
        return str(self.questionid)

    def question_details(self):
        return self.questiontext,self.questionanswer, self.topicid, self.subjectid

    def subject(self):
        return self.subjectid    