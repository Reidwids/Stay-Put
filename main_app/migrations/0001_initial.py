# Generated by Django 4.0.2 on 2022-04-01 19:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='RealEstate',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('country', models.CharField(max_length=20)),
                ('city', models.CharField(max_length=20)),
                ('address', models.TextField(max_length=250)),
                ('postalCode', models.CharField(max_length=7)),
                ('price', models.IntegerField()),
                ('buildingType', models.CharField(choices=[('C', 'Condo'), ('T', 'Townhouse'), ('S', 'Semi-Detached'), ('H', 'House')], default='C', max_length=1)),
                ('bedrooms', models.IntegerField()),
                ('bathrooms', models.IntegerField()),
                ('parkingSpots', models.IntegerField()),
                ('sqft', models.IntegerField()),
                ('listingDate', models.DateField(verbose_name='Listing Date')),
                ('realtor', models.IntegerField()),
            ],
        ),
        migrations.CreateModel(
            name='User',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('firstName', models.CharField(max_length=100)),
                ('lastName', models.CharField(max_length=100)),
                ('image', models.CharField(blank=True, default=None, max_length=2000, null=True)),
                ('licenseNumber', models.IntegerField()),
                ('phoneNumber', models.IntegerField()),
                ('email', models.EmailField(max_length=254)),
                ('isAgent', models.BooleanField(default=True)),
                ('isAdmin', models.BooleanField(default=False)),
            ],
        ),
        migrations.CreateModel(
            name='Photo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('url', models.CharField(max_length=200)),
                ('real_estate', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='main_app.realestate')),
            ],
        ),
    ]
