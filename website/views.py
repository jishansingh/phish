from django.shortcuts import render
from .models import Website,Page,Hash
from django.shortcuts import get_object_or_404
from selenium import webdriver
from time import sleep
from .forms import WebsiteForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from selenium.webdriver import ActionChains
from selenium.webdriver.common.keys import Keys
import re
# Create your views here.
def index(request):
    if request.method=="POST":
        ViewPage(request,"ab")
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
        user=Hash.objects.all()[0]
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
        nap=Page(name=website,code=data)
        nap.save()
        new_website=Website.objects.filter(name=name)
        if new_website:
            pass
        else:
            new_website=Website(name=name)
            new_website.save()
        page=new_website.pages
        page.add(nap)
        new_website.save()
        ji=Hash(user=request.user,website=new_website,hash_user="ab")
        ji.save()
        return HttpResponse('<h1>added new page</h1>')
        context = {'data':data,}
        driver.close()
    else:
        form=WebsiteForm()
        context={'form':form}
        return render(request,'create.html',context)