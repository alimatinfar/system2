from django.conf.urls import url
from . import views

app_name = 'app1'
urlpatterns = [
    url(r'^create_profile/$', views.CreateProfile.as_view(), name = 'create_profile'),
    url(r'^request_emtood/$', views.RequestEMtoODAPIView.as_view(), name = 'request_emtood'),
    url(r'^request_emtooe/$', views.RequestEMtoOEAPIView.as_view(), name='request_emtooe'),
    url(r'^request_oetood/$', views.RequestOEtoODAPIView.as_view(), name='request_oetood'),
    url(r'^inbox/$', views.InboxAPIView.as_view(), name='inbox'),
    url(r'^deter_emtood/(?P<id>\d+)$', views.DeterminationEMtoODAPIView.as_view(), name='deter_emtood'),
    url(r'^deter_emtooe/(?P<id>\d+)$', views.DeterminationEMtoOEAPIView.as_view(), name='deter_emtooe'),
    url(r'^deter_oetood/(?P<id>\d+)$', views.DeterminationOEtoODAPIView.as_view(), name='deter_oetood'),
    url(r'^login/$', views.Login.as_view(), name='login'),
    url(r'^manage/$', views.ManageAPIView.as_view(), name='manage'),

    # url(r'^(?P<id>\d+)/manage$', views.PostDeleteUpdateAPIView.as_view(), name='post-update'),
    # url(r'^create/$', views.PostCreateAPIView.as_view(), name='post-update'),
    # url(r'^login/$', views.Login222.as_view(), name='post-update'),
]