# Generated by Django 2.1.15 on 2020-04-30 06:58

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('taskmanager', '0006_auto_20200428_1312'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='task',
            options={'ordering': ['priority']},
        ),
    ]