# Generated by Django 2.0.6 on 2018-06-11 11:56

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('forum', '0005_auto_20180611_1354'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='post',
            name='thread_id',
        ),
        migrations.RemoveField(
            model_name='post',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='topic_id',
        ),
        migrations.RemoveField(
            model_name='thread',
            name='user_id',
        ),
        migrations.RemoveField(
            model_name='topic',
            name='user_id',
        ),
        migrations.DeleteModel(
            name='Post',
        ),
        migrations.DeleteModel(
            name='Thread',
        ),
        migrations.DeleteModel(
            name='Topic',
        ),
    ]
