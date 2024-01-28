from django.contrib import admin
from .models import Users, Posts, Comments, UsersRights

admin.site.register(Users)
admin.site.register(Posts)
admin.site.register(Comments)
admin.site.register(UsersRights)