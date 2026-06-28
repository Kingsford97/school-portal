from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Sum, Count, Avg
from django.utils import timezone
from django.conf import settings
from django.http import JsonResponse
from paystackapi.paystack import Paystack
import json
import uuid
from .models import Student, StudentFee, Attendance, StudentAcademicRecord, Announcement, Subject, ExamResult, \
    PaymentTransaction

# Initialize Paystack
paystack_api = Paystack(secret_key=settings.PAYSTACK_SECRET_KEY)


# ============================================
# STUDENT LOGIN
# ============================================
def student_login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)

        if user is not None:
            try:
                student = Student.objects.get(user=user)
                login(request, user)
                messages.success(request, f'Welcome back, {student.first_name}!')
                return redirect('students:dashboard')
            except Student.DoesNotExist:
                messages.error(request, 'You are not registered as a student.')
        else:
            messages.error(request, 'Invalid username or password.')

    return render(request, 'students/login.html')


# ============================================
# STUDENT LOGOUT
# ============================================
def student_logout(request):
    logout(request)
    messages.success(request, 'You have been logged out.')
    return redirect('students:login')


# ============================================
# STUDENT DASHBOARD
# ============================================
@login_required
def student_dashboard(request):
    try:
        student = Student.objects.get(user=request.user)

        # Fee Balance
        total_fees = StudentFee.objects.filter(student=student).aggregate(Sum('amount'))['amount__sum'] or 0
        total_paid = StudentFee.objects.filter(student=student).aggregate(Sum('paid_amount'))['paid_amount__sum'] or 0
        fee_balance = total_fees - total_paid

        # Attendance
        attendance_count = Attendance.objects.filter(student=student).count()
        present_count = Attendance.objects.filter(student=student, status='present').count()

        # Grades
        grade_records = StudentAcademicRecord.objects.filter(student=student)
        total_subjects = grade_records.count()
        average_score = grade_records.aggregate(Avg('total_score'))['total_score__avg'] or 0

        # Announcements
        announcements = Announcement.objects.filter(is_published=True).order_by('-published_date')[:5]

        # Subjects
        subjects = Subject.objects.all()[:10]

        context = {
            'student': student,
            'fee_balance': fee_balance,
            'attendance_count': attendance_count,
            'present_count': present_count,
            'total_subjects': total_subjects,
            'average_score': average_score,
            'announcements': announcements,
            'subjects': subjects,
        }
        return render(request, 'students/dashboard.html', context)
    except Student.DoesNotExist:
        return render(request, 'students/login.html')


# ============================================
# STUDENT PROFILE
# ============================================
@login_required
def student_profile(request):
    try:
        student = Student.objects.get(user=request.user)
        context = {'student': student}
        return render(request, 'students/profile.html', context)
    except Student.DoesNotExist:
        return redirect('students:login')


# ============================================
# EDIT PROFILE
# ============================================
@login_required
def edit_profile(request):
    try:student = Student.objects.get(user=request.user)
    except Student.DoesNotExist:
        messages.error(request, 'Student profile not found.')
        return redirect('students:login')

    if request.method == 'POST':
        student.first_name = request.POST.get('first_name')
        student.last_name = request.POST.get('last_name')
        student.email = request.POST.get('email')
        student.phone_number = request.POST.get('phone_number')
        student.address = request.POST.get('address')
        student.guardian_name = request.POST.get('guardian_name')
        student.guardian_phone = request.POST.get('guardian_phone')

        if request.FILES.get('profile_picture'):
            student.profile_picture = request.FILES['profile_picture']

        student.save()
        messages.success(request, 'Profile updated successfully!')
        return redirect('students:profile')

    context = {'student': student}
    return render(request, 'students/edit_profile.html', context)


# ============================================
# STUDENT GRADES
# ============================================
@login_required
def student_grades(request):
    try:
        student = Student.objects.get(user=request.user)
        exam_results = ExamResult.objects.filter(student=student).select_related('exam', 'exam__subject')
        context = {
            'student': student,
            'exam_results': exam_results,
        }
        return render(request, 'students/grades.html', context)
    except Student.DoesNotExist:
        return redirect('students:login')


# ============================================
# STUDENT ATTENDANCE
# ============================================
@login_required
def student_attendance(request):
    try:
        student = Student.objects.get(user=request.user)
        context = {'student': student}
        return render(request, 'students/attendance.html', context)
    except Student.DoesNotExist:
        return redirect('students:login')


# ============================================
# STUDENT FEES
# ============================================
@login_required
def student_fees(request):
    try:
        student = Student.objects.get(user=request.user)
        context = {'student': student}
        return render(request, 'students/fees.html', context)
    except Student.DoesNotExist:
        return redirect('students:login')


# ============================================
# PAY FEES (PAYSTACK)
# ============================================
@login_required
def pay_fees(request):
    student = get_object_or_404(Student, user=request.user)

    if request.method == 'POST':
        amount = request.POST.get('amount')

        if not amount or float(amount) <= 0:
            messages.error(request, 'Please enter a valid amount.')
            return redirect('students:pay_fees')

        amount_kobo = int(float(amount) * 100)
        reference = f"PAY-{uuid.uuid4().hex[:10].upper()}"

        transaction = PaymentTransaction.objects.create(
            student=student,
            reference=reference,
            amount=amount,
            status='pending'
        )

        response = paystack_api.transaction.initialize(
            amount=amount_kobo,
            email=student.email,
            reference=reference,
            callback_url=settings.PAYSTACK_CALLBACK_URL
        )

        if response['status']:
            return redirect(response['data']['authorization_url'])
        else:
            messages.error(request, 'Payment initialization failed. Please try again.')
            return redirect('students:pay_fees')

    fees = StudentFee.objects.filter(student=student)
    context = {
        'student': student,
        'fees': fees,
    }
    return render(request, 'students/pay_fees.html', context)


# ============================================
# PAYMENT CALLBACK
# ============================================
@login_required
def payment_callback(request):
    reference = request.GET.get('reference')
    if not reference:
        messages.error(request, 'Invalid payment reference.')
        return redirect('students:dashboard')

    response = paystack_api.transaction.verify(reference)

    if response['status']:
        data = response['data']
        transaction = get_object_or_404(PaymentTransaction, reference=reference)

        if data['status'] == 'success':
            transaction.status = 'success'
            transaction.paid_date = timezone.now()
            transaction.payment_method = data['channel']
            transaction.response_data = data
            transaction.save()

            messages.success(request, f'Payment of GHS {transaction.amount} successful!')
        else:
            transaction.status = 'failed'
            transaction.response_data = data
            transaction.save()
            messages.error(request, 'Payment verification failed.')
    else:
        messages.error(request, 'Could not verify payment.')

    return redirect('students:dashboard')
