from django.shortcuts import render,redirect
from django.contrib import messages
from math import ceil
import threading
from .models import *
from .forms import *
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.models import User
from django.views.generic import View
from math import ceil
import threading
import razorpay
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import random


# TO ACTIVATE USER ACCOUNTS
from django.contrib.sites.shortcuts import get_current_site
from django.utils.http import urlsafe_base64_encode,urlsafe_base64_decode
from django.urls import NoReverseMatch,reverse
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes,DjangoUnicodeDecodeError,force_str
# TO ACTIVATE USER ACCOUNTS

# GETTING TOKENS
from .utils import TokenGenerator
# GETTING TOKENS

# SENDING MAILS
from django.core.mail import send_mail,EmailMultiAlternatives,BadHeaderError,EmailMessage
from django.core import mail
from django.conf import settings
# SENDING MAILS


class EmailThread(threading.Thread):
    def __init__(self,email_message):
        self.email_message=email_message
        threading.Thread.__init__(self)
    def run(self):
        self.email_message.send()

razorpay_client=razorpay.Client(
    auth=(settings.RAZOR_KEY_ID,settings.RAZOR_KEY_SECRET)
    )

class activate(View):
    def get(self,request,uidb64,token):
        try:
            uid=force_str(urlsafe_base64_decode(uidb64))
            user=User.objects.get(pk=uid)
        except Exception as identifier:
            user=None
        if(user is not None and TokenGenerator().check_token(user,token)):
            user.is_active=True
            user.save()
            messages.info(request,'Account Is Created Successfully')
            return redirect('LOGIN')
        return render(request,'activatefail.html')
# Create your views here.
def index(request):
    allprods=[]
    catproducts=food.objects.values('cate','id')
    cats={item['cate'] for item in catproducts}
    for cat in cats:
        prod=food.objects.filter(cate=cat)
        n=len(prod)
        nslides=n//4+ceil((n/4)-(n//4))
        allprods.append([prod,range(1,nslides),nslides])
    rev=review.objects.all()
    splfoods=food.objects.filter(special=True)
    return render(request,'index.html',{'foo':allprods,'review':rev,'spl':splfoods})

def logi(request):
    if(request.method=='POST'):
        global ordid
        ordid=str(random.randint(10000,99000))
        username=request.POST['username']
        password=request.POST['password']
        user=authenticate(request,username=username,password=password)
        if(user is not None):
            login(request,user)
            cus,boo=customer.objects.get_or_create(user=request.user)
            if(cartitem.objects.filter(order=cus).exists):
                cartitem.objects.filter(order=cus).delete()
            fin,boo=finalord.objects.get_or_create(customer=cus)
            fin.bill=0
            fin.payment=" "
            fin.paymentid=" "
            fin.paydone=False
            fin.complete=False
            fin.save()
            return redirect('INDEX')
        else:
            messages.info(request,'INVALID CREDENTIALS')
    return render(request,'login.html')

def logo(request):
    logout(request)
    return redirect('INDEX')

def register(request):
    form=userform()
    if(request.method=='POST'):
        form=userform(request.POST)
        if(form.is_valid()):
            form.save()
            loginer=User.objects.get(username=form.cleaned_data['username'])
            current_site=get_current_site(request)
            email_subject="Activate Your Account"
            message=render_to_string('activate.html',{
                'user':loginer,
                'domain':'http://127.0.0.1:8000',
                'uid':urlsafe_base64_encode(force_bytes(loginer.pk)),
                'token':TokenGenerator().make_token(loginer)
            })
            email_message=EmailMessage(email_subject,message,settings.EMAIL_HOST_USER,
                                       ['tejusajayan8@gmail.com'])
            EmailThread(email_message).start()
            messages.success(request,'ACTIVATE YOUR ACCOUNT BY CLICKING LINK ON YOUR MAIL')
            return redirect('LOGIN')
    return render(request,'register.html',{'form':form})

def addcart(request):
    if(request.user.is_authenticated):
        id=request.POST['item_id']
        foo=food.objects.get(id=id)
        cus,boo=customer.objects.get_or_create(user=request.user,name=request.user.username)
        cartitem(order=cus,product=foo,orderid=ordid).save()
        totalcalc(request,foo.foodprice,'add')
        return JsonResponse({'success':True})
    else:
        return redirect('LOGIN')


def cart(request):
    form=shippdet()
    if(request.user.is_authenticated):
        cus,boo=customer.objects.get_or_create(user=request.user)
        cart=cartitem.objects.filter(order=cus)
    else:
        cart=[]
    return render(request,'cart.html',{'cart':cart,'form':form})

def totalcalc(request,price,op):
    finalcus,boo=finalord.objects.get_or_create(customer=customer.objects.get(user=request.user))
    if(op=='add'):
        finalcus.bill+=price*1
    elif(op=='sub'):
        finalcus.bill-=price*1
        print(finalcus.bill)
    finalcus.save()

