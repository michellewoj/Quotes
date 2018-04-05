# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, HttpResponse, redirect
from django.core.urlresolvers import reverse
from django.contrib import messages
from django.contrib.auth import authenticate, login
from .models import User, Quote

def index(request):
    return render(request, 'quotations/index.html')

def register(request):
    errors = User.objects.registration_valid(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect(reverse('main'))
    else:
        user = User.objects.create_user(request.POST)
        request.session['user_id'] = user.id
        return redirect('/quotes')

def login(request):
    errors = User.objects.login_valid(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags = tag)
        return redirect('/main')
    else:
        user = User.objects.get(email=request.POST['email'])
        request.session['user_id'] = user.id
        return redirect('/quotes')

def quotes(request):
    if 'user_id' not in request.session:
        return redirect(reverse('main'))
    context = {
        'user': User.objects.get(id=request.session['user_id']),
        'quotes': Quote.objects.exclude(user_favorited__id=request.session['user_id']),
        'favorites': Quote.objects.filter(user_favorited__id=request.session['user_id'])
    }
    return render(request, 'quotations/quotes.html', context)

def add(request):
    if 'user_id' not in request.session:
        return redirect('/main')
    # request.session['author'] = request.POST['author']
    # request.session['message'] = request.POST['message']
    errors = Quote.objects.newquote_valid(request.POST)
    if len(errors):
        for tag, error in errors.items():
            messages.error(request, error, extra_tags=tag)
        return redirect(reverse('quotes'))
    else:
        user_id = request.session['user_id']
        quote = Quote.objects.create_quote(request.POST, user_id)
        request.session['quote_id'] = quote.id
    return redirect('/quotes')

def favorite(request, quote_id):
    Quote.objects.favorite_quote(request.session['user_id'], quote_id)
    return redirect('/quotes')

def unfavorite(request, quote_id):
    Quote.objects.unfavorite_quote(request.session['user_id'], quote_id)
    return redirect('/quotes')

def userpage(request, user_id):
    user = User.objects.get(id=user_id)
    quotes = Quote.objects.filter(user=user)
    context = {
        'user': user,
        'quotes': quotes,
        'length': len(quotes)
    }
    return render(request, 'quotations/user.html', context)

def logout(request):
    for i in request.session.keys():
        del request.session[i]
    return render(request, 'quotations/index.html')
