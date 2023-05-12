from django.conf import settings
from django.db import migrations
from django.db.models import ForeignKey, OneToOneField, AutoField, DateTimeField
from django.template.backends import django


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('questions', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Votes',
            fields=[
                ('id', AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('create_date', DateTimeField(auto_now_add=True)),
                ('answer', ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Answers')),
                ('author', OneToOneField(on_delete=django.db.models.deletion.DO_NOTHING, to=settings.AUTH_USER_MODEL)),
                ('question', ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='questions.Questions')),
            ],
            options={'verbose_name': 'Vote', 'verbose_name_plural': 'Votes'},
        ),
    ]