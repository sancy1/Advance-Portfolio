# Generated by Django 4.2.4 on 2023-09-06 20:09

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('App', '0008_blog_favourites'),
    ]

    operations = [
        migrations.CreateModel(
            name='Subscribe',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('document', models.FileField(blank=True, null=True, upload_to='document/')),
            ],
        ),
    ]
