from django.db import models
from django.contrib.auth.models import User


class Student(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    STATUS_CHOICES = [
        ('active', 'Active'),
        ('inactive', 'Inactive'),
        ('graduated', 'Graduated'),
        ('suspended', 'Suspended'),
        ('expelled', 'Expelled')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    student_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    student_class = models.CharField(max_length=50, blank=True, null=True)
    admission_date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='active')
    guardian_name = models.CharField(max_length=100)
    guardian_phone = models.CharField(max_length=15)
    profile_picture = models.ImageField(upload_to='student_pics/', blank=True, null=True)
    is_verified = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.student_id})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class Teacher(models.Model):
    GENDER_CHOICES = [('M', 'Male'), ('F', 'Female'), ('O', 'Other')]
    EMPLOYMENT_CHOICES = [
        ('permanent', 'Permanent'),
        ('contract', 'Contract'),
        ('part_time', 'Part Time'),
        ('intern', 'Intern')
    ]

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    teacher_id = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    date_of_birth = models.DateField()
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES)
    phone_number = models.CharField(max_length=15)
    email = models.EmailField()
    address = models.TextField()
    qualification = models.CharField(max_length=200)
    specialization = models.CharField(max_length=100)
    years_of_experience = models.IntegerField(default=0)
    joining_date = models.DateField(auto_now_add=True)
    employment_status = models.CharField(max_length=20, choices=EMPLOYMENT_CHOICES)
    profile_picture = models.ImageField(upload_to='teacher_pics/', blank=True, null=True)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.first_name} {self.last_name} ({self.teacher_id})"

    def full_name(self):
        return f"{self.first_name} {self.last_name}"


class StaffAttendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('on_leave', 'On Leave')
    ]

    staff = models.OneToOneField(User, on_delete=models.CASCADE, related_name='staff_attendance')
    date = models.DateField(auto_now_add=True)
    check_in = models.TimeField()
    check_out = models.TimeField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES)
    hours_worked = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    note = models.TextField(blank=True, null=True)

class Attendance(models.Model):
    STATUS_CHOICES = [
        ('present', 'Present'),
        ('absent', 'Absent'),
        ('late', 'Late'),
        ('excused', 'Excused')
    ]

    student = models.OneToOneField(Student, on_delete=models.CASCADE, related_name='attendance')
    class_name = models.CharField(max_length=50)
    date = models.DateField(auto_now_add=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES)
    time_in = models.TimeField(blank=True, null=True)
    time_out = models.TimeField(blank=True, null=True)
    note = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.student} - {self.date} - {self.status}"

class LeaveRequest(models.Model):
    LEAVE_TYPES = [
        ('annual', 'Annual Leave'),
        ('sick', 'Sick Leave'),
        ('maternity', 'Maternity Leave'),
        ('paternity', 'Paternity Leave'),
        ('study', 'Study Leave'),
        ('other', 'Other')
    ]
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('approved', 'Approved'),
        ('rejected', 'Rejected')
    ]

    staff = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='leave_requests')
    leave_type = models.CharField(max_length=20, choices=LEAVE_TYPES)
    start_date = models.DateField()
    end_date = models.DateField()
    reason = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    approved_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True,
                                    related_name='approved_leaves')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.staff} - {self.leave_type} - {self.status}"

    def __str__(self):
        return f"{self.staff} - {self.date} - {self.status}"



class Department(models.Model):
    name = models.CharField(max_length=100, unique=True)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    head_of_department = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                           related_name='departments_headed')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class Subject(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20, unique=True)
    description = models.TextField(blank=True, null=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='subjects')
    teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                related_name='subjects_taught')
    credits = models.IntegerField(default=3)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"


class Class(models.Model):
    name = models.CharField(max_length=50)
    code = models.CharField(max_length=20, unique=True)
    department = models.ForeignKey(Department, on_delete=models.CASCADE, related_name='classes')
    class_teacher = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, blank=True,
                                      related_name='classes_taught')
    academic_year = models.CharField(max_length=20)
    capacity = models.IntegerField(default=30)
    current_students = models.IntegerField(default=0)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} ({self.code})"

