from django.contrib.auth.decorators import login_required
from django.shortcuts import render

def home(request):
    return render(request, 'home.html')

@login_required
def recruiter_dashboard(request):
    return render(request, 'dashboard/recruiter_dashboard.html')

@login_required
def jobseeker_dashboard(request):
    return render(request, 'dashboard/jobseeker_dashboard.html')