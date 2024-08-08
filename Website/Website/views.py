from django.http import HttpResponse
from django.shortcuts import render, redirect
from .models import *
from django.db import connection
from django.template.defaulttags import register
from django.shortcuts import get_list_or_404

def main(request):
    cursor_t=connection.cursor()
    cursor_t.execute("select pname,photo1,Sdescription from product where category='television' limit 1")
    rec_t=cursor_t.fetchone()
    
    cursor_l=connection.cursor()
    cursor_l.execute("select pname,photo1,Sdescription from product where category='laptop' limit 1")
    rec_l=cursor_l.fetchone()

    cursor_m=connection.cursor()
    cursor_m.execute("select pname,photo1,Sdescription from product where category='mobile' limit 1")
    rec_m=cursor_m.fetchone()

    cursor_f=connection.cursor()
    cursor_f.execute("select cname,feedback from feed limit 3")
    rec_f=cursor_f.fetchall()

    return render(request,"main.html",{"rec_t":rec_t,"rec_l":rec_l,"rec_m":rec_m,"rec_f":rec_f})


def customer_register(request):
    msg={}

    if request.POST.get("cname") and int(request.POST.get("contact")) and request.POST.get("pass1") and request.POST.get("pass2") and request.POST.get("email"):
        check=request.POST.get("pass1")
        check2=request.POST.get("pass2")
        email_1=request.POST.get("email")
        
        if customer.objects.filter(email=email_1).exists():
            msg={"msg":"Email already registered"}
        else:
            if check==check2:
                cust=customer(cname=request.POST.get("cname"),contact=int(request.POST.get("contact")),pass1=request.POST.get("pass1"),email=request.POST.get("email"))
                cust.save()
                msg={"msg":"Registered Successfully"}
            else:
                msg={"msg":"Password does not match!"}
    
    return render(request,"customer_register.html",msg)


def customerlogin(request):
    msg = {}
    
    if request.POST.get("pass11") and request.POST.get("email1"):
        pass11 = request.POST.get("pass11")
        email1 = request.POST.get("email1")
        
        customers = customer.objects.all()
        login_successful = False
        
        for customer_instance in customers:
            pass1=customer_instance.pass1
            email=customer_instance.email
            if pass1 == pass11 and email == email1:
                login_successful = True
                
                request.session['email1']=email1
                break
        
        if login_successful:
            return redirect("/home")
        else:
            msg = {"msg": "Login details do not match!!"}
    
    return render(request, "customerlogin.html",msg)  


def adminlogin(request):
    msg={"msg":""}
    if request.POST.get("username") and request.POST.get("pass11"):

        if request.POST.get("username")=="admin" and request.POST.get("pass11")=="123":
            return redirect("/adminpage")
        else:
            msg={"msg":"Invalid Login Details"}
    return render(request,"adminlogin.html",msg)



def home(request):
    return render(request,"home.html")

def aboutus(request):
    return render(request,"Aboutus.html")


def laptop(request):
    cursor=connection.cursor()
    cursor.execute("select pid,pname,price,photo1,Sdescription from product where category='laptop'")
    rec=cursor.fetchall()
    return render(request,"Laptops.html",{"rec":rec})


def mobile(request):
    cursor=connection.cursor()
    cursor.execute("select pid,pname,price,photo1,Sdescription from product where category='mobile'")
    rec=cursor.fetchall()
    return render(request,"Mobiles.html",{"rec":rec})


def television(request):
    cursor=connection.cursor()
    cursor.execute("select pid,pname,price,photo1,Sdescription from product where category='television'")
    rec=cursor.fetchall()
    return render(request,"Televisions.html",{"rec":rec})


def product_details(request,pid):
    msg=''
    cursor=connection.cursor()
    cursor.execute("select * from product where pid=%s", (pid,))
    rec=cursor.fetchone()
    print(rec)
    email1 = request.session.get('email1', None)
    m = request.POST.get("btn")   
    if m :
        m = int(m)  
        p1 = product.objects.filter(pid=m).first()
        if p1:
            pname1 = p1.pname
            price1 = p1.price        
            rec1 = cart(pid=m, pname=pname1, price=price1, email=email1)  
            rec1.save()
            msg = "Item added to cart!!"
    return render(request,"product_detail.html",{"rec":rec,"msg": msg})


