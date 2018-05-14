# Generated by Django 2.0.4 on 2018-05-13 16:15

from django.db import migrations, models
import django.db.models.deletion
import jsonfield.fields


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='PosiblePerson',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gender', models.CharField(max_length=10, null=True)),
                ('dob', models.DateField(null=True)),
                ('jobs', jsonfield.fields.JSONField(null=True)),
                ('addresses', jsonfield.fields.JSONField(null=True)),
                ('educations', jsonfield.fields.JSONField(null=True)),
                ('ethnicities', jsonfield.fields.JSONField(null=True)),
                ('phones', jsonfield.fields.JSONField(null=True)),
                ('emails', jsonfield.fields.JSONField(null=True)),
                ('names', jsonfield.fields.JSONField(null=True)),
                ('images', jsonfield.fields.JSONField(null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchInfo',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=256, null=True)),
                ('created', models.DateTimeField(auto_now_add=True)),
                ('image', models.CharField(max_length=256, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='SearchResult',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('person_name', models.CharField(max_length=256)),
                ('search_info', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='search_results', to='engine.SearchInfo')),
            ],
        ),
        migrations.AddField(
            model_name='posibleperson',
            name='search_result',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='posible_persons', to='engine.SearchResult'),
        ),
    ]