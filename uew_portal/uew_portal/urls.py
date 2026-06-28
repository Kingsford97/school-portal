from django.urls import path
from . import views

app_name = 'students'

urlpatterns = [
    # Student Authentication
    path('login/', views.student_login, name='login'),
    path('logout/', views.student_logout, name='logout'),
    path('dashboard/', views.student_dashboard, name='dashboard'),
    path('grades/', views.student_grades, name='grades'),
    path('attendance/', views.student_attendance, name='attendance'),
    path('fees/', views.student_fees, name='fees'),
    path('profile/', views.student_profile, name='profile'),
    path('edit-profile/', views.edit_profile, name='edit_profile'),  # ← ADD THIS
    path('grades/', views.student_grades, name='grades'),
    path('attendance/', views.student_attendance, name='attendance'),
    path('pay-fees/', views.pay_fees, name='pay_fees'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
    path('payment/callback/', views.payment_callback, name='payment_callback'),
]

