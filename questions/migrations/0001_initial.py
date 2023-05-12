from django.conf import settings
from django.db import migrations
from django.db.models import AutoField, CharField, TextField, DateTimeField, OneToOneField, ManyToManyField, ForeignKey
from django.template.backends import django


class Migration(migrations.Migration):

    initial = True
    dependencies = [migrations.swappable_dependency(settings.AUTH_USER_MODEL)]
    operations = [
        migrations.CreateModel(
            name='Tags',
            fields=[
                ('id', AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', CharField(max_length=50)),
            ],
            options={'verbose_name': 'Tag', 'verbose_name_plural': 'Tags'},
        ),
        migrations.CreateModel(
            name='Questions',
            fields=[
                ('id', AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', CharField(max_length=50)),
                ('body', TextField()),
                ('create_date', DateTimeField(auto_now_add=True)),
                ('author', OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('tags', ManyToManyField(to='questions.Tags')),
            ],
            options={'verbose_name': 'Question', 'verbose_name_plural': 'Questions'},
        ),
        migrations.CreateModel(
            name='Answers',
            fields=[
                ('id', AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('body', TextField(max_length=1000)),
                ('create_date', DateTimeField(auto_now_add=True)),
                ('author', OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('question', ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Questions')),
            ],
            options={'verbose_name': 'Answer', 'verbose_name_plural': 'Answers'},
        ),
    ]



