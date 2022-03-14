# Generated by Django 4.0.1 on 2022-03-09 19:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0009_alter_student_classes'),
    ]

    operations = [
        migrations.AlterField(
            model_name='student',
            name='classes',
            field=models.ManyToManyField(blank=True, related_name='students', to='accounts.Classroom'),
        ),
    ]