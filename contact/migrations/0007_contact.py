# Generated by Django 3.2.5 on 2021-07-31 11:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('contact', '0006_alter_feedback_user'),
    ]

    operations = [
        migrations.CreateModel(
            name='Contact',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('subject', models.CharField(blank=True, max_length=50, null=True)),
                ('message', models.TextField(max_length=2000)),
                ('email', models.EmailField(max_length=254)),
                ('user', models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='contact', to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name_plural': 'Contact',
            },
        ),
    ]
