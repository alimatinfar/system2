from django.conf.urls import url
from . import views

app_name = 'app1'
urlpatterns = [
    url(r'^create_profile/$', views.CreateProfile.as_view(), name='create_profile'),
    # ساخت پروفایل

    url(r'^request_emod/$', views.RequestEMtoODAPIView.as_view(), name='request_emod'),
    # ارسال درخواست ارتقا کامند به مدیر سازمان

    url(r'^request_emoe/$', views.RequestEMtoOEAPIView.as_view(), name='request_emoe'),
    # ارسال درخواست ارتقا کارمند به کارمند سازمان

    url(r'^request_oeod/$', views.RequestOEtoODAPIView.as_view(), name='request_oeod'),
    # ارسال درخواست ارتقا کارمند سازمان به مدیر سازمان
    url(r'^inbox/$', views.InboxAPIView.as_view(), name='inbox'),
    # صندوق جهت مشاهده درخواست های ارتقا برای ادمین و مدیر سازمان

    url(r'^deter_emod/(?P<id>\d+)/$', views.DeterminationEMtoODAPIView.as_view(), name='deter_emod'),
    #تعیین وضعیت درخواست های ارتقا کارمند به مدیر سازمان توسط ادمین determine

    url(r'^deter_emoe/(?P<id>\d+)/$', views.DeterminationEMtoOEAPIView.as_view(), name='deter_emoe'),
    # تعیین وضعیت درخواست های ارتقا کارمند به کارمند سازمان توسط ادمین و مدیر سازمان determine

    url(r'^deter_oeod/(?P<id>\d+)/$', views.DeterminationOEtoODAPIView.as_view(), name='deter_oeod'),
    # تعیین وضعیت درخواست های ارتقا کارمند سازمان به مدیر سازمان توسط ادمین و مدیر سازمان determine

    url(r'^login/$', views.Login.as_view(), name='login'),
    #ورود کاربر

    url(r'^manage/$', views.ManageAPIView.as_view(), name='manage'),
    #مدیریت پروفایل کابران جهت تغییر نقش و سازمان افراد توسط ادمین

    url(r'^create_duty/$', views.DutyCreateAPIView.as_view(), name='create_duty'),
    #وظیفه

    url(r'^edit_duty/(?P<id>\d+)/$', views.DutyEditAPIView.as_view(), name='edit_duty'),
    # وظیفه

    # url(r'^(?P<id>\d+)/manage$', views.PostDeleteUpdateAPIView.as_view(), name='post-update'),
    # url(r'^create/$', views.PostCreateAPIView.as_view(), name='post-update'),
    # url(r'^login/$', views.Login222.as_view(), name='post-update'),
]
