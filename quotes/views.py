##quote/views.py
## description: logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

# Create your views here.
""" def home(request):
    ''' A function to respond to the /hw URL.
    '''

    # create some text:
    response_text = f'''
    <html>
    <h1>Hellow, world!</h1>
    <p>This is the home page for the hw app.</p>
    <hr>
    This page was generated at {time.ctime()}.
    '''

    # return a response to the client
    return HttpResponse(response_text) """

quotes_list = [
    "We support Lady Gaga Being The Queen",
    "Da Vinki",
    "You're beautiful",
]

images_list = [
    "/static/lgbtq.png",
    "/static/davinki.jpeg",
    "/static/beautiful.jpeg",
]


def quotes(request):
    ''' A function to respond to the /quotes URL.
    '''
    rndm = random.randint(0,2)
    # this template will present the response
    template_name = "quotes/quotes.html"


    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'letter1': quotes_list[rndm], #a letter in the range A..Z
        'letter2': images_list[rndm], #a letter in the range A..Z
    }

    # delegate response to the template:
    return render(request, template_name, context)

def about(request):
    '''
    A function to respond to the /quotes/about URL.
    This function will delegate work to an HTML template.
    '''
    # this template will present the response
    template_name = "quotes/about.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template:
    return render(request, template_name, context)

def show_all(request):
    '''
    A function to respond to the /quotes/quote URL.
    '''
    template_name = "quotes/show_all.html"

    context = {
        'current_time': time.ctime(),
    }
    return render(request, template_name, context)
