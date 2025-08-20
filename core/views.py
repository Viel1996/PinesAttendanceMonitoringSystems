from django.shortcuts import render, redirect
from django.utils import timezone
from .models import ScanLog, Student
from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth.hashers import check_password
from .supabase_client import supabase

def home(request):
    logs = ScanLog.objects.order_by('-timestamp')[:20]  # last 20 scans

    if request.method == "POST":
        rfid_code = request.POST.get("rfid_code")

        # Check Supabase
        response = supabase.table("students").select("*").eq("rfid", rfid_code).execute()
        data = response.data

        if data:
            student_name = data[0]["name"]
            status = "Success"
        else:
            student_name = None
            status = "Failed"

        # Save scan log in your Django database
        student_obj = Student.objects.filter(rfid=rfid_code).first()
        ScanLog.objects.create(
            student=student_obj,
            rfid_code=rfid_code,
            status=status,
            timestamp=timezone.now()
        )

        return redirect("home")  # refresh page

    return render(request, "home.html", {"logs": logs})

# Attendance sheet
def attendance_sheet(request):
    logs = ScanLog.objects.order_by('-timestamp')
    return render(request, 'attendance_sheet.html', {'logs': logs})

# Dashboard
def dashboard(request):
    total_scans = ScanLog.objects.count()
    success_scans = ScanLog.objects.filter(status='Success').count()
    failed_scans = ScanLog.objects.filter(status='Failed').count()
    return render(request, 'dashboard.html', {
        'total_scans': total_scans,
        'success_scans': success_scans,
        'failed_scans': failed_scans
    })

def settings(request):
    return render(request, "settings.html")
    
def reports(request):
    return render(request, "reports.html")
    
def landing(request):
    return render(request, "landing.html")

def login(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Fetch user from Supabase
        response = supabase.table("users").select("*").eq("username", username).execute()
        print("DEBUG: Supabase response:", response.data)  # Debug

        if response.data and len(response.data) > 0:
            user = response.data[0]

            # Check password
            if check_password(password, user['password']):
                # Role-based redirect
                if user['role'] == 'principal':
                    return redirect('dashboard-2')  # Principal dashboard
                elif user['role'] == 'teacher':
                    return redirect('dashboard')    # Teacher dashboard
                else:
                    messages.error(request, "Invalid role assigned to user.")
            else:
                messages.error(request, "Incorrect password.")
        else:
            messages.error(request, "User not found.")

        return redirect('login')

    return render(request, 'login.html')

def about(request):
    return render(request, "about.html")

def dashboard2(request):
    return render(request, "dashboard-2.html")

