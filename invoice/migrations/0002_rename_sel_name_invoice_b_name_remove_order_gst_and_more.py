# Generated by Django 4.0 on 2022-01-12 20:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('invoice', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='invoice',
            old_name='sel_name',
            new_name='b_name',
        ),
        migrations.RemoveField(
            model_name='order',
            name='gst',
        ),
        migrations.AddField(
            model_name='invoice',
            name='b_address',
            field=models.TextField(default='unknown'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='b_phone',
            field=models.CharField(default='+91 7708470662', max_length=15),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='s_address',
            field=models.TextField(default='No.12, Sellaperumalpet, Lawspet, Puducherry-605 008.'),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='s_name',
            field=models.CharField(default='Manju Groups', max_length=100),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='s_phone',
            field=models.CharField(default='+91 7094870702', max_length=13),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='invoice',
            name='total',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='order',
            name='quantity',
            field=models.PositiveIntegerField(default=1),
        ),
        migrations.AddField(
            model_name='order',
            name='tax',
            field=models.FloatField(default=12.8),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='order',
            name='price',
            field=models.PositiveIntegerField(),
        ),
    ]
