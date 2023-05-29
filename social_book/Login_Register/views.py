
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.models import auth
# from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import UploadedFiles
from sqlalchemy import create_engine
from sqlalchemy import text
from django.core.mail import send_mail
import datetime
from django.utils import timezone
from .models import CustomUser
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .serializers import UploadedFilesSerializer
from django.core.exceptions import ValidationError
from django.contrib.auth.tokens import default_token_generator
from django.contrib.auth import get_user_model
from django.shortcuts import get_object_or_404
from django.contrib.auth.hashers import make_password
from django.urls import reverse_lazy
from django.urls import reverse
from datetime import date
from django.contrib.sessions.models import Session
import re
# from Login_Register.validators import UppercaseLowercaseValidator
# from django.contrib.auth.password_validation import BaseValidator
# from django_otp import devices
# from django_otp.plugins.otp_totp.models import TOTPDevice
# from .forms import EmailForm

User = get_user_model()


def validate_user_password(password):
    try:
        validate_password(password)
    except ValidationError as e:
        error_message = ", ".join(e.messages)
        return False, error_message

    return True, None

def login(request):
    if request.method == 'POST':
        email = request.POST['email']
        password = request.POST['password']

        try:
            user = CustomUser.objects.get(email=email)
        except CustomUser.DoesNotExist:
            messages.error(request, 'user does not exist')
            # return HttpResponse('user does not exist')

        user = auth.authenticate(email=email, password=password)

        if user is not None:
            auth.login(request, user)
            return redirect("index")
        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")
            # return HttpResponse('incorrect details')

    else:
        return render(request, "login.html")

def validate_password(password):
    if len(password) < 6:
        return False, "Password should be at least 6 characters long."
    
    if not re.search(r"[a-z]", password):
        return False, "Password should contain at least one lowercase letter."
    
    if not re.search(r"[A-Z]", password):
        return False, "Password should contain at least one uppercase letter."
    
    if not re.search(r"\d", password):
        return False, "Password should contain at least one number."
    
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False, "Password should contain at least one special character."
    
    return True, ""


def register(request):
    if request.method == 'POST':
        email = request.POST['email']
        password1 = request.POST['pass']
        print(password1)
        password2 = request.POST['cpass']
        public_visibility = bool(request.POST.get('public_visibility', False))
        full_name = request.POST['fname']
        city = request.POST['city']
        state = request.POST['state_name']
        dob = request.POST['date_of_birth']
        date_of_birth = datetime.datetime.strptime(dob, '%Y-%m-%d').date()
        today = timezone.now().date()
        age = today.year - date_of_birth.year
        if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day):
            age -= 1
        request.session['age'] = age
        print(age)

        if password1 == password2:
            # if password1.isupper():
            is_valid, error_message = validate_password(password1)
            if not is_valid:
                return render(request, 'register.html', {'error_message': error_message})

            if CustomUser.objects.filter(email=email).exists():
                messages.info(request, "Email already exist")
                return redirect('register')
            else:
                try:
                    # validator = UppercaseLowercaseValidator()
                    # validator.validate(password1)
                    # is_valid, error_message = validate_user_password(password1)
                    # if not is_valid:
                    #     return render(request, 'register.html', {'error_message': error_message})
                    # validate_user_password(password1)
                    user = CustomUser.objects.create_user(email=email, password=password1, full_name=full_name, city=city, state=state, public_visibility=public_visibility, age=age, date_of_birth=date_of_birth)
                    user.save()
                    messages.info(request, "User created")
                    return redirect('login')
                except ValidationError as e:
                    error_message = ", ".join(e.messages)
                    return render(request, 'register.html', {'error_message': error_message})      
        else:
            messages.info(request, "Password not matching..")
            return redirect('register')
        
    return render(request, 'register.html')
    
@login_required(login_url='login')
def index(request):
    # send_mail(
    #     'Welcome to Markytics Project',
    #     'Thankyou for sigining in to our website. We are available in social media platforms too. follow us to keep updated with our work.',
    #     'mishramanoj2106@gmail.com',
    #     ['manoj.mishra2106@gmail.com'],
    #     fail_silently=False,
    # )
    return render(request, 'index.html')

def logout(request):
    auth.logout(request)
    return redirect('login')

# def calculate_age(date_of_birth):
#     if date_of_birth is None:
#         return None
#     today = date.today()
#     age = today.year - date_of_birth.year
#     if today.month < date_of_birth.month or (today.month == date_of_birth.month and today.day < date_of_birth.day):
#         age -= 1
#     return age

@login_required
def profile(request):
    user = request.user
    age = None
    # age = request.session.get('age')

    if request.method == 'POST':
        email = request.POST.get('email')
        if not email:
            error_message = 'Email is required'
            return render(request, 'profile.html', {'user': user, 'error_message': error_message})
        user.full_name = request.POST.get('full_name')
        user.public_visibility = bool(request.POST.get('public_visibility'))
        user.city = request.POST.get('city')
        user.state = request.POST.get('state')
        date_of_birth = request.POST.get('date_of_birth')
        user.date_of_birth = date_of_birth
        # Convert the birth_date string to a date object.
        date_of_birth = date.fromisoformat(date_of_birth)
        # Use the datetime module to calculate the user's age.
        today = date.today()
        age = today.year - date_of_birth.year - ((today.month, today.day) < (date_of_birth.month, date_of_birth.day))
        # Save the user's age to the database.
        user = request.user
        user.age = age
        user.save()
        
        return redirect('profile')
    
    return render(request, 'profile.html')

