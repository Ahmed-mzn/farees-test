# Generated by Django 4.2.2 on 2024-09-11 19:33

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0007_alter_branch_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='newuser',
            name='role',
            field=models.CharField(choices=[('ADMIN', 'ADMIN'), ('COACH', 'COACH'), ('PARENT', 'PARENT')], max_length=20),
        ),
    ]
