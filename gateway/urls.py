from django.urls import path

from . import views

urlpatterns = [
    path('', views.login_view, name='login'),
    path('verificar/', views.verify_view, name='verify'),
    path('redirigiendo/', views.redirecting_view, name='redirecting'),
    path('streamverse-demo/', views.streamverse_demo_view, name='streamverse_demo'),
]
