# Generated by Django 3.2.5 on 2021-08-17 10:48

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('hrm', '0011_auto_20210817_1325'),
    ]

    operations = [
        migrations.CreateModel(
            name='LegalTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('file', models.FileField(blank=True, null=True, upload_to='important/contract_templates/')),
                ('type', models.CharField(choices=[('Contract Voluntariat', 'Contract Voluntariat'), ('GDPR', 'GDPR'), ('Acord Tutore', 'Acord Tutore')], max_length=30)),
                ('event', models.ForeignKey(null='Not Added', on_delete=django.db.models.deletion.CASCADE, to='hrm.event')),
            ],
        ),
    ]