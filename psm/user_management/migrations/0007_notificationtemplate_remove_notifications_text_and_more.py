# Generated by Django 4.0.3 on 2022-07-06 17:10

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('entities', '0001_initial'),
        ('financial', '0007_alter_typologyiimonthlystats_month'),
        ('internment_management', '0015_activitylog_activity_type'),
        ('user_management', '0006_alter_customuser_user_type'),
    ]

    operations = [
        migrations.CreateModel(
            name='NotificationTemplate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('identifier', models.CharField(max_length=50, unique=True)),
                ('text', models.TextField()),
                ('icon', models.CharField(max_length=30)),
                ('bg_color', models.CharField(max_length=30)),
            ],
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='text',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='type',
        ),
        migrations.RemoveField(
            model_name='notifications',
            name='user',
        ),
        migrations.AddField(
            model_name='notifications',
            name='care_house',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='entities.carehouse'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='display',
            field=models.BooleanField(default=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='modified',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='notifications',
            name='notification_type',
            field=models.CharField(choices=[('referral_creation', 'Criação de Referenciação'), ('referral_opening_indication', 'Indicação de Vaga'), ('referral_evaluation', 'Avaliação de Referenciaçõa'), ('receipt_creation', 'Criação de Recibo'), ('receipt_evaluation', 'Avaliação de Recibo')], default='referral_creation', max_length=27),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifications',
            name='process_type',
            field=models.CharField(choices=[('referral', 'Referenciação'), ('invoice', 'Recibo')], default='referral', max_length=8),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifications',
            name='receipt',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='financial.monthlyinvoice'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='referral',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='internment_management.referral'),
        ),
        migrations.AddField(
            model_name='notifications',
            name='user_type',
            field=models.CharField(choices=[('doctor', 'Institution Psychiatrist'), ('reviewer', 'Referral Reviewer'), ('care_house_staff', 'Care House Staff'), ('financial', 'Financial Staff')], default='doctor', max_length=16),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='notifications',
            name='template',
            field=models.ForeignKey(default='', on_delete=django.db.models.deletion.CASCADE, to='user_management.notificationtemplate'),
            preserve_default=False,
        ),
    ]