@register.filter(name='split')
def split(value, key): 
 
    value.split("key")
    return value.split(key)
    
def adminpage(request):   
    if request.POST.get("operation"):
         if request.POST.get("operation")=="display":
            return redirect("/display")
         elif request.POST.get("operation")=="insert":
             return redirect("/insertrec")
         elif request.POST.get("operation")=="update":
             return redirect("/updaterec")
         elif request.POST.get("operation")=="delete":
             return redirect("/delrec")
    return render(request,"adminpage.html")


def display(request):
    rec=product.objects.all()
    if not rec:
        rec="No record exists"
    return render(request,"display.html",{"rec":rec})


def insertrec(request):
    msg={}
    print( request.POST.get("pname"), request.POST.get("Sdescription"), request.POST.get("Ldescription"), request.POST.get("price"), request.POST.get('category'))
    if  request.POST.get("pname") and request.POST.get("Sdescription") and request.POST.get("Ldescription") and request.POST.get("price") and request.POST.get('category'):
        rec=product(pname=request.POST.get("pname"),Sdescription=request.POST.get("Sdescription"),Ldescription=request.POST.get("Ldescription"),price=request.POST.get("price"),photo1=request.FILES.get("photo1"),photo2=request.FILES.get("photo2"),photo3=request.FILES.get("photo3"),category=request.POST.get("category"))
        rec.save()
        msg={"msg":"Record Inserted..."}
    return render(request,"insertrec.html",msg)


def updaterec(request):
    data = {}
    if request.POST.get("f"):
        given_pid = int(request.POST.get("pid"))
        product_list = product.objects.filter(pid=given_pid)
        
        if product_list.exists():
            rec = product_list[0] 
            data = {
                "pid": rec.pid,
                "pname": rec.pname,
                "Sdescription": rec.Sdescription,
                "Ldescription": rec.Ldescription,
                "price": rec.price,
                "category": rec.category,
                "photo1": rec.photo1,
                "photo2": rec.photo2,
                "photo3": rec.photo3
            }
            print(data)
        else:
            data = {"msg": "Product does not exist"}
    
    if request.POST.get("u"):
        print("in update")
        pid=int(request.POST.get("pid"))
        if pid!=0:
            print(pid)
            rec=product.objects.get(pid=pid)
            rec.pname=request.POST.get("pname")
            rec.Sdescription=request.POST.get("Sdescription")
            rec.Ldescription=request.POST.get("Ldescription")
            rec.price=request.POST.get("price")
            rec.photo1=request.FILES.get("photo1")
            rec.photo2=request.FILES.get("photo2")
            rec.photo3=request.FILES.get("photo3")
            rec.category=request.POST.get("category")
            rec.save()
            data={"msg":"Product details updated"}
    return render(request,"updaterec.html",data)


def delrec(request):
    data={}
    rec=product.objects.all()   
    pid1=request.POST.get("pid")
    
    if request.POST.get("Submit"):
        if product.objects.filter(pid=pid1).exists():
            drec=product.objects.get(pid=int(request.POST.get("pid")))
            drec.delete()
            data={"msg1":"Product deleted successfully!"}
            rec=product.objects.all() 
        else:
            data={"msg1":"Product doesnot exists"}

    return render(request,"delrec.html",{"rec":rec,"msg1":data})


def cart_display(request):
    msg1 = ''
    email1 = request.session.get('email1', None)
    print(email1)

    
    rec = cart.objects.filter(email=email1)  

    if request.POST.get("btn"):
        drec = cart.objects.get(cart_id=int(request.POST.get("btn")))
        drec.delete()
        msg1 = "Deleted from Cart"
   
   
    cursor1 = connection.cursor()
    cursor1.execute("SELECT SUM(price) FROM cart WHERE email = %s", (email1,))
    a = cursor1.fetchone()
    b = a[0] if a is not None else 0 

    if request.POST.get("buy"):
        return redirect("/bill1")
    
    return render(request, "cart_display.html", {"rec": rec, "a": b, "msg1": msg1})



