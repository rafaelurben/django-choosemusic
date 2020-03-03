# Generated by Django 3.0.3 on 2020-02-29 22:55

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('choosemusic', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='einreichung',
            name='status',
            field=models.CharField(choices=[('playlist', 'In der Playlist'), ('play', 'Spielt gerade'), ('wait', 'Auf Überprüfung warten...'), ('passed', 'Schon vorbei'), ('forbidden', 'Wurde nicht zugelassen')], default='wait', max_length=20, verbose_name='Status'),
        ),
    ]
