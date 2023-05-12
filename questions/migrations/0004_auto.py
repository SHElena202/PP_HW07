from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ('questions', '0003_auto'),
    ]

    operations = [
        migrations.AlterField(
            model_name='questions',
            name='body',
            field=models.TextField(verbose_name='Текст вопроса'),
        ),
        migrations.AlterField(
            model_name='questions',
            name='title',
            field=models.CharField(max_length=50, verbose_name='Заголовок'),
        ),
    ]