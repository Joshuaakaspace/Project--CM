# Generated by Django 4.1.5 on 2023-04-16 12:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('django_apis_app', '0004_alter_table1_id_alter_table2_id_alter_table3_id'),
    ]

    operations = [
        migrations.AlterField(
            model_name='table4',
            name='legalentity',
            field=models.BooleanField(default=False),
        ),
        migrations.AlterField(
            model_name='table4',
            name='override',
            field=models.BooleanField(default=False),
        ),
    ]
