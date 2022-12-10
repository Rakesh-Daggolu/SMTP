from django.shortcuts import render,get_object_or_404,redirect
from blogApp.models import *
from blogApp.forms import *
from django.core.mail import send_mail
from taggit.models import Tag
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
import smtplib,ssl
import time,random

optsent=0
timeprev=0.0
def Signup(request):
    form=SignupForm()
    if request.method=="POST":
        form=SignupForm(request.POST)   #filling the details
        if form.is_valid():

            url=''
            d=form.clean()
            for x in d.keys():
                url=x+"="+d[x]+"&"+url
            global otpsent,timeprev
            otpsent=random.randrange(10000,20000)
            timeprev=time.time();
            send_mail('Verification',str(otpsent),'djangoproj6666@gmail.com',[str(form.cleaned_data['email'])],fail_silently=False)
            return redirect('/verification/?'+url)
    return render(request,'blogApp/signup.html',{'form':form})

def Verify(request,id=None):
    otpform=OtpForm()
    form=SignupForm(request.GET)
    flag=False
    msg=''
    if request.method=="POST":
         otpform=OtpForm(request.POST)
         if otpform.is_valid():
             if form.is_valid():
               global otpsent,timeprev
               otprecv=otpform.cleaned_data['Otp']
               if otpsent==otprecv and time.time()-timeprev<120:
                    send_mail("Blog Project","thank you for login",'djangoproj6666@gmail.com',[str(form.cleaned_data['email'])],fail_silently=False) #smtplib.smtperro
                    #send_mail(  sub        ,    msg ,   from ,[to],                      ,)
                    s=form.save(commit=True)
                    s.set_password(s.password)
                    s.save()
                    return redirect('/')
               elif otpsent!=otprecv:
                   flag=True
                   msg="invalid otp please fill form again"
               else:
                   flag=True
                   msg="otp expired please fill form again"


    return render(request,'blogApp/verification.html/',{'form':otpform,'msg':msg,'flag':flag})

def post_list_view(request,tag_slug=None):         #to list all posts
    post_list=Post.objects.all()
    tag=None
    if tag_slug!=None:
        tag=get_object_or_404(Tag,slug=tag_slug)    #Tag table contains 2 fields name,slug
        post_list=post_list.filter(tags__in=[tag])
    p=Paginator(post_list,2)
    page_number=request.GET.get('page')
    try:
        post_list=p.page(page_number)
    except PageNotAnInteger:
        post_list=p.page(1)
    except EmptyPage:
        post_list=p.page(p.num_pages)
    return render(request,'blogApp/post_list.html',{'post_list':post_list,'tag':tag})

@login_required
def post_detail_view(request,id):                 # specific post
    post=Post.objects.get(id=id)
    form=CommentForm()
    if request.method=="POST":
        form=CommentForm(request.POST)
        if form.is_valid():
            new_comment=form.save(commit=False)   #name,mail,body are saved  and created_at ,updated_at by default added
            new_comment.post=post                #but post is not added by default so we will have to assign it
            new_comment.save()
    form=CommentForm()
    comment_list=post.comments.all()
    return render(request,'blogApp/post_detail.html',{'post':post,'form':form,'comment_list':comment_list})

def sharemail(request,id):
    post=Post.objects.get(id=id)   # getting 1st record from db
    sent=False
    if request.method=="POST":
        form=PostMail(request.POST)  #fill the form with values
        if form.is_valid():
            cd=form.cleaned_data            #getting data from form

            smtp_server = "smtp.gmail.com"
            port = 587  # For starttls
            sender_mail=str(cd['Email'])    #from email
            receiver_mail=str(cd['To'])     # To
            password=str(cd['Password'])   #mail password
            # Create a secure SSL context
            context = ssl.create_default_context()

            # Try to log in to server and send email
            try:
              server = smtplib.SMTP(smtp_server,port)
              server.ehlo() # Can be omitted
              server.starttls(context=context) # Secure the connection
              server.ehlo() # Can be omitted
              server.login(sender_mail, password)      #login into smtp server
              server.sendmail(sender_mail,[receiver_mail],post.body)
              #sendmail(from,to,msg)

              #send_mail(post.title,post.body,'djangoproj6666@gmail.com',[str(cd['To'])],fail_silently=False)
              sent=True
            except Exception as e:
                   print(e)
            finally:
                server.quit()
            #send_mail(post.title,post.body,'djangoproj6666@gmail.com',[str(cd['To'])],fail_silently=False)

    else:
        form=PostMail()
    return render(request,'blogApp/sharemail.html',{'form':form,'sent':sent})
