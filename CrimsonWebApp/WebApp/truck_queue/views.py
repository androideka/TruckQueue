# Django
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.sites.models import Site
from django.core.mail import EmailMultiAlternatives
from django.template.loader import get_template
from django.template import Context, RequestContext

# Python
from datetime import datetime
#eventually, for sanitizing user input
import re
import string
import random
import json
import ast

# Twilio stuff
from django_twilio.decorators import twilio_view
from twilio.twiml import Response
from twilio.rest import TwilioRestClient

# Our stuff
from .models import *

# Create your views here.

week = ['Sunday',
        'Monday',
        'Tuesday',
        'Wednesday',
        'Thursday',
        'Friday',
        'Saturday']

today = week[datetime.today().weekday()]

today = 'Tuesday'


def home(request):
    return render(request, 'truck_queue/home.html')

def auth_login(request):
    if request.method == 'POST':
        user = authenticate(username=request.POST['user_name'], password=request.POST['password'])
        employee = Employee.objects.get(username=user)
        if user is not None and user.is_active is True and employee.strikes < 3:
            login(request, user)
            truck_info = get_menu()
            return render(request, 'truck_queue/home.html',
                          {'message': 'You\'ve successfully signed in!',
                           'truck': truck_info['truck'],
                           'menu': truck_info['menu']})
        else:
            return render(request, 'registration/login.html',
                          {'message': 'The username and/or password is incorrect.'})
    else:
        return render(request, 'registration/login.html')

@login_required
def log_out(request):
    logout(request)
    return render(request, 'truck_queue/home.html',
                  {'message': 'You have successfully logged out.'})

def registration_register(request):
    if request.method == 'POST':
        username = request.POST['user_name']
        first_name = request.POST['first_name']
        last_name = request.POST['last_name']
        email = request.POST['email']
        phone = request.POST['phone']
        password1 = request.POST['password1']
        password2 = request.POST['password2']
        if password1 != password2:
            return render(request, 'registration/registration_form.html',
                          {'message': 'Your passwords did not match. Try again'})
        user = User.objects.filter(username=username)
        if not user:
            new_user = User.objects.create_user(username=username, email=email, password=password1,
                                                first_name=first_name, last_name=last_name)
            new_emp = Employee.objects.create(username=new_user, phone=phone,
                                              activation_number=generate_activation_code())
            new_emp.save()
            new_user.is_active = False
            new_user.save()
            send_activation_email(request, new_emp)
            return render(request, 'registration/registration_complete.html')

        else:
            return render(request, 'registration/registration_form.html',
                          {'message': 'That username has been taken, please choose another.'})
    else:
        return render(request, 'registration/registration_form.html')

def activate(request, activation_key):
    employee = Employee.objects.get(activation_number=activation_key)
    user = User.objects.get(employee=employee)
    user.is_active = True
    user.save()
    return render(request, 'registration/activation_complete.html')

def contact(request):
    return render(request, 'truck_queue/contact.html')

def shop(request):
    truck_info = get_menu()
    truck = truck_info['truck']
    entrees = MenuItems.objects.filter(is_side=False, truck=truck)
    sides = MenuItems.objects.filter(is_side=True, truck=truck)
    # ratingCount = RatingCount.objects.all()
    return render(request, 'truck_queue/shop.html',
                  {'truck': truck, 
                   'entrees': entrees,
                   'sides': sides})

def order_confirm(request):
    var = json.dumps(request.GET, ensure_ascii=False)
    var = ast.literal_eval(var)
    names = []
    prices = []
    quantities = []
    context = {'error': 'The order was tampered with, and thus cannot be processed.'}

    for key, value in var.iteritems():
        print "Now we're here"

        found_food_name = find_name(key)
        menu_item = is_same_as_db(found_food_name)

        if menu_item is not None:
            names.Add(found_food_name)
        else:
            print "We're here"
            render(request, 'truck_queue/shop.html', context)

        find_value_type = find_number_type(value)
        if find_value_type == "float":
            prices.Add(value)
        elif find_value_type == "int":
            quantities.Add(value)
        else:
            render(request, 'truck_queue/shop.html', context)

    send_order_email(names, prices, quantities, "")
    return render(request, 'truck_queue/order_confirmation.html')

def is_same_as_db(name):
    truck_info = get_menu()
    return MenuItems.objects.get(name=name, truck=truck_info['truck'])

