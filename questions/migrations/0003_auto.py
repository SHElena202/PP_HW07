import django
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL), ('questions', '0002_votes')]
    operations = [
        migrations.CreateModel(
            name='AnswerVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
            ],
            options={
                'verbose_name': 'Answer vote',
                'verbose_name_plural': 'Answer votes',
            },
        ),
        migrations.CreateModel(
            name='QuestionVotes',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Question vote',
                'verbose_name_plural': 'Question votes',
            },
        ),
        migrations.AlterField(
            model_name='answers',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
        migrations.DeleteModel(
            name='Votes',
        ),
        migrations.AddField(
            model_name='questionvotes',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Questions'),
        ),
        migrations.AddField(
            model_name='answervotes',
            name='answer',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Answers'),
        ),
        migrations.AddField(
            model_name='answervotes',
            name='author',
            field=models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL),
        ),
    ]