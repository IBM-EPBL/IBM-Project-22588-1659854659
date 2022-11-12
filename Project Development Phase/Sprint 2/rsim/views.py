from django.shortcuts import render,redirect,HttpResponse
from django.db import connection
from barcode import Code39
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from barcode.writer import ImageWriter
from .models import Dataset,extendedProfileInfo
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User,auth
import io

def generate_barcode(string,pname):
    my_code = Code39(string, writer=ImageWriter(),add_checksum = False)
    my_code.save(pname)
    f = open(pname+".png","rb")
    return f.read()

def register(request):
    if request.method == "POST":
        name = request.POST['full-name']
        sname = request.POST['store-name']
        location  = request.POST['location']
        email = request.POST['your-email']
        password = request.POST['password']
        repassword = request.POST['comfirm-password']
        if password == repassword:
            user = User.objects.create_user(username = sname,password = password,first_name = sname,email = email)
            user.save()
            userinfo = extendedProfileInfo.objects.create(email = email,location = location,manager_name = name)
            userinfo.save()
            return redirect("/")
    else:
        return render(request,"registration.html")

@login_required(login_url='login')
def productInfo(request):
    if request.method == "POST":
        name = request.POST['name']
        expirydate = request.POST['edate']
        stock = request.POST['qty']
        cp = request.POST['cp']
        sp = request.POST['sp']
        cursor = connection.cursor()
        cursor.execute('''SELECT DISTINCT product_id,1 id FROM dataset''')
        row = cursor.fetchall()
        prodID = "PRD"+str(len(row) + 1)  
        f = generate_barcode(prodID,name)
        buffer = io.BytesIO(f)
        buffer.seek(0)
        Dataset.objects.create(mart_name = request.user.username,name=name,product_id=prodID,expirydate=expirydate,cp=cp,sp=sp,stock = stock).save()
        response = FileResponse(buffer, as_attachment=True, filename=name+'.png')
        return response
    else:
        return render(request,"PI.html")
@login_required(login_url='login')
def existingPro(request):
    dta = request.GET.get('keywords')
    val = []
    page = request.GET.get('page', 1)
    if dta != None:
        values = Dataset.objects.filter(name__iregex=dta,mart_name = request.user.username)
        integer = 1
        for value in values:
            val.append({"id":integer,"name":value.name,"qty":value.stock,"sp":value.sp,"expdate":value.expirydate})
            integer = integer + 1
    else:
        values = Dataset.objects.filter(mart_name = request.user.username)
        integer = 1
        for value in values:
            val.append({"id":integer,"name":value.name,"qty":value.stock,"sp":value.sp,"expdate":value.expirydate})
            integer = integer + 1
    paginator = Paginator(val, 5)
    try:
        users = paginator.page(page)
    except PageNotAnInteger:
        users = paginator.page(1)
    except EmptyPage:
        users = paginator.page(paginator.num_pages)
    return render(request,"EP.html",{'val':users})

def Login(request):
    if request.method == "POST":
        email = request.POST['email']
        password = request.POST['password']
        user = authenticate(request, username = email, password = password)
        if user is not None:
            form = login(request,user)
            return render(request,'PI.html')
        else:
            return render(request,"Login.html",{'status':'Bad Cred if you are the new user Register First'})
    else:
        return render(request,"Login.html")

def displayreport(request):
    return render(request,"report-view.html")