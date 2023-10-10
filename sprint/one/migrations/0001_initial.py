# Generated by Django 4.2.6 on 2023-10-09 15:34

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Climber',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstname', models.CharField(max_length=50)),
                ('lastname', models.CharField(max_length=50)),
                ('patronymic', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=50)),
                ('number', models.CharField(max_length=50)),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Post',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('data_time', models.DateTimeField(auto_now_add=True)),
                ('cordin', models.CharField(max_length=50)),
                ('height', models.CharField(max_length=50)),
                ('text', models.TextField(max_length=3000)),
                ('image', models.ImageField(upload_to='images/')),
                ('post_Author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='one.climber')),
            ],
        ),
    ]