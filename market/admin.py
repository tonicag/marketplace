from django.contrib import admin
from .models import Order,Platform,PlatformType,Post,Type
# Register your models here.


admin.site.register(Order)
admin.site.register(Platform)
admin.site.register(PlatformType)
admin.site.register(Post)
admin.site.register(Type)