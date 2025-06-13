from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import views as auth_views
from core import views
from django.contrib.auth.decorators import login_required

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('core.urls')),
     path('accounts/login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
 path('', login_required(views.profile_view), name='profile'),  # Home after login shows profile
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('profile/<str:username>/', login_required(views.profile_view), name='profile'),
    path('add_post/', login_required(views.add_post), name='add_post'),
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)