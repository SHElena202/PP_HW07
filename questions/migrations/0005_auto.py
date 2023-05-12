from django.db import migrations
from django.db.migrations.operations import models


class Migration(migrations.Migration):
    dependencies = [
        ('questions', '0004_auto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='answers',
            name='body',
            field=models.TextField(max_length=500, verbose_name='Ваш ответ'),
        ),
    ]