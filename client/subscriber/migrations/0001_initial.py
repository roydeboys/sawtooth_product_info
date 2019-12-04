# Generated by Django 2.2.7 on 2019-11-26 09:23

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Block',
            fields=[
                ('block_number', models.BigIntegerField(primary_key=True, serialize=False)),
                ('block_id', models.CharField(max_length=500)),
            ],
        ),
        migrations.CreateModel(
            name='Record',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('record_id', models.CharField(max_length=500)),
                ('start_block_number', models.BigIntegerField()),
                ('end_block_number', models.BigIntegerField()),
            ],
        ),
    ]