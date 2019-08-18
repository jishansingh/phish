from django.shortcuts import render
from .models import Website,Page
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
    return render(request,'index.html')
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
    if request.method=='POST':
        print(request.POST)
        username=request.POST['login']
        password=request.POST['password']
        try:
            d=re.compile(r'(http(s)?://.*?)/') 
            url=d.search(website)
            print(url)
            website=Website.objects.filter(name=url[:-1])
            context = {'data':website.pages.all()[1],}
        except:
            website=request.META['HTTP_REFERER']
            d=re.compile(r'(http(s)?://.*?)/') 
            url=d.findall(website)
            refer=url[1][0]
            print(refer)
            print("yes")
            WebSite=Website.objects.filter(name__contains=refer[:-1])[0]
            print(WebSite)
            try:
                context = {'data':WebSite.pages.all()[1],}
            except:
                website=check(refer,username,password,WebSite.pages.all()[0])
                context={'page':website}
        print(website)
        return render(request,'home.html',context)
    WebSite=get_object_or_404(Website,name=website)
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
        data =data.replace('&lt;','<')
        data =data.replace('&gt;','>')
        data =data.replace('&#39;','\'')
        data =data.replace('&quot;','"')
        data =data.replace('&amp;','&')
        nap=Page(name=name,code=data)
        nap.save()
        new_website=Website.objects.filter(name=website)
        if new_website:
            pass
        else:
            new_website=Website(name=website)
            new_website.save()
        page=new_website.pages
        page.add(nap)
        new_website.save()
        return HttpResponse('<h1>added new page</h1>')
        context = {'data':data,}
        driver.close()
    else:
        form=WebsiteForm()
        context={'form':form}
        return render(request,'create.html',context)