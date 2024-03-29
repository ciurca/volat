# Generated by Django 3.2.5 on 2021-08-01 10:29

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0007_event_organizer'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='volunteer',
            name='contract',
        ),
        migrations.CreateModel(
            name='Contract',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='contracte/')),
                ('event', models.ForeignKey(blank=True, null='Not Added', on_delete=django.db.models.deletion.CASCADE, to='hrm.event')),
                ('volunteer', models.ForeignKey(blank=True, null='Not Added', on_delete=django.db.models.deletion.CASCADE, to='hrm.volunteer')),
            ],
        ),
    ]
