# Generated by Django 2.2.3 on 2019-07-23 09:26

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('username', models.CharField(max_length=100, primary_key=True, serialize=False)),
                ('password', models.CharField(max_length=50)),
                ('email', models.CharField(max_length=100)),
            ],
        ),
    ]
