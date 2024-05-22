"""
URL configuration for sharkRestaurant project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from customer.views import *
from shop.views import *
from django.conf import settings 
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('login/', logins, name='login'),   #登入
    path('register/', register, name='register'), #註冊
    path('logout/', logouts, name='logout'),    #登出

    #店家顧客共用
    path('', homePage, name='home'),    #主頁 
    path('menuAll/', menuAll, name='menuAll'), #菜單全
    path('menuSearch/', menuSearch, name='menuSearch'),#菜單搜索
    path('menuByClassification/<int:classification_id>', menuByClassification, name='menuByClassificationId'), #分類搜索
    path('menu/<int:menu_id>', menuById, name='menu'), #單一菜單
    path('reserveAll/', reserveAll, name='reserveAll'), #訂位記錄查看
    path('comment/', comment, name='comment'),  #留言&留言查看

    #顧客
    path('userModify/', userModify, name='userModify'), #使用者資料修改（本質是密碼修改
    path('userReservation/', userReservation,  name='userReservation'), #訂位

    #店家
    path('menuAdd/', menuAdd, name='menuAdd'),  #菜單添加

    path('menuDelete/<int:menu_id>',menuDelete,name='menuDelete'),  #菜單刪除 多url做刪除後依舊以原篩選模式顯示
    path('menuDelete/<int:menu_id>/<int:classification_id>',menuDelete,name='menuDeleteClassification'),  #
    path('menuDelete/<int:menu_id>/<str:kw>',menuDelete,name='menuDeleteSearch'),  #

    path('menuSaleChange/<int:menu_id>',menuSaleChange, name='menuSaleChange'), #菜單上下架
    path('menuSaleChange/<int:menu_id>/<int:classification_id>',menuSaleChange, name='menuSaleChangeClassification'), #
    path('menuSaleChange/<int:menu_id>/<str:kw>',menuSaleChange, name='menuSaleChangeSearch'), #

    path('reserveIsCome/<int:reserve_id>', reserveIsCome, name='reserveIsCome'), #訂位到場
    path('reserveSearch/', reserveSearch, name='reserveSearch'), #以日期時段查找訂位
    path('timeModify/<int:time_id>',timeModify, name='timeModify'), #時段管理
    path('classificationManage/', classificationManage, name='classificationManage'),  #分類管理
    path('classificationManage/<str:msg>', classificationManage, name='classificationManageMsg'),   #分類管理帶msg
    path('classificationModify/<int:classification_id>', classificationModify, name='classificationModify'),#分類更新
    path('classificationAdd/', classificationAdd, name='classificationAdd'),#分類新增
    path('classificationDelete/<int:classification_id>', classificationDelete, name='classificationDelete'),#分類刪除
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT) #圖片上傳後顯示鏈接
