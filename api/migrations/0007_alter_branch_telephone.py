# Generated by Django 4.2.2 on 2024-09-11 19:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_alter_branch_telephone'),
    ]

    operations = [
        migrations.AlterField(
            model_name='branch',
            name='telephone',
            field=models.IntegerField(default=0, unique=True),
            preserve_default=False,
        ),
    ]
