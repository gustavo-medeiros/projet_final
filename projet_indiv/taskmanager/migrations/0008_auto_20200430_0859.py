# Generated by Django 2.1.15 on 2020-04-30 06:59

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0007_auto_20200430_0858'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['-priority']},
        ),
    ]
