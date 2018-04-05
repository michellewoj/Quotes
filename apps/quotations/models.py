# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from datetime import datetime, timedelta
import bcrypt #for enctypting passwords
import re #for testing/matching regular expressions

class UserManager(models.Manager):
    def registration_valid(self, postData):
        errors = {}
        if len(postData['name']) < 3: #null or invalid
            errors['name'] = "Your name must have at least 3 characters."
        if len(postData['alias']) < 3: #null or invalid
            errors['alias'] = "Your alias must have at least 3 characters."
        if len(postData['email']) < 3: #null or invalid
            errors['email'] = "Your email must have at least 3 characters."
        #check if email is already in database
        if User.objects.filter(email=postData['email']): #email already in db
            errors['dup_email'] = "That email already exists."
        if len(postData['password']) < 1: #null or invalid
            errors['password'] = "Please enter a valid password. Password must be at least 8 characters, include one uppercase letter and one number."
        if postData['pwconf'] != postData['password']: #passwords do not match
            errors['pwconf'] = "The password you entered does not match. Please try again."
        return errors

#email regex

    def login_valid(self, postData):
        errors = {}
        try:
            user = User.objects.get(email=postData['email'])
            if not bcrypt.checkpw(postData['password'].encode(), user.password.encode()): #passwords do not match
                errors['bad_login'] = "You have entered an invalid email or password."
        except User.DoesNotExist:
            errors['bad_login'] = "It doesn't look like you've registered. Please register!"
        return errors

    def create_user(self, postData):
        name = postData['name']
        alias = postData['alias']
        email = postData['email']
        enc_pw = bcrypt.hashpw(postData['password'].encode(), bcrypt.gensalt())
        user = self.create(name=name, alias=alias, email=email, password=enc_pw)
        return user

class QuoteManager(models.Manager):
    #validations here
    def newquote_valid(self, postData):
        errors = {}
        #check if quote is already in database
        if len(postData['author']) < 1: #null
            errors['author'] = "Please enter the author of the quote you'd like to add."
        if len(postData['author']) < 3: #not long enough
            errors['author'] = "The author's name must be greater than 3 characters."
        if Quote.objects.filter(message=postData['message']): #quote already in db
            errors['dup_quote'] = "Someone has already added that quote. Would you like to add a different one?"
        if len(postData['message']) < 1: #null
            errors['review'] = "Please enter a quote that you would like to add."
        if len(postData['message']) < 10: #null
            errors['review'] = "Your quote doesn't seem long enough. Quotes must be greater than 10 characters. Please try again."
        return errors

    def create_quote(self, postData, user_id):
        #create the quote, with author and user attached
        author = postData['author']
        message = postData['message']
        user = User.objects.get(id=user_id)
        new_quote = self.create(message=message, author=author, user=user)
        return new_quote

    def favorite_quote(self, user_id, quote_id):
        user = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        quote.user_favorited.add(user)
        return quote

    def unfavorite_quote(self, user_id, quote_id):
        user = User.objects.get(id=user_id)
        quote = Quote.objects.get(id=quote_id)
        quote.user_favorited.remove(user)
        return quote

    def get_all_quotes(self):
        all_quotes = []
        quotes = Quote.objects.all()
        for quote in quotes:
            print quote.id, quote.quote
            all_quotes.append({'quote_id': quote.id, 'message': quote.message, 'author': quote.author})
            print all_quotes

class User(models.Model):
    name = models.CharField(max_length=255)
    alias = models.CharField(max_length=100)
    email = models.CharField(max_length=255)
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = UserManager()

    def __str__(self):
	    return 'User Info: %s %s %s' % (self.name, self.alias, self.email)

class Quote(models.Model):
    author = models.CharField(max_length=255)
    message = models.CharField(max_length=255)
    user = models.ForeignKey(User, related_name="quotes", null=True)
    user_favorited = models.ManyToManyField(User, related_name="favorites")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = QuoteManager()

    def __str__(self):
	    return 'Quote Info: %s %s %s' % (self.author, self.message, self.user)