def deletecart(request):
    id=request.POST['item_id']
    try:
        obj=cartitem.objects.get(id=id)
        totalcalc(request,obj.product.foodprice,'sub')
        cartitem(id=id).delete()
        return JsonResponse({'success':True})
    except cartitem.DoesNotExist:
        return JsonResponse({'success':False,'error':'Cart item does not exist'})

def incquant(request):
    id=request.POST['item_id']
    try:
        obj=cartitem.objects.get(id=id)
        obj.quantity+=1
        totalcalc(request,obj.product.foodprice,'add')
        obj.save()
        return JsonResponse({'success':True})
    except cartitem.DoesNotExist:
        return JsonResponse({'success':False,'error':'Cart item does not exist'}) 
    
def deccquant(request):
    id=request.POST['item_id']
    try:
        obj=cartitem.objects.get(id=id)
        obj.quantity-=1
        totalcalc(request,obj.product.foodprice,'sub')
        obj.save()
        return JsonResponse({'success':True})
    except cartitem.DoesNotExist:
        return JsonResponse({'success':False,'error':'Cart item does not exist'})

def getreview(request):
    if(request.method=='POST'):
        name=request.POST['reviewer']
        content=request.POST['revcon']
        review(name=name,content=content).save()
        return redirect('INDEX')

def dine(request):
    if(request.method=='POST'):
        name=request.POST['field1']
        num=request.POST['field2']
        dt=request.POST['field3']
        seat=request.POST['field4']
        dinereq(name=name,number=num,datetime=dt,seat=seat).save()
        return redirect('INDEX')
    

def payment(request):
    if(request.user.is_authenticated):
        form=shippdet()
        if(request.method=='POST'):
            val=request.POST['by']
            form=shippdet(request.POST)
            if(form.is_valid()):
                cus,boo=customer.objects.get_or_create(user=request.user)
                finalcus,boo=finalord.objects.get_or_create(customer=cus)
                finalcus.name=form.cleaned_data['name']
                finalcus.number=form.cleaned_data['number']
                finalcus.doorno=form.cleaned_data['doorno_street_area']
                finalcus.landmark=form.cleaned_data['landmark']
                finalcus.pincode=form.cleaned_data['pincode']
                finalcus.transaction_id=ordid
                finalcus.save()
                if(val=='OP'):
                    finalcus.payment='ONLINE PAYMENT'
                    amount=finalcus.bill
                    client=razorpay.Client(auth=('rzp_test_pX8GliFg8F8TDt','imIPZ0GJZCd9XM6kJhfXyCIS'))
                    razorpay_order=client.order.create(
                        {'amount':amount*100,'currency':'INR','payment_capture':'1'}
                    )
                    porder=order.objects.create(
                        name=request.user.username,amount=amount,provider_order_id=razorpay_order["id"]
                    )
                    finalcus.paymentid=razorpay_order["id"]
                    finalcus.save()
                    porder.save()
                    callback_url = "http://" + "127.0.0.1:8000" + "/paysf/"
            
                    context = {}
                    context['razorpay_order_id'] = razorpay_order['id']
                    context['razorpay_merchant_key'] = settings.RAZOR_KEY_ID
                    context['currency'] = 'INR'
                    context['callback_url'] = callback_url
                    context['order']=porder
                    context['email']=User.objects.get(username=request.user.username).email
                    context['name']=customer.objects.get(user=request.user).name
                    return render(request,'payhandler.html',context)
                elif(val=='COD'):
                    finalcus.payment="Cash On Delivery"
                    finalcus.save()
                    return render(request,'paysuccess.html')
        return render(request,'cart.html',{'form':form})
    else:
        return redirect('CART')

@csrf_exempt
def paysf(request):
    def verify_signature(response_data):
        client=razorpay.Client(auth=('rzp_test_pX8GliFg8F8TDt','imIPZ0GJZCd9XM6kJhfXyCIS'))
        return client.utility.verify_payment_signature(response_data)
    
    if('razorpay_signature' in request.POST):
        pid=request.POST['razorpay_payment_id']
        poid=request.POST['razorpay_order_id']
        signid=request.POST['razorpay_signature']
        ord=order.objects.get(provider_order_id=poid)
        ord.payment_id=pid
        ord.signature_id=signid
        ord.save()
        if verify_signature(request.POST):
            ord.status='PAYMENT SUCCESS'
            ord.save()
            return render(request,'paysuccess.html')
        else:
            ord.status='PAYMENT FAILURE'
            ord.save()
            return render(request,'payfail.html')
    else:
        payment_id = json.loads(request.POST.get("error[metadata]")).get("payment_id")
        provider_order_id = json.loads(request.POST.get("error[metadata]")).get(
            "order_id"
        )
        ord = order.objects.get(provider_order_id=provider_order_id)
        ord.payment_id = payment_id
        ord.status = 'PAYMENT FAILURE'
        ord.save()
        return render(request, "payfail.html")
