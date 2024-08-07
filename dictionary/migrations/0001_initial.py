# Generated by Django 3.2.25 on 2024-07-24 12:28

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='KanjiElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('keb', models.CharField(max_length=255)),
                ('ke_inf', models.TextField(blank=True, null=True)),
                ('ke_pri', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='ReadingElement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reb', models.CharField(max_length=255)),
                ('re_nokanji', models.BooleanField(default=False)),
                ('re_refr', models.TextField(blank=True, null=True)),
                ('re_inf', models.TextField(blank=True, null=True)),
                ('re_pri', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Sense',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('gloss', models.TextField()),
                ('pos', models.TextField(blank=True, null=True)),
                ('xref', models.TextField(blank=True, null=True)),
                ('ant', models.TextField(blank=True, null=True)),
                ('field', models.TextField(blank=True, null=True)),
                ('lsource', models.TextField(blank=True, null=True)),
                ('misc', models.TextField(blank=True, null=True)),
                ('example', models.TextField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='Entry',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ent_seq', models.IntegerField(unique=True)),
                ('keb_elem', models.ManyToManyField(blank=True, to='dictionary.KanjiElement')),
                ('reb_elem', models.ManyToManyField(to='dictionary.ReadingElement')),
                ('sense', models.ManyToManyField(to='dictionary.Sense')),
            ],
        ),
    ]
