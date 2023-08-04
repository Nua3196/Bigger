from django.urls import path, include
from .views import NoticesAPI, NoticeAPI, UpdateNoticesAPI

urlpatterns = [
    path("notices/", NoticesAPI.as_view()),
    path("notice/<int:_id>/", NoticeAPI.as_view()),
    path("update/", UpdateNoticesAPI),
]