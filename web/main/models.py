from django.db import models
from datetime import datetime
from django.core.validators import MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager

class UserManager(BaseUserManager):
    def create_user(self, login, email, password=None, **extra_fields):
        if not email:
            raise ValueError('Email должен быть указан')
        email = self.normalize_email(email)
        user = self.model(login=login, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user 
    
    def create_superuser(self, login, email=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        email = self.normalize_email(email) if email else 'admin@mail.ru'
        return self.create_user(login, email, password, **extra_fields)

def getTimeNow():
        return datetime.now()

class Users(AbstractUser):
    
    login = models.CharField(max_length=150, primary_key=True)
    password = models.CharField(max_length=150)
    email = models.EmailField()
    email_access = models.BooleanField(default=False, editable=False)
    profile_image = models.ImageField(blank=True, upload_to='media/', default='UnknownLogo.png')  
    
    USERNAME_FIELD = 'login'
    REQUIRED_FIELDS = []
    
    objects = UserManager()
    def __str__(self) -> str:
         return self.login
     
    def clean(self):
        self.email = self.__class__.objects.normalize_email(self.email)


class Posts(models.Model): 
    
    CATEGORIES = [('р', 'Ручная живопись'), ('к', 'Компьютерная живопись')]
    
    post_id = models.AutoField(primary_key=True)
    author_login = models.ForeignKey('Users', on_delete=models.CASCADE)
    post_title = models.CharField(max_length=16)
    post_image = models.ImageField()
    post_date = models.DateTimeField(editable=False, default=getTimeNow)
    img_price = models.IntegerField(validators=[MinValueValidator(limit_value=0, message='Цена не может быть ниже 0')])
    post_likes = models.IntegerField(default=0, editable=False)
    post_category = models.CharField(max_length=1, choices=CATEGORIES, default='р')
    
    def __str__(self) -> str:
         return self.post_title


class Comments(models.Model):
    
    comment_id = models.AutoField(primary_key=True)
    author_login = models.ForeignKey('Users', on_delete=models.CASCADE)
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE, default=0)
    comment_content = models.TextField()
    comment_date = models.DateTimeField(editable=False, default=getTimeNow)
    
    def __str__(self) -> str:
         return f'post({self.post_id}): {self.author_login}'


class UsersRights(models.Model):
    
    author_login = models.ForeignKey('Users', on_delete=models.CASCADE)
    post_id = models.ForeignKey('Posts', on_delete=models.CASCADE)
    right_date = models.DateTimeField(editable=False, default=getTimeNow)
    
    def __str__(self) -> str:
         return f'{self.post_id} - {str(self.right_date).split('+')[0].split('.')[0]}'
    

class Likes(models.Model):
    user = models.ForeignKey(Users, on_delete=models.CASCADE)
    post = models.ForeignKey(Posts, on_delete=models.CASCADE)

    class Meta:
        unique_together = ['user', 'post']
        
class Marks(models.Model):
    likes = models.ForeignKey(Likes, on_delete=models.CASCADE)