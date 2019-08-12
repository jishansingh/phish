from django.shortcuts import render
from .models import Website,Page
from django.shortcuts import get_object_or_404
from selenium import webdriver
from time import sleep
from .forms import WebsiteForm
from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
import re
# Create your views here.
def index(request):
    return render(request,'index.html')
@csrf_exempt
def ViewPage(request,website):
    if request.method=='POST':
        print(request.POST)
        d=re.compile(r'http(s)://')
        website=Website.objects.filter(name__contains=website)
        context = {'data':website.pages.all()[1],}
        return render(request,'home.html',context)
    website=get_object_or_404(Website,name=website)
    context = {'data':website.pages.all()[0],}
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