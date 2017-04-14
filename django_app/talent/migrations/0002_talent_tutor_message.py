from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('talent', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='talent',
            name='tutor_message',
            field=models.TextField(blank=True),
        ),
    ]
