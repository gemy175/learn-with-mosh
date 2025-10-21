from django.shortcuts import render
from django.http import HttpResponse

def say_hello(req):

    x = 1
    y = 2

    # return HttpResponse('hello from django')
    return render(req, 'hello.html' , {'name': 'ahmed' , 'age': 20})

