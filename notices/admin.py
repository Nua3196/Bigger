from django.contrib import admin

# Register your models here.

#블로그 보고 따라한거
#django admin page에 Noti 모델 등록하는 코드
from .models import Notice, Update

admin.site.register(Notice)
admin.site.register(Update)

