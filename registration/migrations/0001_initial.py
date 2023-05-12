from django.db import migrations
from django.forms import models


class Migration(migrations.Migration):
    initial = True
    dependencies = []
    operations = [
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.AutoField(auto_creted=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('email', models.EmailField(max_length=250, null=True, unique=True)),
                ('nickname', models.CharField(max_length=50, unique=True)),
                ('photo', models.CharField(max_length=50)),
                ('date_of_reg', models.DateField()),
            ],
            options={'verbose_name': 'User', 'verbose_name_plural': 'Users'},
        ),
    ]
