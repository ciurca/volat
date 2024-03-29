# Generated by Django 3.2.5 on 2021-07-31 14:24

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0006_auto_20210728_0357'),
    ]

    operations = [
        migrations.CreateModel(
            name='Organizer',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=30)),
            ],
        ),
        migrations.CreateModel(
            name='Event',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=30)),
                ('organizer', models.ForeignKey(blank=True, null='Not Added', on_delete=django.db.models.deletion.CASCADE, to='hrm.organizer')),
                ('volunteers', models.ManyToManyField(to='hrm.Volunteer')),
            ],
        ),
    ]
