##quote/views.py
## description: logic to handle URL requests

from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
import time
import random

from datetime import datetime, timedelta

daily_specials = [
    "Spaghetti",
    "Lasagna",
    "Macaroni and Cheese",
]

menu_prices = {
    "Spaghetti": 15,
    "Lasagna": 20,
    "Macaroni and Cheese": 10,
    "Cheese Pizza": 12,
    "Pepperoni Pizza": 15,
    "Sausage Pizza": 18,
    "White Pizza": 14,
}

def main(request):
    ''' A function to respond to the /main URL.
    '''
    # this template will present the response
    template_name = "restaurant/main.html"


    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
    }

    # delegate response to the template:
    return render(request, template_name, context)

def order(request):
    '''
    A function to respond to the /restaurant/order URL.
    This function will delegate work to an HTML template.
    '''
    rndm = random.randint(0,2)
    # this template will present the response
    template_name = "restaurant/order.html"

    # create a dictionary of context variables
    context = {
        'current_time': time.ctime(),
        'daily_special': daily_specials[rndm],
        'special_price': menu_prices[daily_specials[rndm]],
    }

    # delegate response to the template:
    return render(request, template_name, context)

def confirmation(request):
    ''' A function to respond to the /restaurant/confirmation URL. '''
    if request.method == 'POST':
        selected_items = request.POST.getlist('items')
        customer_name = request.POST.get('name')
        customer_email = request.POST.get('email')
        
        # Calculate a ready time 30-60 minutes from now
        now = datetime.now()
        minutes_add = random.randint(30, 60)
        ready_time = (now + timedelta(minutes=minutes_add)).strftime("%H:%M %p")

    context = {
        'current_time': time.ctime(),
        'ordered_items': selected_items,
        'customer_name': customer_name,
        'customer_email': customer_email,
        'ready_time': ready_time,
    }
    return render(request, 'restaurant/confirmation.html', context)