class StudentAcademicRecord(models.Model):
    TERM_CHOICES = [
        ('first', 'First Term'),
        ('second', 'Second Term'),
        ('third', 'Third Term')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='academic_records')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='academic_records')
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='academic_records')
    academic_year = models.CharField(max_length=20)
    term = models.CharField(max_length=20, choices=TERM_CHOICES)
    assignment_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    test_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    exam_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    total_score = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=2, blank=True, null=True)
    teacher_remarks = models.TextField(blank=True, null=True)

    def calculate_total(self):
        self.total_score = self.assignment_score + self.test_score + self.exam_score
        self.save()
        return self.total_score

    def calculate_grade(self):
        total = self.total_score
        if total >= 80:
            self.grade = 'A'
        elif total >= 70:
            self.grade = 'B'
        elif total >= 60:
            self.grade = 'C'
        elif total >= 50:
            self.grade = 'D'
        else:
            self.grade = 'F'
        self.save()
        return self.grade

    def __str__(self):
        return f"{self.student} - {self.subject} - {self.term} - {self.grade}"

    class Meta:
        unique_together = ('student', 'subject', 'academic_year', 'term')


class Timetable(models.Model):
    DAYS = [
        ('monday', 'Monday'),
        ('tuesday', 'Tuesday'),
        ('wednesday', 'Wednesday'),
        ('thursday', 'Thursday'),
        ('friday', 'Friday'),
        ('saturday', 'Saturday'),
        ('sunday', 'Sunday')
    ]

    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='timetables')
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='timetables')
    teacher = models.ForeignKey(Teacher, on_delete=models.CASCADE, related_name='teacher_timetables')
    day = models.CharField(max_length=20, choices=DAYS)
    start_time = models.TimeField()
    end_time = models.TimeField()
    room = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.class_name} - {self.subject} - {self.day} ({self.start_time})"


class FeeStructure(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    academic_year = models.CharField(max_length=20)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - GHS {self.amount}"


class StudentFee(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('partial', 'Partial'),
        ('paid', 'Paid'),
        ('overdue', 'Overdue')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_fees')
    fee_structure = models.ForeignKey(FeeStructure, on_delete=models.CASCADE, related_name='student_fees')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    due_date = models.DateField()
    paid_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.student} - {self.fee_structure} - {self.status}"


class Payment(models.Model):
    PAYMENT_METHODS = [
        ('cash', 'Cash'),
        ('bank_transfer', 'Bank Transfer'),
        ('mobile_money', 'Mobile Money'),
        ('card', 'Card'),
        ('other', 'Other')
    ]

    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_payments')
    fee = models.ForeignKey(StudentFee, on_delete=models.CASCADE, related_name='student_payments')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHODS)
    reference = models.CharField(max_length=100, unique=True)
    date = models.DateTimeField(auto_now_add=True)
    receipt_number = models.CharField(max_length=50, unique=True)
    notes = models.TextField(blank=True, null=True)
    processed_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='processed_payments')
    def __str__(self):
        return f"{self.student} - GHS {self.amount} - {self.date}"

class PaymentTransaction(models.Model):
        STATUS_CHOICES = [
            ('pending', 'Pending'),
            ('success', 'Success'),
            ('failed', 'Failed'),
            ('cancelled', 'Cancelled')
        ]

        student = models.ForeignKey('Student', on_delete=models.CASCADE, related_name='transactions')
        reference = models.CharField(max_length=100, unique=True)
        amount = models.DecimalField(max_digits=10, decimal_places=2)
        status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
        payment_method = models.CharField(max_length=50, blank=True, null=True)
        transaction_date = models.DateTimeField(auto_now_add=True)
        paid_date = models.DateTimeField(blank=True, null=True)
        response_data = models.JSONField(blank=True, null=True)

        def __str__(self):
            return f"{self.student} - GHS {self.amount} - {self.status}"

class Expense(models.Model):
    CATEGORIES = [
        ('salary', 'Salary'),
        ('utilities', 'Utilities'),
        ('maintenance', 'Maintenance'),
        ('supplies', 'Supplies'),
        ('equipment', 'Equipment'),
        ('transport', 'Transport'),
        ('other', 'Other')
    ]

    description = models.CharField(max_length=200)
    category = models.CharField(max_length=20, choices=CATEGORIES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    receipt = models.FileField(upload_to='expenses/', blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    created_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, related_name='created_expenses')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.category} - GHS {self.amount} ({self.date})"


