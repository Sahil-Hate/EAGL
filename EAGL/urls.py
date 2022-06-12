from django.urls import path
from . import views

urlpatterns = [
    path("",views.index,name='index'),
    path("login",views.login,name='login'),
    path("logout",views.logout,name='logout'),
    path("userlist",views.userlist,name='userlist'),
    path("userdetail/<int:id>/",views.userdetail,name='userdetail'),
    path("update_user/<int:id>/",views.update_user,name='update_user'),
    path("delete_user/<int:id>/",views.delete_user,name='delete_user'),
    path("insuranceClaim/<str:user>/<int:id>/",views.insuranceClaim,name='insuranceClaim'),
    path("update_insurance/<str:user>/<int:id>/",views.update_insurance,name='update_insurance'),
    path("vaccination/<str:user>/<int:id>/",views.vaccination,name='vaccination'),
    path("update_vaccination/<str:user>/<int:id>/",views.update_vaccination,name='update_vaccination'),
    # API
    path("api_createvillager/",views.VillagerDetailCreate.as_view(),name='VillagerDetailCreate'),
    path("api_villagerlist/",views.VillagerList,name='VillagerList'),
    path("api_creategoat/",views.GoatCreate,name='GoatCreate'),
    path("api_insurancecreate/<int:id>/",views.InsuranceCreate,name='InsuranceCreate'),
]