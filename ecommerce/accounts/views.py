
from django.shortcuts import render, redirect
from django.contrib import messages, auth
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError, transaction
import re

from .models import UserProfile


def User_register(request):

    if request.method == 'POST':
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        phone = re.sub(r'[\s()-]', '', request.POST.get('phone_number', ''))
        if phone.startswith('+976') and len(phone) == 12:
            phone = phone[4:]
        confirm_password = request.POST.get('confirm_password')

        if not re.fullmatch(r'\+?[0-9]{8,15}', phone) or len(phone) > 15:
            messages.error(request, 'Утасны дугаараа зөв оруулна уу!')
            return redirect('register')

        if password != confirm_password:
            messages.error(request, 'Нууц үг таарахгүй байна!')
            return redirect('register')

        if User.objects.filter(username=username).exists():
            messages.error(request, 'Энэ хэрэглэгчийн нэр бүртгэлтэй байна!')
            return redirect('register')

        if User.objects.filter(email=email).exists():
            messages.error(request, 'Энэ имэйл бүртгэлтэй байна!')
            return redirect('register')
        if UserProfile.objects.filter(phone_number=phone).exists():
            messages.error(request, "Энэ дугаар бүртгэлтэй байна!")
            return redirect('register')

        try:
            with transaction.atomic():
                user = User.objects.create_user(
                    first_name=first_name,
                    last_name=last_name,
                    username=username,
                    email=email,
                    password=password
                )
                UserProfile.objects.create(user=user, phone_number=phone)
        except IntegrityError:
            messages.error(request, 'Хэрэглэгчийн нэр эсвэл утасны дугаар бүртгэлтэй байна!')
            return redirect('register')

        messages.success(request, 'Амжилттай бүртгэгдлээ!')
        return redirect('signin')

    return render(request, 'accounts/register.html')


def User_login(request):

    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = auth.authenticate(
            username=username,
            password=password
        )

        if user is not None:
            auth.login(request, user)

            messages.success(
                request,
                'Амжилттай нэвтэрлээ!'
            )

            return redirect('profile')

        else:
            messages.error(
                request,
                'Хэрэглэгчийн нэр эсвэл нууц үг буруу байна!'
            )

            return redirect('signin')

    return render(request, 'accounts/signin.html')


@login_required(login_url='signin')
def User_logout(request):

    auth.logout(request)

    messages.success(
        request,
        'Системээс амжилттай гарлаа!'
    )

    return redirect('home')

@login_required(login_url='signin')
def User_profile(request):
    return render(request, 'accounts/profile.html')
