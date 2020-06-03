# Generated by Django 3.0.6 on 2020-05-30 19:54

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('subject', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='subjectlandingpage',
            name='subject',
            field=models.CharField(default='Physics', help_text='Enter the Subject Name', max_length=20, unique=True),
            preserve_default=False,
        ),
    ]
