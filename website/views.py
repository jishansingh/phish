from django.shortcuts import render
from .models import Website
from django.shortcuts import get_object_or_404
from selenium import webdriver
from time import sleep
# Create your views here.
def index(request):
    return render(request,'index.html')
def ViewPage(request,website):
    website=get_object_or_404(name=website)
    context = {'data':website.pages.all()[0],}
    return render(request,'home.html',context)
def new(request,website):
    if request.method=='POST':
        driver = webdriver.Chrome('./chromedriver')
        driver.get(website)
        sleep(2)
        data=driver.page_source
        data =data.replace('&lt;','<')
        data =data.replace('&gt;','>')
        data =data.replace('&#39;','\'')
        data =data.replace('&quot;','"')
        data =data.replace('&amp;','&')
        context = {'data':data,}

    return render(request,'home.html',context)