def imageupload(request):
    user = request.user
    if request.method == 'POST':
        profile_image = request.FILES.get('profile_image')
        if profile_image:
            user.profile_image = profile_image
        user.save()
        return redirect('profile')
    return render(request, 'profile.html')

def forgotpassword(request):
    if request.method == 'POST':
        email = request.POST['email']
        user = User.objects.filter(email=email).first()

        if user:
            # Generate password reset token
            token = default_token_generator.make_token(user)

            # Create password reset URL
            reset_url = request.build_absolute_uri(reverse('passresetconfirm', kwargs={
                'uidb64': user.pk,
                'token': token,
            }))

            # Send password reset email
            send_mail(
                'Password Reset',
                f'You are receiving this email because you requested a password reset for your account at our website.Please reset your password using this URL: {reset_url}',
                'mishramanoj2106@gmail.com',
                ['manoj.mishra2106@gmail.com'],
                fail_silently=False,
            )

        # Redirect to password reset done page
        return redirect('passresetmsg')

    return render(request, 'forgotpass.html')

def passresetdone(request):
    return render(request, 'passresetdone.html')

def passresetmsg(request):
    return render(request, 'passresetmsg.html')

def passresetconfirm(request, uidb64, token):
    if request.method == 'POST':
        uid = uidb64
        user = get_object_or_404(User, pk=uid)

        # Verify the token
        if default_token_generator.check_token(user, token):
            password = request.POST['password']
            # Update the user's password
            user.password = make_password(password)
            user.save()

            # Redirect to password reset complete page
            return redirect('passresetdone')

    return render(request, 'passresetform.html', {'uidb64': uidb64, 'token': token})


def authorseller(request):
    results = CustomUser.objects.filter(public_visibility=True)
    return render(request, 'authorseller.html', {'results': results})

# def is_pdf_file(file):
    # mime_type = magic.from_buffer(file.read(), mime=True)
    # return mime_type == 'application/pdf'

def display_image(file):
    if file.name.lower().endswith('.pdf'):
        return True
    else:
        return False

def upload_book(request):
    if request.method == 'POST':
        title = request.POST['title']
        description = request.POST['description']
        visibility = bool(request.POST.get('visibility', False))
        cost = request.POST['cost']
        year_published = request.POST['year_published']
        file = request.FILES['file']
        is_pdf = display_image(file)
        
        # validations
        error_messages = []
        try:
            if len(description) > 200:
                error_messages.append('Description should not exceed 200 characters.')
                
            if len(title) > 20:
                error_messages.append('Title should not exceed 50 characters.')
                    
            cost = float(cost)
            if cost < 0:
                error_messages.append('Cost cannot be negative.')
            
            year_published = int(year_published)
            current_year = datetime.date.today().year
            if year_published > current_year:
                error_messages.append('Year published cannot be in the future.')
        except ValueError:
            error_messages.append('Invalid field value.')
        
        if error_messages:
            for message in error_messages:
                messages.error(request, message)
            return redirect('upload_book') 
        
        uploaded_file = UploadedFiles.objects.create(
            user=request.user,
            title=title,
            description=description,
            visibility=visibility,
            cost=cost,
            year_published=year_published,
            file=file,
            is_pdf=is_pdf
        )
        uploaded_file.save()
        return redirect('uploaded_books')
    
    return render(request, 'upload.html')


def has_uploaded_books(user):
    return UploadedFiles.objects.filter(user=user).exists()

@login_required
def uploaded_books(request):
    if not has_uploaded_books(request.user):
        return render(request, 'bookpopup.html')
    uploaded_files = UploadedFiles.objects.filter(user=request.user)
    if uploaded_files.exists():
        return render(request, 'uploaded_books.html', {'uploaded_files': uploaded_files})
    else:
        return redirect('upload_book')
   
def fetch_data(request):
    # Create a SQLAlchemy engine for the default SQLite database
    engine = create_engine('sqlite:///C:/Users/manoj mishra/OneDrive/Desktop/Markytics_task/Social_book/social_book/db.sqlite3')

    # Execute a SQL query
    query = text("SELECT id,is_staff,full_name,email,city,state FROM Login_Register_customuser")
    conn = engine.connect()
    result = conn.execute(query)

    # Process the query result
    data = [row for row in result]

    # Print the fetched data
    for row in data:
        print(row)

    # Return a response
    return render(request, 'data.html', {'data': data})

@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_uploaded_files(request):
    user = request.user
    uploaded_files = UploadedFiles.objects.filter(user=user)
    serializer = UploadedFilesSerializer(uploaded_files, many=True)
    return Response(serializer.data)