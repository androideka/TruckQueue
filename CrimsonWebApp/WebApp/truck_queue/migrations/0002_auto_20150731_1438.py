# -*- coding: utf-8 -*-
from __future__ import unicode_literals

import datetime
from django.db import migrations, models
from django.utils.timezone import utc


class Migration(migrations.Migration):

    dependencies = [
        ('truck_queue', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='OpenOrders',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=200)),
            ],
        ),
        migrations.RemoveField(
            model_name='employee',
            name='email',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='first_name',
        ),
        migrations.RemoveField(
            model_name='employee',
            name='last_name',
        ),
        migrations.AddField(
            model_name='employee',
            name='activation_number',
            field=models.IntegerField(default=0),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='phone',
            field=models.IntegerField(default=1234),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='employee',
            name='strikes',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='rating',
            name='date',
            field=models.DateField(default=datetime.datetime(2015, 7, 31, 14, 38, 15, 620391, tzinfo=utc)),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='rating',
            name='description',
            field=models.CharField(default='none', max_length=200),
            preserve_default=False,
        ),
    ]
