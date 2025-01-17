# Generated by Django 5.1.4 on 2025-01-17 07:34

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('roles', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Workspace',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255, unique=True)),
            ],
            options={
                'db_table': 'workspaces',
            },
        ),
        migrations.CreateModel(
            name='WorkspaceMember',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('is_active', models.CharField(choices=[('active', 'ACTIVE'), ('inactive', 'INACTIVE')], default='active', max_length=10)),
                ('role', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspace_members', to='roles.role')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='workspace_memberships', to=settings.AUTH_USER_MODEL)),
                ('workspace', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='members', to='workspaces.workspace')),
            ],
            options={
                'db_table': 'workspace_members',
                'indexes': [models.Index(fields=['user', 'workspace'], name='user_workspace_idx')],
                'unique_together': {('workspace', 'user')},
            },
        ),
    ]
