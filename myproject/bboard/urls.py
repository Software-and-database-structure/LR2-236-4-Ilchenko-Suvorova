from django.urls import path
from .views import index, rubric_bbs, BbCreateView
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('', index, name='index'),
    path('<int:rubric_id>/', rubric_bbs, name='rubric_bbs'),
    path('add/', BbCreateView.as_view(), name='add'),
]