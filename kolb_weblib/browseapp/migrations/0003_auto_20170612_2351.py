# Generated by Django 2.0.dev20170509185503 on 2017-06-12 23:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('browseapp', '0002_materialwebprocesado_codigo_fuente'),
    ]

    operations = [
        migrations.AlterField(
            model_name='materialwebprocesado',
            name='codigo_fuente',
            field=models.TextField(default='', verbose_name='codigo_fuente'),
        ),
    ]
