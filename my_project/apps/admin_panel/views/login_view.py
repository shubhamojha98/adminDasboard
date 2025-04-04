from django.shortcuts import render, redirect
import datetime
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
import jwt
from django.conf import settings
from django.contrib import messages
from apps.admin_panel.models.auth_model import AuthModel
from django.contrib.auth.hashers import check_password

# Static credentials
USERNAME = "admin"
PASSWORD = "12345"

# Generate JWT Token


def generate_jwt_token(username):
    payload = {
        "username": username,
       "exp": datetime.datetime.now(datetime.timezone.utc) + datetime.timedelta(minutes=30),  # Expiry time
        "iat": datetime.datetime.now(datetime.timezone.utc)  # Issued at
    }
    token = jwt.encode(payload, settings.SECRET_KEY, algorithm="HS256")
    return token


@csrf_exempt  # Disable CSRF for testing purposes
def login_view(request):
    if request.method == "POST":
        post_data={
        "username" :request.POST.get("username"),
        "password" : request.POST.get("password"),
        "remember_me" : request.POST.get("remember_me"),
        "lat":request.POST.get('latitude'),
        "long":request.POST.get("longitude")
        }
        
        user=AuthModel.login(post_data,request)

        # if details  and username == details['user_name'] and check_password(password, details['password'] ): #for hashed password
        # if details and username == details['user_name'] and password == details['password']:
        if user:
            token = generate_jwt_token(username)  # Generate JWT token
            response = redirect("dashboard")  # Redirect to dashboard
            response.set_cookie("jwt_token", token, httponly=True, samesite="Lax")  # Store token in cookie
            response.set_cookie("username", user['user_name'], max_age=3600)
            response.set_cookie("password", user['password'], max_age=3600)
            return response
        else:
             messages.add_message(request,messages.ERROR, 'Invalid username or password.')
             return  redirect("login") 
    return render(request, "admin_panel/login.html")

#old code backup
# def login_view(request):
#     if request.method == "POST":
#         post_data={
#         "username" :request.POST.get("username"),
#         "password" : request.POST.get("password"),
#         "remember_me" : request.POST.get("remember_me"),
#         "lat":request.POST.get('latitude'),
#         "long":request.POST.get("longitude")
#         }
        
#         # details=AuthModel.get_user_by_username(username)

#         # if details  and username == details['user_name'] and check_password(password, details['password'] ): #for hashed password
#         if details and username == details['user_name'] and password == details['password']:
#             token = generate_jwt_token(username)  # Generate JWT token
#             response = redirect("dashboard")  # Redirect to dashboard
#             response.set_cookie("jwt_token", token, httponly=True, samesite="Lax")  # Store token in cookie
#             return response
#         else:
#              messages.add_message(request,messages.ERROR, 'Invalid username or password.')
#              return  redirect("login") 
#     return render(request, "admin_panel/login.html")

    

# def login_view(request):
#     if request.method == "POST":
#         username = request.POST.get("username")
#         password = request.POST.get("password")

#         if username == USERNAME and password == PASSWORD:
#             return redirect("dashboard")
#         else:
#             return render(request, "admin_panel/login.html", {"error": "Invalid Credentials"})

#     return render(request, "admin_panel/login.html")
