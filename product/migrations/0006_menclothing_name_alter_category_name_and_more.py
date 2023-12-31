# Generated by Django 4.2.1 on 2023-10-24 05:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0005_category_alter_menclothing_category'),
    ]

    operations = [
        migrations.AddField(
            model_name='menclothing',
            name='name',
            field=models.CharField(default=0, max_length=100),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='category',
            name='name',
            field=models.CharField(max_length=100),
        ),
        migrations.AlterField(
            model_name='menclothing',
            name='brand',
            field=models.CharField(max_length=20),
        ),
        migrations.AlterField(
            model_name='menclothing',
            name='color',
            field=models.CharField(max_length=50),
        ),
        migrations.AlterField(
            model_name='menclothing',
            name='image',
            field=models.ImageField(upload_to='clothing_images'),
        ),
        migrations.AlterField(
            model_name='menclothing',
            name='size',
            field=models.CharField(max_length=20),
        ),
    ]
