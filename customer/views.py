from django.shortcuts import *
from .models import Sex, User, Classification, Vegetarian, Menu, Comment, Time, Reserve
from .forms import *
from django.utils import timezone
from datetime import timedelta
from django.db.models import *
from django.contrib.auth import  authenticate,login,logout
from datetime import datetime
from django.contrib import messages
from django.contrib.auth.hashers import check_password

# messages的使用方法，用於未登入時跳轉到登入界面的提示
# {% if messages and not message_displayed %}
#     {% with message_displayed=True %}
#         {% for message in messages %}
#         <p{% if message.tags %} class="{{ message.tags }}"{% endif %} style="color: red;">{{ message }}</p>
#         {% endfor %}
#     {% endwith %}
# {% endif %}

# 表單的ValidationError異常顯示處理
# {{ form.as_p }}
# {% if form.errors %}
#     <ul>
#     {% for field in form %}
#         {% for error in field.errors %}
#             <li>{{ error }}</li>
#         {% endfor %}
#     {% endfor %}
#     </ul>
# {% endif %}

#recommendation都是隨機提供四個做推薦,單菜單下會隨機四個但不包含現在的

def homePage(request):
    if request.user.is_superuser:
        reserveNoon=Reserve.objects.filter(date=datetime.now().date(),time=Time.objects.get(id=1)).order_by('-alternate', 'isCome')
        reserveAfternoon=Reserve.objects.filter(date=datetime.now().date(),time=Time.objects.get(id=2)).order_by('-alternate', 'isCome')
        reserveEvening=Reserve.objects.filter(date=datetime.now().date(),time=Time.objects.get(id=3)).order_by('-alternate', 'isCome')
        reserveNight=Reserve.objects.filter(date=datetime.now().date(),time=Time.objects.get(id=4)).order_by('-alternate', 'isCome')
        timeList=Time.objects.all().order_by('timeStart')
        return render(request, 'manageHome.html', locals())
    menu=Menu.objects.filter(listingDate__lte=timezone.now(),isSale=True).order_by('?')
    menuNew=Menu.objects.filter(listingDate__lte=timezone.now(),isSale=True).order_by('listingDate')
    recommendation=menu[:min(len(menu), 4)]
    new=menuNew[:min(len(menuNew), 4)]
    return render(request, 'home.html', locals())

def logins(request):
    if request.user.is_active:
        return redirect('home')
    if request.method == 'POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            msg = '帳號密碼輸入錯誤'
    return render(request, 'login.html', locals())

def register(request):
    if request.user.is_active:
        return redirect('home')
    sexList=Sex.objects.all()
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')
        password2=request.POST.get('password2')
        email=request.POST.get('email')
        first_name=request.POST.get('first_name')
        sex_id=request.POST.get('sex')
        sex=Sex.objects.get(id=sex_id)
        if password != password2:
            msg='兩次輸入密碼不同'
            return render(request,'register.html',locals())
        elif username == '':
            msg='手機號不得為空'
            return render(request,'register.html',locals())
        elif User.objects.filter(username=username).exists():
            msg='該手機號已註冊'
            return render(request,'register.html',locals())
        elif not bool(re.match('09[0-9]{8}', username)):
            msg='手機號錯誤'
            return render(request, 'register.html', locals())
        elif email=='':
            msg='mail不可為空'
            return render(request,'register.html',locals())
        elif first_name=='':
            msg='姓名不可為空'
            return render(request,'register.html',locals())
        u = User.objects.create_user(username=username, password=password, email=email, first_name=first_name, sex=sex)
        u.save()
        return redirect('/login/')
    return render(request,'register.html',{"sexList": sexList})

def logouts(request):
    logout(request)
    return redirect('/')

def userModify(request):
    if request.user.is_active and not request.user.is_superuser:
        if request.method=='POST':
            password=request.POST.get('password')
            newPassword1=request.POST.get('newPassword1')
            newPassword2=request.POST.get('newPassword2')
            if not check_password(password, request.user.password):
                return render(request, 'userModify.html', {'msg':'原密碼輸入錯誤'})
            if newPassword1 != newPassword2:
                return render(request, 'userModify.html', {'msg':'兩次的新密碼輸入不同'})
            request.user.set_password(newPassword1)
            request.user.save()
            msg='修改成功'
        return render(request, 'userModify.html')
    return redirect('home')

#是管理則回傳提供編輯新增的界面
def menuAll(request):
    classificationAll=Classification.objects.all()
    searchState=request.GET.get('state')
    print(searchState)

    if request.user.is_superuser:
        if searchState == "on":
            menuList=Menu.objects.filter(listingDate__lte=timezone.now(), isSale=True).order_by('isSale','listingDate','price')
        elif searchState == "off":
            menuList=Menu.objects.filter(listingDate__lte=timezone.now(), isSale=False).order_by('isSale','listingDate','price')
        else:
            menuList=Menu.objects.all().order_by('-isSale','listingDate','price')
        return render(request, 'menuManage.html', locals())
    menuList=Menu.objects.filter(listingDate__lte=timezone.now(), isSale=True).order_by('isSale','listingDate','price')
    return render(request, 'menuPage.html', locals())

