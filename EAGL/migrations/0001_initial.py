# Generated by Django 3.2.4 on 2022-02-19 18:45

import EAGL.models
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='GoatDetails',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('goat_gender', models.CharField(max_length=50)),
                ('tag_number', models.CharField(max_length=255, unique=True)),
                ('policy_number', models.CharField(max_length=255)),
                ('is_alive', models.BooleanField(default=True)),
                ('goat_hand_over_date', models.DateField(blank=True, null=True)),
            ],
        ),
        migrations.CreateModel(
            name='VillagerDetail',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('username', models.CharField(max_length=255, unique=True)),
                ('email', models.EmailField(max_length=255, unique=True)),
                ('phone_number', models.CharField(max_length=10)),
                ('hamlet', models.CharField(max_length=255)),
                ('block_number', models.CharField(max_length=255)),
                ('latitude', models.CharField(max_length=255)),
                ('longitude', models.CharField(max_length=255)),
                ('po_number', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Vaccine',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('deworming_date', models.DateField(blank=True, null=True)),
                ('ppr_date', models.DateField(blank=True, null=True)),
                ('etv_date', models.DateField(blank=True, null=True)),
                ('etv_booster_date', models.DateField(blank=True, null=True)),
                ('anthrax_date', models.DateField(blank=True, null=True)),
                ('enterotoxamia_date', models.DateField(blank=True, null=True)),
                ('fmd_date', models.DateField(blank=True, null=True)),
                ('hs_bq_date', models.DateField(blank=True, null=True)),
                ('goat_pox_date', models.DateField(blank=True, null=True)),
                ('ccpr_date', models.DateField(blank=True, null=True)),
                ('goat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAGL.goatdetails')),
            ],
        ),
        migrations.CreateModel(
            name='InsuranceClaim',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('death_place', models.CharField(blank=True, max_length=255, null=True)),
                ('death_date', models.DateField(blank=True, null=True)),
                ('death_time', models.CharField(blank=True, max_length=255, null=True)),
                ('toll_free_no', models.CharField(blank=True, max_length=255, null=True)),
                ('intimation', models.CharField(blank=True, max_length=255, null=True)),
                ('panchnama_doc', models.FileField(blank=True, null=True, upload_to=EAGL.models.get_upload_path1)),
                ('police_doc', models.FileField(blank=True, null=True, upload_to=EAGL.models.get_upload_path2)),
                ('sarpanch_doc', models.FileField(blank=True, null=True, upload_to=EAGL.models.get_upload_path3)),
                ('pm_doc', models.FileField(blank=True, null=True, upload_to=EAGL.models.get_upload_path4)),
                ('submission_claim_date', models.DateField(blank=True, null=True)),
                ('submitted_person', models.CharField(blank=True, max_length=255, null=True)),
                ('claim_number', models.CharField(blank=True, max_length=255, null=True)),
                ('claim_settlement_date', models.DateField(blank=True, null=True)),
                ('neft_intimation_date', models.DateField(blank=True, null=True)),
                ('goat_replacement_date', models.DateField(blank=True, null=True)),
                ('replaced_tag_number', models.CharField(blank=True, max_length=255, null=True)),
                ('claim_status', models.BooleanField()),
                ('goat', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAGL.goatdetails')),
            ],
        ),
        migrations.AddField(
            model_name='goatdetails',
            name='user',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='EAGL.villagerdetail'),
        ),
    ]
