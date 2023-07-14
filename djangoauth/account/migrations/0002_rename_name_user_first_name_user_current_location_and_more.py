# Generated by Django 4.2.3 on 2023-07-13 09:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user',
            old_name='name',
            new_name='first_name',
        ),
        migrations.AddField(
            model_name='user',
            name='current_location',
            field=models.CharField(choices=[('Abia', 'Abia (Umuahia)'), ('Adamawa', 'Adamawa (Yola)'), ('Akwa Ibom', 'Akwa Ibom (Uyo)'), ('Anambra', 'Anambra (Awka)'), ('Bauchi', 'Bauchi (Bauchi)'), ('Bayelsa', 'Bayelsa (Yenagoa)'), ('Benue', 'Benue (Makurdi)'), ('Borno', 'Borno (Maiduguri)'), ('Cross River', 'Cross River (Calabar)'), ('Delta', 'Delta (Asaba)'), ('Ebonyi', 'Ebonyi (Abakaliki)'), ('Edo', 'Edo (Benin City)'), ('Ekiti', 'Ekiti (Ado Ekiti)'), ('Enugu', 'Enugu (Enugu)'), ('Gombe', 'Gombe (Gombe)'), ('Imo', 'Imo (Owerri)'), ('Jigawa', 'Jigawa (Dutse)'), ('Kaduna', 'Kaduna (Kaduna)'), ('Kano', 'Kano (Kano)'), ('Katsina', 'Katsina (Katsina)'), ('Kebbi', 'Kebbi (Birnin Kebbi)'), ('Kogi', 'Kogi (Lokoja)'), ('Kwara', 'Kwara (Ilorin)'), ('Lagos', 'Lagos (Ikeja)'), ('Nasarawa', 'Nasarawa (Lafia)'), ('Niger', 'Niger (Minna)'), ('Ogun', 'Ogun (Abeokuta)'), ('Ondo', 'Ondo (Akure)'), ('Osun', 'Osun (Osogbo)'), ('Oyo', 'Oyo (Ibadan)'), ('Plateau', 'Plateau (Jos)'), ('Rivers', 'Rivers (Port Harcourt)'), ('Sokoto', 'Sokoto (Sokoto)'), ('Taraba', 'Taraba (Jalingo)'), ('Yobe', 'Yobe (Damaturu)'), ('Zamfara', 'Zamfara (Gusau)')], default='Abia', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='intern_category',
            field=models.CharField(choices=[('About to graduate', 'About to graduate'), ('Just graduated', 'Just graduated'), ('Looking to change fields', 'Looking to change fields')], default='About to graduate', max_length=100),
        ),
        migrations.AddField(
            model_name='user',
            name='last_name',
            field=models.CharField(max_length=100, null=True),
        ),
        migrations.AddField(
            model_name='user',
            name='phone_number',
            field=models.IntegerField(default=None, null=True),
        ),
    ]
