from django.shortcuts import render, redirect
from django.contrib.auth.models import User,auth
from django.contrib import messages
from .models import VillagerDetail,GoatDetails,InsuranceClaim,Vaccine
from django.core.files.storage import FileSystemStorage
from django.utils.datastructures import MultiValueDictKeyError
from django.db.models import Count
from  django.core.exceptions import ValidationError
from rest_framework import generics,mixins,status
from .serializers import VillagerDetailSerializer,GoatDetailsSerializer
from rest_framework.decorators import api_view
from django.http import JsonResponse
from rest_framework.response import Response


# Create your views here.
def index(request):
    return render(request,'index.html')

def logout(request):
    auth.logout(request)
    return redirect("/")

def login(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = auth.authenticate(username=username,password=password)

        if user is not None:
            auth.login(request,user)
            return redirect('userlist')
        else:
            messages.info(request,'Invalid credentials')
            return redirect('login')
    
    else:
        return render(request,'login.html')

def userlist(request):
    if request.user.is_authenticated:
        map_chart = []
        goat_count_pie_total = [["Gender","Count"]]
        users = VillagerDetail.objects.all()
        map_details = users.values('username','latitude','longitude')
        # To plot users on a map
        for i in map_details:
            map_chart.append([i['username'],float(i['latitude']),float(i['longitude'])])
        
        goat_genders_total = GoatDetails.objects.values('goat_gender')
        num_goats = len(goat_genders_total)

        result = GoatDetails.objects.values('goat_gender').annotate(dcount=Count('goat_gender')).order_by()
        # To create a pie chart
        for i in result:
            goat_count_pie_total.append([i['goat_gender'],i['dcount']])
        error = ""
        if request.method == 'POST':
            username = request.POST['username'].strip()
            email = request.POST['email'].strip()
            phone_number = request.POST['phone_number'].strip()
            hamlet = request.POST['hamlet'].strip()
            block_number = request.POST['block'].strip()
            latitude = request.POST['latitude'].strip()
            longitude = request.POST['longitude'].strip()
            po_number = request.POST['po_number'].strip()
            if username == "":
                messages.info(request,'Please enter a valid username!')
                error="yes"
            elif email == "":
                messages.info(request,'Please enter a valid email address!')
                error="yes"
            elif User.objects.filter(username=username).exists():
                messages.info(request,'Username already taken! Please enter a different username to proceed')
                error="yes"
            elif User.objects.filter(email=email).exists():
                messages.info(request, 'Email already exists')
                error="yes"
            elif phone_number == "":
                messages.info(request,'Please enter a valid phone number!')
                error="yes"
            elif len(phone_number) != 10:
                messages.info(request, 'Please enter a valid Phone number')
                error="yes"
            elif hamlet == "":
                messages.info(request,'Please enter a valid village!')
                error="yes"
            elif block_number == "":
                messages.info(request,'Please enter a valid block number!')
                error="yes"
            elif latitude == "":
                messages.info(request,'Please enter a valid latitude!')
                error="yes"
            elif longitude == "":
                messages.info(request,'Please enter a valid longitude!')
                error="yes"
            elif po_number == "":
                messages.info(request,'Please enter a valid policy number!')
                error="yes"
            if error!= "":
                return render(request,'userlist.html',{"users":users,"error":error,"map_chart":map_chart,"num_goats":num_goats})
            else:
                villagers_details = VillagerDetail  (username=username,
                email=email,
                phone_number=phone_number,
                hamlet=hamlet,
                block_number=block_number,
                latitude=latitude,
                longitude=longitude,
                po_number=po_number)
                villagers_details.save()
                goat_count_pie = [["Gender","Count"]]
                goat_genders_total = GoatDetails.objects.values('goat_gender')
                result = goat_genders_total.annotate(dcount=Count('goat_gender')).order_by()
                map_chart = []
                map_details = users.values('username','latitude','longitude')
                for i in map_details:
                    map_chart.append([i['username'],float(i['latitude']),float(i['longitude'])])
                messages.info(request,'User Created!')
                return render(request,'userlist.html',{"users":users,"error":error,"goat_count_pie_total":goat_count_pie_total,"map_chart":map_chart,"num_goats":num_goats})
        else:        
            return render(request,'userlist.html',{"users":users,"error":error,"goat_count_pie_total":goat_count_pie_total,"map_chart":map_chart,"num_goats":num_goats})
    else:
        return redirect("login")


def userdetail(request,id):
    if request.user.is_authenticated:
        goat_count_pie = [["Gender","Count"]]
        insurance_pie = [["Status","Count"]]
        user = VillagerDetail.objects.get(id=id)
        goat_set = GoatDetails.objects.filter(user__id=id)
        goat_insurance_all = InsuranceClaim.objects.all()
        ins_user = InsuranceClaim.objects.filter(goat__user = user).values('claim_status')
        insu = InsuranceClaim.objects.filter(goat__user = user)
        insurance_count = len(insu)
        print(goat_set)
        # goat_kids = KidsGoat.objects.all() 
        for i in insu:
            if i.claim_status == True:
                dead_goat = i.goat
                dead_goat.is_alive = False
                dead_goat.save()
        res = ins_user.annotate(dcount=Count('claim_status')).order_by()
        for i in res:
            insurance_pie.append([str(i['claim_status']),i['dcount']])
        goat_set_list = []
        for i in goat_set:
            x = []
            x.append(i)
            x.append(InsuranceClaim.objects.filter(goat=i).exists())
            x.append(Vaccine.objects.filter(goat=i).exists())
            status = InsuranceClaim.objects.filter(goat=i)
            if InsuranceClaim.objects.filter(goat=i).exists():
                for j in status:
                    x.append(j.claim_status)
            else:
                x.append("DOESNOTEXIST")
            goat_set_list.append(x)
        subresult = GoatDetails.objects.filter(user=user).values('goat_gender')
        user_num_goats = len(subresult)
        result = subresult.annotate(dcount=Count('goat_gender')).order_by()
        for i in result:
            goat_count_pie.append([i['goat_gender'],i['dcount']])
        error = ""
        if request.method == 'POST':
            goat_gender = request.POST['gender']
            tag_number = request.POST['tag_number']
            policy_number = request.POST['policy_number']
            goat_hand_over_date = request.POST['goat_hand_over_date']
            if tag_number == "":
                messages.info(request,'Please enter a tag number!')
                error = "yes"
            elif policy_number == "":
                messages.info(request,'Please enter a policy number!')
                error = "yes"
            elif goat_hand_over_date == "":
                goat_hand_over_date = None
            if error!= "":
                return render(request,'userdetails.html',{"user":user,
                "error":error,"goat_count_pie":goat_count_pie,"user_num_goats":user_num_goats,
                "goat_set_list":goat_set_list,"insurance_pie":insurance_pie,"insurance_count":insurance_count})
            else:
                goat_details = GoatDetails.objects.create(user=user,
                goat_gender=goat_gender,
                tag_number=tag_number,
                policy_number=policy_number,
                goat_hand_over_date=goat_hand_over_date)
                goat_details.save()
                goat_count_pie = [["Gender","Count"]]
                insurance_pie = [["Status","Count"]]
                subresult = GoatDetails.objects.filter(user=user).values('goat_gender')
                user_num_goats = len(subresult)
                result = subresult.annotate(dcount=Count('goat_gender')).order_by()
                goat_set_list = []
                goat_set = GoatDetails.objects.filter(user__id=id)
                for i in goat_set:
                    x = []
                    x.append(i)
                    x.append(InsuranceClaim.objects.filter(goat=i).exists())
                    x.append(Vaccine.objects.filter(goat=i).exists())
                    status = InsuranceClaim.objects.filter(goat=i)
                    if InsuranceClaim.objects.filter(goat=i).exists():
                        for j in status:
                            x.append(j.claim_status)
                    else:
                        x.append("DOESNOTEXIST")
                    goat_set_list.append(x)
                for i in result:
                    goat_count_pie.append([i['goat_gender'],i['dcount']])
                ins_user = InsuranceClaim.objects.filter(goat__user = user).values('claim_status')
                res = ins_user.annotate(dcount=Count('claim_status')).order_by()
                insu = InsuranceClaim.objects.filter(goat__user = user)
                for i in insu:
                    if i.claim_status == True:
                        dead_goat = i.goat
                        dead_goat.is_alive = False
                        dead_goat.save()
                for i in res:
                    insurance_pie.append([str(i['claim_status']),i['dcount']])
                return render(request,'userdetail.html',{"user":user,
                "error":error,"goat_count_pie":goat_count_pie,"user_num_goats":user_num_goats,
                "goat_set_list":goat_set_list,"insurance_pie":insurance_pie,"insurance_count":insurance_count})
        else:
            return render(request,'userdetail.html',{"user":user,
            "error":error,"goat_count_pie":goat_count_pie,"user_num_goats":user_num_goats,
            "goat_set_list":goat_set_list,"insurance_pie":insurance_pie,"insurance_count":insurance_count})
    else:
        return redirect("login")


def update_user(request,id):
    user = VillagerDetail.objects.get(id=id)
    if request.method == 'POST':
        username = request.POST['username'].strip()
        email = request.POST['email'].strip()
        phone_number = request.POST['phone_number'].strip()
        hamlet = request.POST['hamlet'].strip()
        block_number = request.POST['block'].strip()
        latitude = request.POST['latitude'].strip()
        longitude = request.POST['longitude'].strip()
        po_number = request.POST['po_number'].strip()
        if username =="" or email =="" or phone_number =="" or hamlet =="" or block_number =="" or latitude =="" or longitude =="" or po_number == "":
            messages.info(request,'Please fill the field')
            return render(request,'update_user.html')
        elif user.username != username:
            user.username = username
        elif user.email != email:
            user.email = email
        elif user.phone_number != phone_number:
            user.phone_number = phone_number
        elif user.hamlet !=hamlet:
            user.hamlet = hamlet
        elif user.block_number != block_number:
            user.block_number = block_number
        elif user.latitude != latitude:
            user.latitude = latitude
        elif user.longitude != longitude:
            user.longitude = longitude
        elif user.po_number != po_number:
            user.po_number = po_number
        user.save()
        return render(request,'update_user.html',{"user":user})
    return render(request,'update_user.html',{"user":user})


def delete_user(request,id):
    user = VillagerDetail.objects.get(id=id)
    if request.method == 'POST':
        user.delete()
        return redirect("userlist")
    return render(request,'delete_user.html',{"user":user})


def insuranceClaim(request,user,id):
    if request.user.is_authenticated:
        user = VillagerDetail.objects.get(username=user)
        goat = GoatDetails.objects.get(id=id)
        if request.method == 'POST':
            death_place = request.POST['death_place'].strip()
            death_date = request.POST.get('death_date')
            death_time = request.POST['death_time'].strip()
            toll_free_no = request.POST['toll_free_no'].strip()
            intimation = request.POST['intimation'].strip()
            panchnama_doc = request.FILES.get('panchnama-file')
            police_doc = request.FILES.get('police-file')
            sarpanch_doc = request.FILES.get('sarpanch-file')
            pm_doc = request.FILES.get('pm_report-file')
            submission_claim_date = request.POST.get('submission_claim_date')
            submitted_person = request.POST['submitted_person'].strip()
            claim_number = request.POST['claim_number'].strip()
            claim_settlement_date = request.POST.get('claim_settlement_date')
            neft_intimation_date = request.POST.get('neft_intimation_date')
            goat_replacement_date = request.POST.get('goat_replacement_date')
            replaced_tag_number = request.POST['replaced_tag_number'].strip()
            claimed = request.POST['claim']
            if death_date:
                death_date = death_date
            else:
                death_date = None
        
            if submission_claim_date:
                submission_claim_date =submission_claim_date
            else: 
                submission_claim_date = None
            
            if claim_settlement_date:
                claim_settlement_date = claim_settlement_date
            else: 
                claim_settlement_date = None

            if neft_intimation_date:
                neft_intimation_date = neft_intimation_date
            else: 
                neft_intimation_date = None

            if goat_replacement_date:
                goat_replacement_date = goat_replacement_date
            else: 
                goat_replacement_date = None
            if panchnama_doc != None:
                try:
                    panchnama_doc = request.FILES['panchnama-file']
                except MultiValueDictKeyError:
                    panchnama_doc = request.FILES['panchnama-file']
            else:
                panchnama_doc = None
            
            if police_doc != None:
                try:
                    police_doc = request.FILES['police-file']
                except MultiValueDictKeyError:
                    police_doc = request.FILES['police-file']
            else:
                police_doc = None
            
            if sarpanch_doc  != None:
                try:
                    sarpanch_doc = request.FILES['sarpanch-file']
                except MultiValueDictKeyError:
                    sarpanch_doc = request.FILES['sarpanch-file']
            else:
                sarpanch_doc = None

            if pm_doc  != None:
                try:
                    pm_doc = request.FILES['pm_report-file']
                except MultiValueDictKeyError:
                    pm_doc = request.FILES['pm_report-file']
            else:
                pm_doc = None

            insurance_claim = InsuranceClaim.objects.create(
                goat=goat,
                death_place=death_place,
                death_date=death_date,
                death_time=death_time,
                toll_free_no=toll_free_no,
                intimation=intimation,
                panchnama_doc=panchnama_doc,
                police_doc=police_doc,
                sarpanch_doc=sarpanch_doc,
                pm_doc=pm_doc,
                submission_claim_date=submission_claim_date,
                submitted_person=submitted_person,
                claim_number=claim_number,
                claim_settlement_date=claim_settlement_date,
                neft_intimation_date=neft_intimation_date,
                goat_replacement_date=goat_replacement_date,
                replaced_tag_number=replaced_tag_number,
                claim_status=claimed
            )
            
            insurance_claim.save()
            return render(request,'insurance_claim.html',{"user":user,"goat":goat})
        else:
            return render(request,'insurance_claim.html',{"user":user,"goat":goat})
    else:
        return redirect("login")


def update_insurance(request,user,id):
    if request.user.is_authenticated:
        user = VillagerDetail.objects.get(username=user)
        goat = GoatDetails.objects.get(id=id)
        goat_insurance = InsuranceClaim.objects.get(goat=goat)
        
        claim_status = goat_insurance.claim_status
        if request.method == 'POST':
            death_place = request.POST['death_place'].strip()
            death_date = request.POST.get('death_date')
            death_time = request.POST['death_time'].strip()
            toll_free_no = request.POST['toll_free_no'].strip()
            intimation = request.POST['intimation'].strip()
            panchnama_doc = request.FILES.get('panchnama-file')
            police_doc = request.FILES.get('police-file')
            sarpanch_doc = request.FILES.get('sarpanch-file')
            pm_doc = request.FILES.get('pm_report-file')
            submission_claim_date = request.POST.get('submission_claim_date')
            submitted_person = request.POST['submitted_person'].strip()
            claim_number = request.POST['claim_number'].strip()
            claim_settlement_date = request.POST.get('claim_settlement_date')
            neft_intimation_date = request.POST.get('neft_intimation_date')
            goat_replacement_date = request.POST.get('goat_replacement_date')
            replaced_tag_number = request.POST['replaced_tag_number'].strip()
            claimed = request.POST['claim']
            claimed = bool(claimed)
            
            if death_date:
                goat_insurance.death_date = death_date
            else:
                death_date = None
        
            if submission_claim_date:
                goat_insurance.submission_claim_date =submission_claim_date
            else: 
                submission_claim_date = None
            
            if claim_settlement_date:
                goat_insurance.claim_settlement_date = claim_settlement_date
            else: 
                claim_settlement_date = None

            if neft_intimation_date:
                goat_insurance.neft_intimation_date = neft_intimation_date
            else: 
                neft_intimation_date = None

            if goat_replacement_date:
                goat_insurance.goat_replacement_date = goat_replacement_date
            else: 
                goat_replacement_date = None
            
            if panchnama_doc != None:
                try:
                    panchnama_doc = request.FILES['panchnama-file']
                except MultiValueDictKeyError:
                    panchnama_doc = request.FILES['panchnama-file']
            else:
                panchnama_doc = None
            
            if police_doc != None:
                try:
                    police_doc = request.FILES['police-file']
                except MultiValueDictKeyError:
                    police_doc = request.FILES['police-file']
            else:
                police_doc = None
            
            if sarpanch_doc  != None:
                try:
                    sarpanch_doc = request.FILES['sarpanch-file']
                except MultiValueDictKeyError:
                    sarpanch_doc = request.FILES['sarpanch-file']
            else:
                sarpanch_doc = None

            if pm_doc  != None:
                try:
                    pm_doc = request.FILES['pm_report-file']
                except MultiValueDictKeyError:
                    pm_doc = request.FILES['pm_report-file']
            else:
                pm_doc = None
            
            if claimed == True:
                goat_insurance.claim_status = True
            else:
                goat_insurance.claim_status = False
            
            if goat_insurance.death_place != death_place:
                goat_insurance.death_place = death_place
            elif goat_insurance.death_date != death_date:
                goat_insurance.death_date = death_date
            elif goat_insurance.death_time != death_time:
                goat_insurance.death_time = death_time
            elif goat_insurance.toll_free_no != toll_free_no:
                goat_insurance.toll_free_no = toll_free_no
            elif goat_insurance.intimation != intimation:
                goat_insurance.intimation = intimation
            elif goat_insurance.panchnama_doc != panchnama_doc:
                goat_insurance.panchnama_doc =panchnama_doc
            elif goat_insurance.police_doc != police_doc:
                goat_insurance.police_doc = police_doc
            elif goat_insurance.sarpanch_doc != sarpanch_doc:
                goat_insurance.sarpanch_doc = sarpanch_doc
            elif goat_insurance.pm_doc != pm_doc:
                goat_insurance.pm_doc = pm_doc
            elif goat_insurance.submission_claim_date != submission_claim_date:
                goat_insurance.submission_claim_date = submission_claim_date
            elif goat_insurance.submitted_person != submitted_person:
                goat_insurance.submitted_person = submitted_person
            elif goat_insurance.claim_number != claim_number:
                goat_insurance.claim_number = claim_number
            elif goat_insurance.claim_settlement_date != claim_settlement_date:
                goat_insurance.claim_settlement_date = claim_settlement_date
            elif goat_insurance.neft_intimation_date != neft_intimation_date:
                goat_insurance.neft_intimation_date = neft_intimation_date
            elif goat_insurance.goat_replacement_date != goat_replacement_date:
                goat_insurance.goat_replacement_date = goat_replacement_date
            elif goat_insurance.replaced_tag_number != replaced_tag_number:
                goat_insurance.replaced_tag_number = replaced_tag_number
            
            claim_status = goat_insurance.claim_status
            goat_insurance.save()

            return render(request,'update_insurance.html',{"user":user,"goat":goat,"goat_insurance":goat_insurance,"claim_status":claim_status})
        return render(request,'update_insurance.html',{"user":user,"goat":goat,"goat_insurance":goat_insurance,"claim_status":claim_status})
    else:
        return redirect("login")

def vaccination(request,user,id):
    if request.user.is_authenticated:
        user = VillagerDetail.objects.get(username=user)
        goat = GoatDetails.objects.get(id=id)
        if request.method == 'POST':
            deworming_date = request.POST['deworming_date']
            ppr_date = request.POST['ppr_date']
            etv_date = request.POST['etv_date']
            etv_booster_date = request.POST['etv_booster_date']
            anthrax_date = request.POST['anthrax_date']
            enterotoxamia_date = request.POST['enterotoxamia_date']
            fmd_date = request.POST['fmd_date']
            hs_bq_date = request.POST['hs_bq_date']
            goat_pox_date = request.POST['goat_pox_date']
            ccpr_date = request.POST['ccpr_date']

            if deworming_date:
                deworming_date = deworming_date
            else:
                deworming_date = None

            if ppr_date:
                ppr_date = ppr_date
            else:
                ppr_date=None
            
            if etv_date:
                etv_date = etv_date
            else:
                etv_date=None
            
            if etv_booster_date:
                etv_booster_date = etv_booster_date
            else:
                etv_booster_date=None

            if anthrax_date:
                anthrax_date = anthrax_date
            else:
                anthrax_date=None
                
            if enterotoxamia_date:
                enterotoxamia_date = enterotoxamia_date
            else:
                enterotoxamia_date=None

            if fmd_date:
                fmd_date = fmd_date
            else:
                fmd_date=None

            if hs_bq_date:
                hs_bq_date = hs_bq_date
            else:
                hs_bq_date=None

            if goat_pox_date:
                goat_pox_date = goat_pox_date
            else:
                goat_pox_date=None

            if ccpr_date:
                ccpr_date = ccpr_date
            else:
                ccpr_date=None
            
            goat_vaccines = Vaccine.objects.create(
                goat=goat,
                deworming_date=deworming_date,
                ppr_date=ppr_date,
                etv_date=etv_date,
                etv_booster_date=etv_booster_date,
                anthrax_date=anthrax_date,
                enterotoxamia_date=enterotoxamia_date,
                fmd_date=fmd_date,
                hs_bq_date=hs_bq_date,
                goat_pox_date=goat_pox_date,
                ccpr_date=ccpr_date
            )
            goat_vaccines.save()
            return render(request,'vaccination.html',{"user":user,"goat":goat})
        else:
            return render(request,'vaccination.html',{"user":user,"goat":goat})
    else:
        return redirect("login")

def update_vaccination(request,user,id):
    if request.user.is_authenticated:
        user = VillagerDetail.objects.get(username=user)
        goat = GoatDetails.objects.get(id=id)
        goat_vaccine = Vaccine.objects.get(goat=goat)
        if request.method == 'POST':
            deworming_date = request.POST['deworming_date']
            ppr_date = request.POST['ppr_date']
            etv_date = request.POST['etv_date']
            etv_booster_date = request.POST['etv_booster_date']
            anthrax_date = request.POST['anthrax_date']
            enterotoxamia_date = request.POST['enterotoxamia_date']
            fmd_date = request.POST['fmd_date']
            hs_bq_date = request.POST['hs_bq_date']
            goat_pox_date = request.POST['goat_pox_date']
            ccpr_date = request.POST['ccpr_date']

            if deworming_date:
                goat_vaccine.deworming_date = deworming_date
            else:
                goat_vaccine.deworming_date = None

            if ppr_date:
                goat_vaccine.ppr_date = ppr_date
            else:
                goat_vaccine.ppr_date=None
            
            if etv_date:
                goat_vaccine.etv_date = etv_date
            else:
                goat_vaccine.etv_date=None
            
            if etv_booster_date:
                goat_vaccine.etv_booster_date = etv_booster_date
            else:
                goat_vaccine.etv_booster_date=None

            if anthrax_date:
                goat_vaccine.anthrax_date = anthrax_date
            else:
                goat_vaccine.anthrax_date=None
                
            if enterotoxamia_date:
                goat_vaccine.enterotoxamia_date = enterotoxamia_date
            else:
                goat_vaccine.enterotoxamia_date=None

            if fmd_date:
                goat_vaccine.fmd_date = fmd_date
            else:
                goat_vaccine.fmd_date=None

            if hs_bq_date:
                goat_vaccine.hs_bq_date = hs_bq_date
            else:
                goat_vaccine.hs_bq_date=None

            if goat_pox_date:
                goat_vaccine.goat_pox_date = goat_pox_date
            else:
                goat_vaccine.goat_pox_date=None

            if ccpr_date:
                goat_vaccine.ccpr_date = ccpr_date
            else:
                goat_vaccine.ccpr_date=None
            
            goat_vaccine.save()
            return render(request,'update_vaccination.html',{"user":user,"goat":goat,"goat_vaccine":goat_vaccine})
        else:
            return render(request,'update_vaccination.html',{"user":user,"goat":goat,"goat_vaccine":goat_vaccine})
    else:
        return redirect("login")
    

class VillagerDetailCreate(mixins.CreateModelMixin, generics.GenericAPIView):
    queryset = VillagerDetail.objects.all()
    serializer_class = VillagerDetailSerializer
    
    def post(self, request, *args, **kwargs):
        return self.create(request, *args, **kwargs)

# class GoatDetailsCreate(mixins.CreateModelMixin, generics.GenericAPIView):
#     queryset = GoatDetails.objects.all()
#     serializer_class = GoatDetailsSerializer
    
#     def post(self, request, *args, **kwargs):
#         return self.create(request, *args, **kwargs)


@api_view(["GET"])
def VillagerList(request):
    if request.method=="GET":
        variable = VillagerDetail.objects.all()
        villagers = []
        for i in variable:
            villagers.append(i.username)
        return JsonResponse(
            villagers,
            status=status.HTTP_200_OK,
            safe=False,
        )
    else:
        return JsonResponse(
            data={"Message": "Only GET request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )

@api_view(["POST"])
def GoatCreate(request):
    if request.method == "POST":
        try:
            print(request)
            user = request.data.get("user")
            print(user)
            user = VillagerDetail.objects.get(username=user)
            goat_gender = request.data.get('goat_gender')
            tag_number = request.data.get('tag_number')
            policy_number = request.data.get('policy_number')
            goat_hand_over_date = request.data.get('goat_hand_over_date')
            
            GoatDetails.objects.create(
                user=user,
                goat_gender=goat_gender,
                tag_number=tag_number,
                policy_number=policy_number,
                goat_hand_over_date=goat_hand_over_date,
                is_alive=True
            )
            return Response(
                {"success": "Task Created"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                data={"Message": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return JsonResponse(
            data={"Message": "Only POST request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )


@api_view(["POST"])
def InsuranceCreate(request,id):
    if request.method == "POST":
        try:
            print(request)
            goat = GoatDetails.objects.get(id=id)
            print(goat)
            # user = VillagerDetail.objects.get(username=user)
            # goat_gender = request.data.get('goat_gender')
            # tag_number = request.data.get('tag_number')
            # policy_number = request.data.get('policy_number')
            # goat_hand_over_date = request.data.get('goat_hand_over_date')
            
            # GoatDetails.objects.create(
            #     user=user,
            #     goat_gender=goat_gender,
            #     tag_number=tag_number,
            #     policy_number=policy_number,
            #     goat_hand_over_date=goat_hand_over_date,
            #     is_alive=True
            # )
            death_place = request.data.get('death_place')
            death_date = request.data.get('death_date')
            death_time = request.data.get('death_time')
            toll_free_no = request.data.get('toll_free_no')
            intimation = request.data.get('intimation')
            panchnama_doc = request.data.get('panchnama_doc')
            police_doc = request.data.get('police_doc')
            sarpanch_doc = request.data.get('sarpanch_doc')
            pm_doc = request.data.get('pm_doc')
            submission_claim_date = request.data.get('submission_claim_date')
            submitted_person = request.data.get('submitted_person')
            claim_number = request.data.get('claim_number')
            claim_settlement_date = request.data.get('claim_settlement_date')
            neft_intimation_date = request.data.get('neft_intimation_date')
            goat_replacement_date = request.data.get('goat_replacement_date')
            replaced_tag_number = request.data.get('replaced_tag_number')
            claim_status = request.data.get('claim_status')
            return Response(
                {"success": "Task Created"},
                status=status.HTTP_201_CREATED,
            )
        except Exception as e:
            print(e)
            return JsonResponse(
                data={"Message": "Internal Server Error"},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR,
            )
    else:
        return JsonResponse(
            data={"Message": "Only POST request allowed"},
            status=status.HTTP_400_BAD_REQUEST,
        )