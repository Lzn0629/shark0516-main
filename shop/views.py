from django.shortcuts import *
from django.utils import timezone
from datetime import datetime
from django.contrib.auth.decorators import login_required
from customer.models import Sex, User, Classification, Vegetarian, Menu, Comment, Time, Reserve
from datetime import timedelta
from customer.forms import *
from django.urls import reverse

@login_required
def menuAdd(request):
    if not request.user.is_superuser:
        return redirect('home')
    form=MenuForm()
    if request.method=='POST':
        form=MenuForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            form=MenuForm()
            msg="新增成功"
    return render(request,'menuAdd.html', locals())

@login_required
def menuDelete(request, menu_id, classification_id=None, kw=None):
    if not request.user.is_superuser and Menu.objects.filter(id=menu_id).exists():
        return redirect('home')
    menu=Menu.objects.get(id=menu_id)
    menu.delete()
    if classification_id:
        return redirect('menuByClassificationId', classification_id=classification_id)  #是<int:classification_id>
    if kw:
        return redirect(reverse('menuSearch') + '?keyWord=' + kw)    #menuSearch的URL是menuSearch/ 沒有接收<>的參數，是接收form的值做搜尋(使用?參數=)
    return redirect('menuAll')

@login_required
def menuSaleChange(request, menu_id, classification_id=None, kw=None):
    if not request.user.is_superuser and Menu.objects.filter(id=menu_id).exists():
        return redirect('home')
    menu=Menu.objects.get(id=menu_id)
    menu.isSale = not (menu.isSale)
    menu.save()
    if classification_id:
        return redirect('menuByClassificationId', classification_id=classification_id)
    if kw:
         return redirect(reverse('menuSearch') + '?keyWord=' + kw)
    return redirect('menuAll')

@login_required
def reserveIsCome(request, reserve_id):
    if request.user.is_superuser and Reserve.objects.filter(id=reserve_id).exists():
        reserve=Reserve.objects.get(id=reserve_id)
        reserve.isCome=True
        reserve.save()
    return redirect('home')

# @login_required
# def reserveDelete(request, reserve_id):
#     if request.user.is_superuser and Reserve.objects.filter(id=reserve_id).exists():
#         reserve=Reserve.objects.get(id=reserve_id)
#         reserve.delete()
#         return redirect('reserveAll')
#     return redirect('home')

@login_required
def reserveSearch(request):
    if request.user.is_superuser:
        reserve = None  #讓未選取的是None
        if request.method == 'POST':
            form = ReserveSearchForm(request.POST)
            if form.is_valid():
                time = form.cleaned_data.get('time')
                date = form.cleaned_data.get('date')
                if time and date:
                    reserve = Reserve.objects.filter(date__range=[datetime.now().date(), datetime.now().date() + timedelta(days=6)], time=time, date=date)
                elif time:
                    reserve = Reserve.objects.filter(date__range=[datetime.now().date(), datetime.now().date() + timedelta(days=6)], time=time)
                elif date:
                    reserve = Reserve.objects.filter(date__range=[datetime.now().date(), datetime.now().date() + timedelta(days=6)], date=date)
                else:
                    reserve = Reserve.objects.filter(date__range=[datetime.now().date(), datetime.now().date() + timedelta(days=6)])
            return render(request, 'reserveManage.html', locals())
        form = ReserveSearchForm()
        return render(request, 'reserveManage.html', locals())
    return redirect('home')

@login_required
def timeModify(request, time_id):
    if request.user.is_superuser and Time.objects.filter(id=time_id).exists():
        time=Time.objects.get(id=time_id)
        form=TimeForm(instance=time)
        if request.method=='POST':
            form=TimeForm(request.POST, instance=time)
            if form.is_valid():
                form.save()
                msg='更改成功'
        return render(request, 'timeModify.html', locals())
    return redirect('home')

@login_required
def classificationManage(request, msg=None):
    if request.user.is_superuser:
        classifications=Classification.objects.all()
        return render(request, 'classificationManage.html', locals())
    return redirect('home')

@login_required
def classificationModify(request, classification_id):
    if request.user.is_superuser and Classification.objects.filter(id=classification_id).exists():
        classification=Classification.objects.get(id=classification_id)
        form=ClassificationForm(instance=classification)
        if request.method=='POST':
            form=ClassificationForm(request.POST, instance=classification)
            if form.is_valid():
                form.save()
        return redirect('classificationManage')
    return redirect('home')

@login_required
def classificationAdd(request):
    if request.user.is_superuser:
        form=ClassificationForm()
        if request.method=='POST':
            form=ClassificationForm(request.POST)
            if form.is_valid():
                form.save()
                return redirect('classificationManage')
        return render(request, 'classificationAdd.html', locals())
    return redirect('home')

@login_required
def classificationDelete(request, classification_id):
    if request.user.is_superuser and Classification.objects.filter(id=classification_id).exists():
        classification=Classification.objects.get(id=classification_id)
        if Menu.objects.filter(classification=classification).exists():
            msg='當前分類仍有項目無法刪除'
        else:
            classification.delete()
            msg='刪除成功'
        return redirect('classificationManageMsg', msg=msg)
    return redirect('home')
