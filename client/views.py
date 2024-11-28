from django.shortcuts import render, redirect
from django.contrib.auth.models import User, auth
from django.contrib import messages
from django.core.mail import send_mail
from django.core.mail import send_mail, BadHeaderError
from django.conf import settings


def user(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        confirmpassword = request.POST.get('confirmpassword')
        if password == confirmpassword:
            if User.objects.filter(username=username).exists():
                messages.info(request, "Username already taken")
                return redirect('register')  
            elif User.objects.filter(email=email).exists():
                messages.info(request, "Email already taken")
                return redirect('register')  
            else:
                user_reg = User.objects.create_user(username=username, email=email, password=password)
                user_reg.save()

                # Send a welcome email
                send_mail(
                    subject="Welcome to Our Service",
                    message=f"Hi {username},\n\nThank you for registering with our service. We're excited to have you on board!\n\nBest regards,\nEvent Management Team",
                    from_email='northfieldhills@gmail.com',  
                    recipient_list=[email],
                    fail_silently=False,
                )

                messages.info(request, "Successfully created")
                return redirect('/') 
        else:
            messages.info(request, "Password doesn't match")
            return redirect('register')  

    return render(request, 'reg.html')


def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = auth.authenticate(username=username, password=password)
        if user is not None:
            auth.login(request, user)
            messages.info(request, "Login Success")
            return redirect('/')
        else:
            messages.info(request, "Invalid")
            return redirect('register') 

    return render(request, 'log.html')


def logout(request):
    auth.logout(request)
    return redirect('/')




def contact(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')  # Customer's email
        message = request.POST.get('message')

        # Compose the email to send to your admin email
        subject = f"New Contact Us Message from {name}"
        full_message = f"Name: {name}\nEmail: {email}\n\nMessage:\n{message}"

        try:
            send_mail(
                subject=subject,
                message=full_message,
                from_email=settings.EMAIL_HOST_USER,  
                recipient_list=['northfieldhills@gmail.com'], 
                fail_silently=False,
            )
            messages.success(request, "Thank you for contacting us! We'll get back to you soon.")
        except BadHeaderError:
            messages.error(request, "Invalid header found.")
        except Exception as e:
            messages.error(request, "Something went wrong. Please try again later.")
            print(f"Email error: {e}")

        return redirect('contact')  

    return render(request, 'contact.html')
