from django.urls import path

from . import views

app_name = 'permits'
urlpatterns = [
    path('',views.index,name='index'),
    path('log-in',views.user_login,name='user_login'),
    path('log-out',views.user_logout,name='user_logout'),
    path('register',views.register,name='register'),
    path('apply/sfha',views.sfha,name='sfha'),
    path('apply/grading',views.grading,name='grading'),
    path('apply/franchise',views.franchise,name='franchise'),
    path('success',views.success,name='success'),
    path('my-applications',views.my_applications,name='my_applications'),
    path('my-applications/<int:pk>',views.my_app_detail,name='my_app_detail'),
    path('review',views.review,name='review'),
    path('review/<int:pk>',views.review_detail,name='review_detail'),
    path('review/download/<folder>/<filename>',views.download,name='download'),
    path('payment',views.make_payment,name='payment'),
    ]
