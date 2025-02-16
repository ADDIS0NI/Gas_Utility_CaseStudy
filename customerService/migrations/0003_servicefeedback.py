# Generated by Django 4.2.6 on 2025-01-20 14:28

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('customerService', '0002_servicerequest_assigned_team_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='ServiceFeedback',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('rating', models.IntegerField(choices=[(1, '★'), (2, '★★'), (3, '★★★'), (4, '★★★★'), (5, '★★★★★')])),
                ('comment', models.TextField()),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('service_request', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='feedback', to='customerService.servicerequest')),
            ],
        ),
    ]
