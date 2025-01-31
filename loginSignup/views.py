from django.shortcuts import render, redirect
from django.contrib.auth.models import auth, User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.mail import send_mail
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.utils.encoding import force_bytes, force_str
from django.template.loader import render_to_string
from django.contrib.sites.shortcuts import get_current_site
from django.contrib.auth.tokens import default_token_generator
from django.http import HttpResponse

def login(request):
    if request.method=='POST':
        username=request.POST['username']
        password=request.POST['password']
        user=auth.authenticate(username=username, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect('about')
        else:
            messages.info(request, 'invalid credentials')
            return redirect('login')
    else:
        return render(request, 'login.html')
        
def logout(request):
    auth.logout(request)
    return redirect('/')

#Register using verification
def signup(request):
    if request.method == 'POST':
        fname = request.POST['fname']
        lname = request.POST['lname']
        email = request.POST['email']
        username = request.POST['username']
        pass1 = request.POST['password1']
        pass2 = request.POST['password2']

        print("Received Signup Request")

        if pass1 == pass2:
            if User.objects.filter(email=email).exists():
                print("Email already exists")
                messages.info(request, 'Email is already taken')
                return redirect('signup')
            else:
                user = User.objects.create_user(username=username, password=pass1, email=email, first_name=fname, last_name=lname)
                user.is_active = False
                user.save()

                print("User created successfully, sending email...")

                # Send verification email
                send_verification_email(request, user, email)

                messages.success(request, "Account created! Please check your email to verify your account.")
                return render(request, 'authenticate.html')
        else:
            print("Passwords do not match")
            messages.info(request, 'Passwords do not match')
            return redirect('signup')
    else:
        return render(request, 'signup.html')

    
def send_verification_email(request, user, to_email):
    try:
        current_site = get_current_site(request)
        mail_subject = "Activate Your Account"
        message = render_to_string('email_verification.html', {
            'user': user,
            'domain': current_site.domain,
            'uid': urlsafe_base64_encode(force_bytes(user.pk)),
            'token': default_token_generator.make_token(user),
        })

        print("Generated email message:", message)

        send_mail(
            mail_subject,
            message,
            'patolesahil5@gmail.com',
            [to_email],
            fail_silently=False,
        )

        print("Email sent successfully.")
    except Exception as e:
        print("Error sending email:", e)

def activateEmail(request, user, to_email):
    current_site = get_current_site(request)
    mail_subject = "Activate Your Account"
    message = render_to_string('email_verification.html', {
        'user': user,
        'domain': current_site.domain,
        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
        'token': default_token_generator.make_token(user),
    })
    send_mail(mail_subject, message, 'patolesahil5@gmail.com', [to_email], fail_silently=False)

def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except (TypeError, ValueError, OverflowError, User.DoesNotExist):
        user = None

    if user is not None and default_token_generator.check_token(user, token):
        user.is_active = True
        user.save()
        messages.success(request, "Your account has been verified! You can now log in.")
        return redirect('login') 
    else:
        return HttpResponse('Activation link is invalid!', status=400)


@login_required(login_url="login")
def about(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return render(request, 'about.html')
        else:
            return redirect('login')
    else:
        return render(request, 'signup.html')


def index(request):
    return render(request, 'index.html')
    
    




# def index(request):
#     pass