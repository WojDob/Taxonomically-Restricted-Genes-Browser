# Generated by Django 2.2.12 on 2021-08-08 14:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0002_auto_20210808_1423'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxon',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_taxons', to='browser.Taxon'),
        ),
        migrations.AlterField(
            model_name='taxonomicunit',
            name='parent',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='child_taxonomic_unit', to='browser.TaxonomicUnit'),
        ),
    ]
