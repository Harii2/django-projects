# Generated by Django 3.0 on 2023-08-23 05:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('assignment2', '0002_cast_is_debut_movie'),
    ]

    operations = [
        migrations.CreateModel(
            name='Gender',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=50)),
            ],
        ),
    ]