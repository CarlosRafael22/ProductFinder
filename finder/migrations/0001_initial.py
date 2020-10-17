# Generated by Django 3.1.2 on 2020-10-17 19:19

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=200)),
                ('price', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('link', models.CharField(blank=True, max_length=200, null=True)),
                ('image_url', models.CharField(blank=True, max_length=200, null=True)),
                ('store', models.CharField(max_length=50)),
                ('category', models.CharField(blank=True, max_length=50, null=True)),
            ],
        ),
    ]