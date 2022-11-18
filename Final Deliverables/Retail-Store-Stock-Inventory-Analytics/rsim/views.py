from django.shortcuts import render,redirect,HttpResponse
from django.db import connection
from barcode import Code39
from datetime import date
from django.http import JsonResponse,FileResponse
from django.views.decorators.csrf import csrf_exempt
from django.core.paginator import Paginator,EmptyPage, PageNotAnInteger
from barcode.writer import ImageWriter
from .models import Dataset,extendedProfileInfo,RegularSales
from django.http import FileResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login,logout
from django.contrib.auth.models import User,auth
from . import prediction
import io,requests,os

cache = {
    "item_cnt":"1",
}

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
            val.append({"id":integer,"name":value.name,"qty":value.stock,"sp":value.sp,"expdate":value.expirydate,"pid":value.product_id})
            integer = integer + 1
    else:
        values = Dataset.objects.filter(mart_name = request.user.username)
        integer = 1
        for value in values:
            val.append({"id":integer,"name":value.name,"qty":value.stock,"sp":value.sp,"expdate":value.expirydate,"pid":value.product_id})
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
            return redirect("/")
        else:
            return render(request,"Login.html",{'status':'Bad Cred if you are the new user Register First'})
    else:
        return render(request,"Login.html")

def displayreport(request):
    if request.method == "POST":
        manager_name = extendedProfileInfo.objects.get(email = request.user.email).manager_name
        prediction.createPDF(manager_name,request.user.username)
        return FileResponse(open('text-on-image.pdf', 'rb'), content_type='application/pdf')
    else:
        prediction.visualize(request.user.username)
        return render(request,"report-view.html")

def update(request):
    prod_id = request.GET.get('prodid')
    if request.method == "POST":
        cp = request.POST['cp']
        sp = request.POST['sp']
        stock = int(request.POST['stock'])
        exp = request.POST['expiryDate']
        post = Dataset.objects.get(product_id=prod_id)
        post.sales = int(post.sales) + stock
        post.cp = cp
        post.sp = sp
        post.expiryDate = exp
        post.save()
    else:
        accuracy,mon_values,pred_values = prediction.Predict(prod_id,request.user.username)
        v = Dataset.objects.filter(product_id = prod_id,mart_name = request.user.username).values()[0]
        return render(request,"update_records.html",{'cp':v['cp'],'sp':v['sp'],'stock':v['stock'],'acc':accuracy,"months":mon_values,"pred":pred_values})
@login_required(login_url='login')
@csrf_exempt
def billing(request):
    res = list(Dataset.objects.filter(mart_name = request.user.username).values_list('name',flat=True))
    if request.method == 'POST':
        val = request.POST['search_val']
        res = Dataset.objects.filter(mart_name = request.user.username,name = val).values()
        resp = []
        for i in res:
            resp.append({'id':cache["item_cnt"],'name':i["name"],'price':i["sp"]}) 
        cache["item_cnt"] =  int(cache["item_cnt"]) + 1
        return JsonResponse({'name':resp})
    else:
        cache["item_cnt"],cache['total'] = "1",0
        return render(request,"testbilling.html",{'name':res})

def sendEmail(product,email,count):
    url = 'https://api.emailjs.com/api/v1.0/email/send'
    header = {
        'contentType': 'application/json'
    }
    myobj = {
        'service_id': 'service_r43q87l',
        'template_id': 'template_0dqkujg',
        'user_id': 'lYYw2FI0jGkE59hnh',
        'template_params':{
            'product':product,
            'count':count,
            'mart_owner': email,
            'to_name': extendedProfileInfo.objects.get(email = email).manager_name
        }
    }
    x = requests.post(url,headers=header, json = myobj)
    return(x.text)

def modDB(request):
    for i in request.GET:
        res = Dataset.objects.get(mart_name = request.user.username,name = i)
        sendEmail(i,request.user.email,request.GET.get(i))
        RegularSales.objects.create(mart_name = request.user.username,prod_name = i,sales = request.GET.get(i),date = str(date.today()))
        res.stock = int(res.stock) - int(request.GET.get(i)) 
        res.save()
    return redirect("billing")

def index(request):
    if request.user.is_authenticated:
        return render(request,"index.html",{'auth':"True"})
    else:
        return render(request,"index.html",{'auth':"False"})
@login_required(login_url='login')
def log_out(request):
    logout(request)
    return redirect("/")