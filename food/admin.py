from django.contrib import admin
from . models import *
# Register your models here.

class MenuAdmin(admin.ModelAdmin):
    list_display = ('id', 'title', 'img', 'price', 'max_quantity', 'min_quantity', 'display', 'created', 'update', 'description', 'breakfast', 'lunch', 'dinner', 'dessert')
admin.site.register(Menu,MenuAdmin)

class ContactAdmin(admin.ModelAdmin):
    list_display = ('id','full_name','email','message','admin_note','status','message_date','admin_update')
admin.site.register(Contact,ContactAdmin)

class ProfileAdmin(admin.ModelAdmin):
    list_display = ['id','user', 'first_name','last_name','email','phone','address','state','pix']
admin.site.register(Profile,ProfileAdmin)

class ShopcartAdmin(admin.ModelAdmin):
    list_display = ['user', 'menu','quantity', 'price', 'amount', 'order_no', 'paid', 'created_at']
admin.site.register(Shopcart,ShopcartAdmin)
