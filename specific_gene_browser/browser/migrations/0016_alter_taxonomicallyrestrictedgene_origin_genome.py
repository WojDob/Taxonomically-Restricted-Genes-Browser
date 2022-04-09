# Generated by Django 3.2.5 on 2022-04-09 14:51

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('browser', '0015_auto_20220404_1637'),
    ]

    operations = [
        migrations.AlterField(
            model_name='taxonomicallyrestrictedgene',
            name='origin_genome',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='originating_trgs', to='browser.genome'),
        ),
    ]
