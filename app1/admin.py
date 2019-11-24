from django.contrib import admin
from .models import *
# Register your models here.
admin.site.register(Profile)
admin.site.register(RequestEMtoOD)
admin.site.register(Organization)
admin.site.register(Duty)
admin.site.register(RequestEMtoOE)
admin.site.register(RequestOEtoOD)