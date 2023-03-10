# Generated by Django 4.1.1 on 2022-09-22 09:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('SendEmail', '0008_alter_emaillog_emailid_alter_emaillog_sender'),
    ]

    operations = [
        migrations.CreateModel(
            name='ReceivedEMail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.BooleanField(default=True)),
                ('is_delete', models.BooleanField(default=False)),
                ('created_on', models.DateTimeField(auto_now_add=True)),
                ('updated_on', models.DateTimeField(auto_now=True)),
                ('created_by', models.IntegerField(blank=True, null=True)),
                ('deleted_by', models.IntegerField(blank=True, null=True)),
                ('emailid', models.EmailField(max_length=254)),
                ('subject', models.CharField(max_length=255)),
                ('body', models.CharField(max_length=255)),
                ('date', models.DateField()),
            ],
            options={
                'abstract': False,
            },
        ),
    ]
