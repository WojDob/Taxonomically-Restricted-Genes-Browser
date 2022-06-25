# Generated by Django 3.2.5 on 2022-04-04 16:37

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0014_auto_20211114_1134_squashed_0016_alter_taxon_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='taxonomicallyrestrictedgene',
            name='aggregation',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxonomicallyrestrictedgene',
            name='disorder',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxonomicallyrestrictedgene',
            name='entropy',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxonomicallyrestrictedgene',
            name='length',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='taxonomicallyrestrictedgene',
            name='specific_to',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='taxonomically_restricted_genes', to='browser.taxon'),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='taxonomicallyrestrictedgene',
            name='origin_genome',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='browser.genome'),
        ),
    ]