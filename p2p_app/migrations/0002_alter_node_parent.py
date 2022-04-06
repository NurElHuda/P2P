# Generated by Django 4.0.3 on 2022-04-04 19:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('p2p_app', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='node',
            name='parent',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='children', to='p2p_app.node'),
        ),
    ]