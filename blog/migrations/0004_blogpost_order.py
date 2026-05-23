from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0003_alter_blogpost_image'),
    ]

    operations = [
        migrations.AddField(
            model_name='blogpost',
            name='order',
            field=models.IntegerField(default=0, verbose_name='Sıralama (kucuk=ust)'),
        ),
        migrations.AlterModelOptions(
            name='blogpost',
            options={'ordering': ['order', '-created_at'], 'verbose_name': 'Blog Post', 'verbose_name_plural': 'Blog Posts'},
        ),
    ]