class Book(models.Model):
    title = models.CharField(max_length=200)
    author = models.CharField(max_length=100)
    isbn = models.CharField(max_length=20, unique=True)
    publisher = models.CharField(max_length=100)
    publication_year = models.IntegerField()
    edition = models.CharField(max_length=50, blank=True, null=True)
    category = models.CharField(max_length=100)
    quantity = models.IntegerField(default=1)
    available_quantity = models.IntegerField(default=1)
    location = models.CharField(max_length=50, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    cover_image = models.ImageField(upload_to='book_covers/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.title} by {self.author}"


class BorrowRecord(models.Model):
    STATUS_CHOICES = [
        ('borrowed', 'Borrowed'),
        ('returned', 'Returned'),
        ('overdue', 'Overdue'),
        ('lost', 'Lost')
    ]
    BORROWER_TYPES = [
        ('student', 'Student'),
        ('teacher', 'Teacher')
    ]

    book = models.ForeignKey(Book, on_delete=models.CASCADE, related_name='created_expenses')
    borrower_type = models.CharField(max_length=20, choices=BORROWER_TYPES)
    borrower_id = models.IntegerField()
    borrow_date = models.DateTimeField(auto_now_add=True)
    due_date = models.DateField()
    return_date = models.DateField(blank=True, null=True)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='borrowed')
    fine_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return f"{self.book} - {self.borrower_type} - {self.status}"


class Exam(models.Model):
    EXAM_TYPES = [
        ('mid_term', 'Mid Term'),
        ('end_term', 'End Term'),
        ('final', 'Final'),
        ('quiz', 'Quiz'),
        ('mock', 'Mock')
    ]

    name = models.CharField(max_length=100)
    exam_type = models.CharField(max_length=20, choices=EXAM_TYPES)
    subject = models.ForeignKey(Subject, on_delete=models.CASCADE, related_name='exams')
    class_name = models.ForeignKey(Class, on_delete=models.CASCADE, related_name='exams')
    date = models.DateField()
    start_time = models.TimeField()
    duration = models.IntegerField(help_text="Duration in minutes")
    total_marks = models.IntegerField()
    passing_marks = models.IntegerField()
    venue = models.CharField(max_length=100)
    invigilator = models.ForeignKey(Teacher, on_delete=models.SET_NULL, null=True, related_name='invigilated_exams')
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject} ({self.date})"


class ExamResult(models.Model):
    exam = models.ForeignKey(Exam, on_delete=models.CASCADE, related_name='results')
    student = models.ForeignKey(Student, on_delete=models.CASCADE, related_name='student_exam_results')
    marks_obtained = models.DecimalField(max_digits=5, decimal_places=2)
    percentage = models.DecimalField(max_digits=5, decimal_places=2, default=0)
    grade = models.CharField(max_length=2, blank=True)
    is_passed = models. BooleanField(default=False)
    remarks = models.TextField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.student} - {self.exam} - {self.grade}"


class Announcement(models.Model):
    PRIORITY_CHOICES = [
        ('low', 'Low'),
        ('medium', 'Medium'),
        ('high', 'High'),
        ('urgent', 'Urgent')
    ]

    title = models.CharField(max_length=200)
    content = models.TextField()
    priority = models.CharField(max_length=20, choices=PRIORITY_CHOICES, default='medium')
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='announcements')
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    published_date = models.DateTimeField(blank=True, null=True)
    expiry_date = models.DateTimeField(blank=True, null=True)
    category = models.CharField(max_length=50, blank=True, null=True)

    def __str__(self):
        return self.title


class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    date = models.DateTimeField()
    venue = models.CharField(max_length=200)
    organizer = models.CharField(max_length=100)
    contact_email = models.EmailField(blank=True, null=True)
    contact_phone = models.CharField(max_length=15, blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    is_active = models.BooleanField(default=True)

    def __str__(self):
        return f"{self.title} - {self.date}"


class Notification(models.Model):
    recipient = models.ForeignKey(User, on_delete=models.CASCADE, related_name='student_notifications')
    title = models.CharField(max_length=200)
    message = models.TextField()
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    link = models.CharField(max_length=200, blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.recipient}"


class Report(models.Model):
    REPORT_TYPES = [
        ('student', 'Student Report'),
        ('financial', 'Financial Report'),
        ('attendance', 'Attendance Report'),
        ('academic', 'Academic Report'),
        ('staff', 'Staff Report'),
        ('library', 'Library Report')
    ]

    report_type = models.CharField(max_length=20, choices=REPORT_TYPES)
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, null=True)
    generated_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='generated_reports')
    generated_date = models.DateTimeField(auto_now_add=True)
    start_date = models.DateField()
    end_date = models.DateField()
    data = models.JSONField(blank=True, null=True)
    file = models.FileField(upload_to='reports/', blank=True, null=True)

    def __str__(self):
        return f"{self.title} - {self.generated_date}"