#是管理則回傳提供編輯新增的界面
def menuSearch(request):
    classificationAll=Classification.objects.all()
    kw=request.GET.get('keyWord')
    menuList=Menu.objects.filter(Q(name__icontains=kw)|
                                Q(introduce__icontains=kw)|
                                Q(classification__name__icontains=kw)).order_by('-isSale','name','listingDate')
    if request.user.is_superuser:
        return render(request,'menuManage.html',locals())
    menuList=menuList.filter(listingDate__lte=timezone.now(),isSale=True)
    return render(request,'menuPage.html',locals())

#是管理則回傳提供編輯的界面
def menuById(request, menu_id):
    if Menu.objects.filter(id=menu_id).exists():
        menu=Menu.objects.get(id=menu_id)
        if request.user.is_superuser:
            form=MenuForm(instance=menu)
            if request.method=='POST':
                form=MenuForm(request.POST, request.FILES, instance=menu)
                if form.is_valid():
                    form.save()
                    msg="修改完成"
            return render(request, 'menuModify.html', locals())
        recommendation=Menu.objects.filter(listingDate__lte=timezone.now(),isSale=True).exclude(id=menu_id).order_by('?')
        recommendation=recommendation[:min(len(recommendation), 4)]
        return render(request,'menu.html',locals())
    return redirect('/')

def menuByClassification(request, classification_id):
    classificationAll=Classification.objects.all()
    if Classification.objects.filter(id=classification_id).exists():
        classification=Classification.objects.get(id=classification_id)
        if request.user.is_superuser:
            menuList=Menu.objects.filter(classification=classification).order_by('-isSale','listingDate','price')
            return render(request, 'menuManage.html', locals())
        menuList=Menu.objects.filter(classification=classification, listingDate__lte=timezone.now(), isSale=True).order_by('isSale','listingDate','price')
        return render(request,'menuPage.html',locals())
    return redirect('/')

def comment(request):
    comments = Comment.objects.all()  # 查詢所有資料
    if request.user.is_superuser:
        comments=Comment.objects.all().order_by('uploadTime')
        return render(request, 'readComment.html', locals())
    if request.method == "POST":
        if request.user.is_active:
            name=request.POST.get('name')
            if name=='':
                name=request.user.first_name
            comment=request.POST.get('comment')
            if comment == '':
                msg='不能上傳空的留言哦'
                return render(request, 'toComment.html', locals())
            Comment.objects.create(name=name, commenter=request.user, comment=comment)
            mag='感謝您的留言回饋，祝您生活愉快'
            return render(request, 'toComment.html', locals())
        msg='尚未登入不可留言，請先登入'
        return render(request, 'error.html', locals())
    return render(request, 'toComment.html', locals())
    
def userReservation(request):
    if request.user.is_active:
        if request.user.is_superuser:
            redirect('home')
        if request.method=='POST':
            d=request.POST.get('date')
            date=datetime.strptime(d, '%Y年%m月%d日')
            time_id=request.POST.get('time')
            time=Time.objects.get(id=time_id)
            numberOfPeople=int(request.POST.get('numberOfPeople'))
            note=request.POST.get('note')
            alternate=False
            if Reserve.objects.filter(customer=request.user, date=date, time=time).exists():
                msg='您已經預約本時段'
                return render(request, 'userReservation.html', locals())
            total_people_count=Reserve.objects.filter(date=date, time=time).aggregate(Sum('numberOfPeople'))['numberOfPeople__sum']    #aggregate進行合計 平均等操作
            if total_people_count is None: 
                    total_people_count=0
            allWait=total_people_count + numberOfPeople
            if allWait > time.numberOfPeopleMax:
                    alternate=True
            Reserve.objects.create(customer=request.user, numberOfPeople=numberOfPeople,
                                   date=date, time=time, note=note, alternate=alternate)
            return render(request, 'reservationSuccess.html', locals())
        dateList = []
        for i in range(1, 8):
            future_date = datetime.today().date() + timedelta(days=i)
            dateList.append(future_date)
        timeList = Time.objects.all().order_by('timeStart')
        return render(request, 'userReservation.html', locals())
    msg='尚未登入不可訂位，請先登入'
    return render(request, 'error.html', locals())

def reserveAll(request):
    if request.user.is_active:
        if request.user.is_superuser:
            form=ReserveSearchForm()
            reserve=Reserve.objects.filter(date__range=[datetime.now().date(), datetime.now().date() + timedelta(days=6)]).order_by('date')
            return render(request, 'reserveManage.html', locals())
        reserve=Reserve.objects.filter(customer=request.user).order_by('date')
        return render(request, 'reserve.html', locals())
    msg='尚未登入不可查看訂位，請先登入'
    return render(request, 'error.html', locals())