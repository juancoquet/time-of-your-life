# Generated by Django 3.2.5 on 2021-07-29 11:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('contact', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='feedback',
            name='message',
            field=models.TextField(default='text', max_length=2000),
            preserve_default=False,
        ),
    ]
