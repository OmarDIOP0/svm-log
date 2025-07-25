# Generated by Django 5.2.3 on 2025-07-25 00:01

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AuthLog',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('timestamp', models.DateTimeField()),
                ('category', models.CharField(max_length=50)),
                ('source_ip', models.GenericIPAddressField()),
                ('username', models.CharField(blank=True, max_length=100, null=True)),
                ('status', models.CharField(max_length=20)),
                ('message', models.TextField()),
                ('raw_log', models.TextField()),
                ('is_malicious', models.BooleanField(default=False)),
            ],
            options={
                'ordering': ['-timestamp'],
            },
        ),
    ]
