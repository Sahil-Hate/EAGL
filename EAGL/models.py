from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class VillagerDetail(models.Model):
    username = models.CharField(max_length=255,unique=True)
    email = models.EmailField(max_length=255,unique=True)
    phone_number = models.CharField(max_length=10)
    hamlet = models.CharField(max_length=255)
    block_number = models.CharField(max_length=255)
    latitude = models.CharField(max_length=255)
    longitude = models.CharField(max_length=255)
    po_number = models.CharField(max_length=255)
    

    def __str__(self):
        return self.username

class GoatDetails(models.Model):
    user = models.ForeignKey(VillagerDetail,on_delete=models.CASCADE)
    goat_gender = models.CharField(max_length=50)
    tag_number = models.CharField(max_length=255,unique=True)
    policy_number = models.CharField(max_length=255)
    is_alive = models.BooleanField(default=True)
    goat_hand_over_date = models.DateField(null=True,blank=True) 

    def __str__(self):
        return str(self.user) + "- Goat(" + self.tag_number + ")"

CHOICES = (
    ("Yes", "yes"),
    ("No", "no"),
)

import os
def get_upload_path1(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("panchnama_doc",ext)
    return os.path.join("user_" + str(instance.goat.user), filename)

def get_upload_path2(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("police_doc",ext)
    return os.path.join("user_" + str(instance.goat.user), filename)

def get_upload_path3(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("sarpanch_doc",ext)
    return os.path.join("user_" + str(instance.goat.user), filename)

def get_upload_path4(instance, filename):
    ext = filename.split('.')[-1]
    filename='{}.{}'.format("pm_doc",ext)
    return os.path.join("user_" + str(instance.goat.user), filename)

class InsuranceClaim(models.Model):
    goat = models.ForeignKey(GoatDetails,on_delete=models.CASCADE)
    death_place = models.CharField(max_length=255,null=True,blank=True)
    death_date = models.DateField(null=True,blank=True)       #date 
    death_time  = models.CharField(null=True,blank=True,max_length=255)  #time
    toll_free_no = models.CharField(max_length=255,null=True,blank=True)
    intimation = models.CharField(max_length=255,null=True,blank=True)   #date-time
    panchnama_doc = models.FileField(upload_to=get_upload_path1,blank=True, null=True)
    police_doc = models.FileField(upload_to=get_upload_path2,blank=True, null=True)
    sarpanch_doc = models.FileField(upload_to=get_upload_path3,blank=True, null=True)
    pm_doc = models.FileField(upload_to=get_upload_path4,blank=True, null=True)
    submission_claim_date = models.DateField(null=True,blank=True)  #date
    submitted_person = models.CharField(max_length=255, null=True,blank=True)
    claim_number = models.CharField(max_length=255, null=True,blank=True)
    claim_settlement_date = models.DateField(null=True,blank=True)  #date
    neft_intimation_date = models.DateField(null=True,blank=True)  #date
    goat_replacement_date = models.DateField(null=True,blank=True)  #date
    replaced_tag_number = models.CharField(max_length=255,null=True,blank=True)
    claim_status = models.BooleanField()

    def __str__(self):
        return str(self.goat.user) + "-Goat(" + self.goat.tag_number + ")"


class Vaccine(models.Model):
    goat = models.ForeignKey(GoatDetails,on_delete=models.CASCADE)
    deworming_date = models.DateField(null=True,blank=True) 
    ppr_date = models.DateField(null=True,blank=True) 
    etv_date = models.DateField(null=True,blank=True) 
    etv_booster_date = models.DateField(null=True,blank=True) 
    anthrax_date = models.DateField(null=True,blank=True) 
    enterotoxamia_date = models.DateField(null=True,blank=True) 
    fmd_date = models.DateField(null=True,blank=True) 
    hs_bq_date = models.DateField(null=True,blank=True) 
    goat_pox_date = models.DateField(null=True,blank=True) 
    ccpr_date = models.DateField(null=True,blank=True) 

    def __str__(self):
        return str(self.goat.user) + "-Goat_Vaccine(" + self.goat.tag_number + ")"
     
