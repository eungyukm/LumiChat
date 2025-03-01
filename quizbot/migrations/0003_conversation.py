# Generated by Django 4.2.19 on 2025-02-19 17:27

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('quizbot', '0002_alter_question_category_alter_user_score'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conversation',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('user_input', models.TextField()),
                ('bot_response', models.TextField()),
                ('timestamp', models.DateTimeField(auto_now_add=True)),
            ],
        ),
    ]
