# Generated by Django 3.2.5 on 2021-08-22 14:07

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0005_auto_20210822_1406'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='taxon',
            name='child',
        ),
        migrations.AddField(
            model_name='taxon',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_taxons', to='browser.taxon'),
        ),
    ]
