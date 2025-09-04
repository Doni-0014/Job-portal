from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.db.models import Q
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse

from .models import Job, Application, Bookmark


def job_list(request):
    query = request.GET.get('q', '')
    location = request.GET.get('location', '')
    min_salary = request.GET.get('min_salary')
    max_salary = request.GET.get('max_salary')

    jobs = Job.objects.filter(status='approved')

    if query:
        jobs = jobs.filter(Q(title__icontains=query) | Q(description__icontains=query) | Q(skills__icontains=query))
    if location:
        jobs = jobs.filter(location__icontains=location)
    if min_salary:
        jobs = jobs.filter(max_salary__gte=min_salary)
    if max_salary:
        jobs = jobs.filter(min_salary__lte=max_salary)

    return render(request, 'jobs/job_list.html', {
        'jobs': jobs,
        'query': query,
        'location': location,
        'min_salary': min_salary or '',
        'max_salary': max_salary or '',
    })


def job_detail(request, pk):
    job = get_object_or_404(Job, pk=pk, status='approved')
    is_bookmarked = False
    if request.user.is_authenticated:
        is_bookmarked = Bookmark.objects.filter(user=request.user, job=job).exists()
    return render(request, 'jobs/job_detail.html', {'job': job, 'is_bookmarked': is_bookmarked})


@login_required
def job_create(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')

    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        location = request.POST.get('location')
        min_salary = request.POST.get('min_salary') or None
        max_salary = request.POST.get('max_salary') or None
        skills = request.POST.get('skills', '')
        company_name = request.POST.get('company_name')

        Job.objects.create(
            title=title,
            description=description,
            location=location,
            min_salary=min_salary,
            max_salary=max_salary,
            skills=skills,
            company_name=company_name,
            posted_by=request.user,
            status='pending',
        )
        return redirect('recruiter_dashboard')

    return render(request, 'jobs/job_form.html')


@login_required
def apply_job(request, pk):
    job = get_object_or_404(Job, pk=pk, status='approved')
    if request.user.role != 'jobseeker':
        return redirect('job_detail', pk=pk)

    if request.method == 'POST':
        resume = request.FILES.get('resume')
        cover_letter = request.POST.get('cover_letter', '')

        # Already applied check
        if Application.objects.filter(job=job, applicant=request.user).exists():
            messages.info(request, 'You have already applied for this job.')
            return redirect('job_detail', pk=pk)

        # Validate required fields
        if not resume or not cover_letter.strip():
            messages.error(request, 'Resume and cover letter are required.')
            return redirect('job_detail', pk=pk)

        # Create application
        Application.objects.create(
            job=job,
            applicant=request.user,
            resume=resume,
            cover_letter=cover_letter
        )
        messages.success(request, 'Job applied successfully!')
        return redirect('job_detail', pk=pk)

    return render(request, 'jobs/apply_form.html', {'job': job})


@login_required
def toggle_bookmark(request, pk):
    job = get_object_or_404(Job, pk=pk, status='approved')
    bookmark, created = Bookmark.objects.get_or_create(user=request.user, job=job)
    if not created:
        bookmark.delete()
    return redirect('job_detail', pk=pk)


@login_required
def my_bookmarks(request):
    bookmarks = Bookmark.objects.filter(user=request.user).select_related('job')
    return render(request, 'jobs/bookmarks.html', {'bookmarks': bookmarks})


@login_required
def manage_applications(request):
    if request.user.role != 'recruiter':
        return redirect('job_list')
    apps = Application.objects.filter(job__posted_by=request.user).select_related('job', 'applicant')
    if request.method == 'POST':
        app_id = request.POST.get('application_id')
        new_status = request.POST.get('status')
        app = get_object_or_404(Application, id=app_id, job__posted_by=request.user)
        app.status = new_status
        app.save()
        return redirect('manage_applications')
    return render(request, 'jobs/manage_applications.html', {'applications': apps, 'status_choices': Application.STATUS_CHOICES})


@login_required
def recommendations(request):
    import re
    text = ''
    if request.method == 'POST' and request.FILES.get('resume'):
        from PyPDF2 import PdfReader
        pdf = request.FILES['resume']
        try:
            reader = PdfReader(pdf)
            for page in reader.pages:
                text += page.extract_text() or ''
        except Exception:
            text = ''
    # Fallback: use skills typed in a text box
    if not text:
        text = request.POST.get('skills', '')

    tokens = set([t.lower() for t in re.split(r'[^a-zA-Z0-9+#]+', text) if t])
    jobs = Job.objects.filter(status='approved')
    scored = []
    for job in jobs:
        job_tokens = set([t.strip().lower() for t in (job.skills or '').split(',') if t.strip()])
        overlap = tokens.intersection(job_tokens)
        score = len(overlap)
        if score > 0:
            scored.append((score, job, ', '.join(sorted(overlap))))
    scored.sort(key=lambda x: x[0], reverse=True)
    top = scored[:5]
    return render(request, 'jobs/recommendations.html', {'results': top})
