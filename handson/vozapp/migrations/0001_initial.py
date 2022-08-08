# Generated by Django 4.1 on 2022-08-08 00:04

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Employee',
            fields=[
                ('id', models.BigIntegerField(primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=120)),
                ('salary', models.BigIntegerField()),
            ],
            options={
                'db_table': 'employee',
                'managed': False,
            },
        ),
    ]
