# Generated by Django 3.2 on 2023-05-10 15:57

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='TestServers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('mac_address', models.CharField(blank=True, max_length=50, null=True)),
                ('hostname', models.CharField(blank=True, default=None, max_length=100, null=True)),
                ('jenkins_node', models.CharField(blank=True, default=None, max_length=50, null=True)),
                ('ip', models.GenericIPAddressField(blank=True, default=None, null=True, protocol='ipv4')),
                ('ipmi', models.CharField(blank=True, max_length=50, null=True)),
                ('server_os', models.CharField(blank=True, max_length=20, null=True)),
                ('gpu_type', models.CharField(blank=True, default=None, max_length=64, null=True)),
                ('server_type', models.IntegerField(choices=[(0, 'others'), (1, 'x86'), (2, 'kunpeng'), (3, 'ampere')], default=0)),
                ('machine_info', models.CharField(blank=True, default=None, max_length=1024, null=True)),
                ('location', models.CharField(blank=True, max_length=20, null=True)),
                ('create_time', models.DateTimeField(auto_now_add=True)),
                ('update_time', models.DateTimeField(auto_now=True)),
                ('usage', models.FloatField(blank=True, default=0, null=True)),
                ('status', models.IntegerField(choices=[(-1, 'unknown'), (0, 'idle'), (1, 'busy')], default=-1)),
            ],
        ),
    ]
