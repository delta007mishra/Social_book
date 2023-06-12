from django.contrib import admin
from django.urls import path
from django.conf import settings
from django.conf.urls.static import static
from .import views


urlpatterns = [
    path('', views.login, name='login'),
    path('login/', views.login, name='login'),
    path('logout/', views.logout, name="logout"),
    path('passreset/', views.forgotpassword, name="passreset"),
    path('passresetdone/', views.passresetdone, name="passresetdone"),
    path('passresetmsg/', views.passresetmsg, name="passresetmsg"),
    path('passresetconfirm//<uidb64>/<token>/', views.passresetconfirm, name="passresetconfirm"),
    path('register/', views.register, name='register'),
    path('profile/', views.profile, name='profile'),
    path('imageupload/', views.imageupload, name='imageupload'),
    path('index/', views.index, name='index'),
    path('authorseller/', views.authorseller, name='authorseller'),
    path('upload_book/', views.upload_book, name='upload_book'),
    path('uploaded_books/', views.uploaded_books, name='uploaded_books'),
    path('fetch_data/', views.fetch_data, name='fetch_data'),
    path('api/files/', views.get_uploaded_files, name='get_uploaded_files'),
    

]

urlpatterns = urlpatterns + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)