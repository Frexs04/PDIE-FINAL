from django.contrib import admin
from .models import Manager,RESIDENT,STAFF,Visitor,EVENT,REPORT,Duties

# Register your models here.
admin.site.register(Manager),
admin.site.register(RESIDENT),
admin.site.register(STAFF),
admin.site.register(Visitor),
admin.site.register(EVENT),
admin.site.register(REPORT),
admin.site.register(Duties),