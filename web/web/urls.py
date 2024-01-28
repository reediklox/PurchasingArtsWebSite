"""
URL configuration for web project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
import main.views as main_views
from django.conf import settings
from django.conf.urls.static import static as st
from django.contrib.auth.views import LogoutView

"""
get all posts on general page - ''
get only one post - '/{id}'
get profile - '/{login}'
search paints - '/search'; when start searching - '/search/{title | author_login | price}'
get ordered by popularity - '/popular'
search by category choose - '/category/{category}'
get marks - '/{login}/marks'
get mark - '/{login}/marks/{id}'
get history - '/{login}/history'
get order cart - '/{login}/cart'
"""

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', main_views.general, name='home'),
    path('like/<int:post_id>/', main_views.like_post, name='like_post'),
    path('<int:post_id>/', main_views.post, name='post'),
    path('<int:post_id>/add', main_views.addComment, name='addCommnet'),
    path('popular/', main_views.popular, name='pop'),
    path('registration/', main_views.registration, name='reg'),
    path('login/', main_views.user_login, name='login'),
    path('logout/', main_views.user_logout, name='logout'),
    path('profile/', main_views.profile, name='profile'),
    path('profile/add/', main_views.addPost, name='add'),
    path('marks/', main_views.marks, name='marks'),
    path('categories/<str:post_category>/', main_views.category, name='category'),
    path('profile/change/', main_views.imgChange, name='imgChange'),
    path('history/', main_views.history, name='history'),
    path('buy/<int:post_id>/', main_views.buy, name='buy'),
]

urlpatterns += st(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)