# Generated by Django 4.2.3 on 2023-08-04 02:36

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('notices', '0002_alter_notice_date'),
    ]

    operations = [
        migrations.CreateModel(
            name='Updates',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('when', models.DateTimeField()),
            ],
        ),
    ]