def bill1(request):
    
    msg = {}
    email1 = request.session.get('email1', None)
    add1 = request.POST.get("address")
    mode = request.POST.get("mode")
    request.session['address'] = add1
    request.session['mode'] = mode
    
    cursor4 = connection.cursor()
    cursor4.execute("SELECT TIME(current_time())")
    x = cursor4.fetchone()
    x_str = x[0].strftime('%H:%M:%S')
    request.session['x']=x_str
    
   
    cart_items = get_list_or_404(cart, email=email1)

    for cart_item in cart_items:
        if add1 and mode:
            pname = cart_item.pname
            price = cart_item.price
            pid = cart_item.pid
           
            bill_record = bill(address=add1, payment=mode, email=email1, pname=pname, price=price, pid=pid, uni=x_str)
            bill_record.save()
            msg = {"msg": "Records Inserted..."}
    if msg:

      return redirect("/bill_display")

    return render(request, "bill1.html", msg)


def bill_display(request):

    email1=request.session.get('email1',None)
    cursor1 = connection.cursor()
    cursor1.execute("SELECT cname,email FROM customer WHERE email = %s", (email1,))
    a = cursor1.fetchall()
    
    add1=request.session.get('address')
    mode=request.session.get('mode')
    x1=request.session.get('x')

    cursor6 = connection.cursor()
    cursor6.execute("SELECT pid,pname,price,count(pname) FROM bill WHERE uni = %s group by pname order by pid", (x1,))
    p = cursor6.fetchall()

    #rec = bill.objects.filter(uni=x1)

    cursor2 = connection.cursor()
    cursor2.execute("SELECT SUM(price) FROM bill WHERE uni = %s ", (x1,))
    amt = cursor2.fetchone()
    amt = amt[0] if a is not None else 0 


    cursor3 = connection.cursor()
    cursor3.execute("SELECT CURRENT_DATE()")
    y = cursor3.fetchone() 
    
    cursor5 = connection.cursor()
    cursor5.execute("delete FROM cart WHERE email = %s", (email1,))
    
    return render(request,"bill_display.html",{"a":a,"b":add1, "c":mode,"amt":amt,"x":x1,"y":y,"p":p})


def c_update(request):

    email1=request.session.get('email1')

    rec=customer.objects.get(email=email1)
    if rec:
        email1=rec.email
        pass1=rec.pass1
        data={"email":email1,"cname":rec.cname,"contact":rec.contact}
        print(data)

        if request.POST.get("u"):
            rec.cname=request.POST.get("cname")
            rec.contact=request.POST.get("contact")
            rec.save()
            data={"msg":"Details updated.." , "email":email1,"cname":rec.cname,"contact":rec.contact}
            print(data)

        if request.POST.get("p"):
            pass_1=request.POST.get("pass_1")
            pass2=request.POST.get("pass2")
            pass3=request.POST.get("pass3")
            if not pass_1 and not pass2 and not pass3:
                data={"msg1":"All fields are mandatory","email":email1,"cname":rec.cname,"contact":rec.contact}
            else:
                if pass_1==pass1:
                    if pass2==pass3:
                        if pass2==pass_1:
                            data={"msg1":"Old password and new password cannot be same","email":email1,"cname":rec.cname,"contact":rec.contact}
                        else:
                            rec.pass1=pass2
                            rec.save()
                            data={"msg1":"Password updated","email":email1,"cname":rec.cname,"contact":rec.contact}
                    else:
                        data={"msg1":"New password and confirm new password doesnot match","email":email1,"cname":rec.cname,"contact":rec.contact}
                else:
                    data={"msg1":"Old Password doesnot match","email":email1,"cname":rec.cname,"contact":rec.contact}
    return render(request,"c_update.html",data)


def feedback(request):

    feedback=request.POST.get("feedback")
    email1=request.session.get("email1")
    rec=customer.objects.get(email=email1)
    if rec:
        email1=rec.email
        data={"cname":rec.cname}
        print(data)

        if feedback:
            feed1=feed(feedback=feedback,cname=rec.cname,email=email1)
            feed1.save()
            data={"cname":rec.cname,"msg":"Feedback Submitted"}

    return render(request,"feedback.html",data)