from django.contrib import admin
from .models import *

# Register your models here.
class UserAdmin(admin.ModelAdmin):
    list_display=['username','first_name','last_name','email','sex']

class MenuAdmin(admin.ModelAdmin):
    list_display=['name','price','listingDate','image','isSale','classification']

class CommentAdmin(admin.ModelAdmin):
    list_display=['commenter','comment']

class TimeAdmin(admin.ModelAdmin):
    list_display=['name','timeStart','timeEnd']

class ReserveAdmin(admin.ModelAdmin):
    list_display=['customer','date','time','alternate','isCome']

class Admin(admin.ModelAdmin):
    list_display=['name']


admin.site.register(Sex, Admin)
admin.site.register(User, UserAdmin)
admin.site.register(Classification, Admin)
admin.site.register(Vegetarian, Admin)
admin.site.register(Menu, MenuAdmin)
admin.site.register(Comment, CommentAdmin)
admin.site.register(Time, TimeAdmin)
admin.site.register(Reserve, ReserveAdmin)