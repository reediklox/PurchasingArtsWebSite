from django import forms
from .models import Users, Likes, Posts, Comments
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = Users
        fields = ['login', 'password1', 'password2', 'email']
        
class LikeForm(forms.ModelForm):
    class Meta:
        model = Likes
        fields = ['post']
        
class AddPost(forms.ModelForm):
    class Meta:
        model = Posts
        fields = ['post_title', 'post_category', 'post_image', 'img_price']
        
class AddComment(forms.ModelForm):
    class Meta:
        model = Comments
        fields = ['comment_content']       
    