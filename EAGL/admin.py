from django.contrib import admin
from .models import VillagerDetail,GoatDetails,InsuranceClaim,Vaccine

# Register your models here.
admin.site.register(VillagerDetail)
admin.site.register(GoatDetails)
admin.site.register(InsuranceClaim)
admin.site.register(Vaccine)
