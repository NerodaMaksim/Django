# Generated by Django 3.0.5 on 2020-04-22 12:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Login', '0002_auto_20200417_1459'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='id',
        ),
        migrations.AlterField(
            model_name='user',
            name='username',
            field=models.CharField(max_length=258, primary_key=True, serialize=False),
        ),
    ]