def find_name(food_string):
    if len(food_string) > 10:
        food_string = food_string[11:]
        name = ""
        for i in xrange(len(food_string)):
            if food_string[i] == ']':
                break          
            name += food_string[i]
        return name
    return ""

def find_number_type(number_string):
    try:
        int(number_string)
        return "integer"
    except ValueError:
        try: 
            float(number_string)
            return "float"
        except ValueError:
            return ""


def send_order_email(names, prices, quantity, emailAddress):
     subject = 'Truck Queue Order Confirmation'
     #message_html = get_template('registration/confirmation_email')
     emailBody = '''
        You just got your order, son.
     '''
     message = EmailMultiAlternatives(subject, emailBody, 'info@truckqueue.com', ['youngco@advisory.com'])
     message.send()

def get_menu():
    truck = Truck.objects.get(truck_day=today)
    menu = MenuItems.objects.filter(truck=truck)
    return {'menu': menu,
            'truck': truck}

def send_activation_email(request, new_user):
    subject = 'Truck Queue User Registration'
    message_html = get_template('registration/activation_email.html')
    message_txt = get_template('registration/activation_email.txt')
    email = request.POST['email']
    context = Context({'email': email,
                       'activation_key': new_user.activation_number,
                       'expiration_days': 7,
                       'site': Site.objects.get_current()})
    message_html = message_html.render(context)
    message_txt = message_txt.render(context)
    message = EmailMultiAlternatives(subject, message_txt, 'info@truckqueue.com', [email])
    message.attach_alternative(message_html, 'text/html')
    message.send()

def generate_activation_code(size=15, chars=string.digits):
    return ''.join(random.choice(chars) for _ in range(size))

# Use Twilio to send text
def sendText(message_body, number):
    client = TwilioRestClient('AC6dd06745bc549844a50812e5e6704641', '2db43dd1e82eb4c19c82b12e6df891c3')

    message = client.messages.create(body=message_body,
                                     to=number,
                                     from_='+15123593110')
    print message.sid

# Receive text
@twilio_view
def sms(request):
    msg = request.POST.get('Body', '')

    if msg[:9] == 'Not coming':
        showingUp(1, '')
    elif msg[:10] == 'Arriving at':
        showingUp(2, msg[12:16])
    elif msg[:3] == 'Here':
        showingUp(3, '')
    elif msg[:3] == 'Gone':
        showingUp(4, '')
    elif msg[4:11] == 'finished':
        completeOrder(msg[:2], True)
    elif msg[4:13] == 'unfinished':
        completeOrder(msg[:2], False)
    elif msg[4:7] == 'left':
        leftOrder(msg[:2])
    else:
        response = Response()
        response.message('Your message was not in the correct format. Please try again.')
        return response

# Order complete
def completeOrder(order_number, status):
    # Get phone number/name from db using orderNumber
    order = Order.objects.get(number=order_number)
    user = Employee.objects.get(username=order.username)
    user_name = user.first_name
    user_number = user.phone

    # Create and send message to user to come pick up
    message_body = user_name + '! '

    if status is True:
        message_body += 'Your order (#%s) is done! Come get your grub!' % (order_number)
    else:
        message_body += 'Your order could not be completed. We sincerely apologize.'

    sendText(message_body, user_number)

# TODO Coming/Not
def showingUp(status, time):
    if status == 1:
        # Not coming
        event = 1
    elif status == 2:
        # Arriving at
        event = 2
    elif status == 3:
        # Here
        event = 3
    elif status == 4:
        # Gone
        event = 4

# No show?
def leftOrder(order_number):
    # Get user from db using orderNumber
    order = Order.objects.get(number=order_number)
    user = Employee.objects.get(username=order.username)
    user_name = user.first_name
    user_number = user.phone
    strikes = user.strikes

    # Add strike to user in db
    strikes += 1

    # Text user saying amount of strikes
    message_body = 'Hey %s, you forgot to get your order today. You have ' % (user_name)

    if strikes < 3:
        message_body += '%s strikes. If you get 3 strikes, you will no longer be able to order.' % strikes
    else:
        message_body += '%s strikes. As a result, you will no longer be able to place orders.' % strikes

    sendText(message_body, user_number)

def demo(request):
    sendText('Your order (#18) is done! Come get your grub!', '+12105428553')
    return HttpResponse("", content_type='text/html')
