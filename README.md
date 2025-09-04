# Job Portal (Django)

An interview-ready job portal showcasing core hiring flows plus a few impressive extras: role-based auth, job posting and applications, search/filters, resume upload, admin approvals, recruiter application tracker, bookmarks, and AI‑lite skill-based recommendations.

## 1) Project Structure

- `jobportal/` (project settings)
  - `settings.py`: apps, DB, templates, static, media, custom `AUTH_USER_MODEL`
  - `urls.py`: routes to accounts, jobs, dashboards, media in dev
  - `views.py`: `home` view
- `accounts/` (auth & roles)
  - `models.py`: `User` extends `AbstractUser` with `role` (recruiter/jobseeker)
  - `forms.py`: Bootstrap-ready login/signup forms
  - `views.py`: signup/login/logout with role-based redirect
  - `urls.py`: `/accounts/login|signup|logout`
- `jobs/` (core domain)
  - `models.py`: `Job`, `Application`, `Bookmark`
  - `views.py`: list/detail/create/apply/bookmark/manage_applications/recommendations
  - `urls.py`: `/jobs/…` endpoints
  - `admin.py`: admin registrations + approve/reject actions
- `templates/`
  - `base.html`: Bootstrap layout/navbar/footer
  - `home.html`: hero with search
  - `login.html`, `signup.html`: styled auth forms
  - `jobs/*.html`: list, detail, post form, apply form, bookmarks, recommendations, manage applications
  - `dashboard/*.html`: recruiter and jobseeker dashboards
- `static/css/styles.css`: small custom CSS

## 2) Key Features

- Recruiter & Job Seeker signup/login (custom user model with `role`)
- Job posting (recruiter)
- Job applications with resume upload (jobseeker)
- Job search and filters (title/skills, location, min/max salary)
- Bookmarks (save/remove jobs)
- Admin approval workflow (jobs default to `pending`; admin can approve/reject)
- Application tracker (recruiter updates application status)
- AI-lite recommendations (PDF resume parse via PyPDF2 or skills text input; Top 5 matches)

## 3) Data Model Summary

- `accounts.User(AbstractUser)`
  - `role`: `recruiter` | `jobseeker`

- `jobs.Job`
  - `title`, `description`, `location`, `min_salary`, `max_salary`
  - `skills` (comma-separated), `company_name`
  - `posted_by` (FK to `User`), `status` (`draft|pending|approved|rejected`)
  - timestamps

- `jobs.Application`
  - `job` (FK), `applicant` (FK), `resume` (FileField), `cover_letter`
  - `status` (`applied|in_review|shortlisted|interview|offer|rejected`)
  - unique per `(job, applicant)`

- `jobs.Bookmark`
  - unique per `(user, job)`

## 4) Views and URLs (high level)

- `jobportal/urls.py`
  - `/` → `home`
  - `/admin/` → Django admin
  - `/accounts/…` → auth
  - `/jobs/…` → jobs module
  - `/recruiter/dashboard/` and `/jobseeker/dashboard/`

- `jobs/urls.py`
  - `/jobs/` → List with filters
  - `/jobs/<id>/` → Detail + apply/bookmark (if jobseeker)
  - `/jobs/create/` → Post a job (recruiter)
  - `/jobs/<id>/apply/` → Apply (jobseeker)
  - `/jobs/<id>/bookmark/` → Toggle bookmark
  - `/jobs/bookmarks/` → My bookmarks
  - `/jobs/applications/manage/` → Recruiter application tracker
  - `/jobs/recommendations/` → AI‑lite recommendations

## 5) Templates / UI

- Bootstrap 5 + Bootstrap Icons (CDN) + minimal custom CSS
- `base.html` navbar shows context-aware links (jobs, recommendations, bookmarks, post job, manage apps)
- `home.html` hero with search inputs
- Forms styled with Bootstrap via form init in `accounts/forms.py` and explicit labels/errors in templates

## 6) Setup & Run

- Requirements: Python 3.13+, MySQL, virtualenv (already provided as `myvenv/`)
- DB settings: `jobportal/settings.py` uses MySQL (`jobportal_db`). Adjust credentials if needed.
- Migrations
  - `python manage.py makemigrations`
  - `python manage.py migrate`
- Create admin user (PowerShell example):
  - Set env + create non-interactive superuser:
    - `DJANGO_SUPERUSER_USERNAME=admin`
    - `DJANGO_SUPERUSER_EMAIL=admin@example.com`
    - `DJANGO_SUPERUSER_PASSWORD=AdminPass123!`
  - `python manage.py createsuperuser --noinput`
- Run server: `python manage.py runserver`
- Admin: `http://127.0.0.1:8000/admin/`

Note: For dev file uploads, media is served via `urlpatterns += static()` while `DEBUG=True`.

## 7) Common Flows

- Post a Job (Recruiter)
  1) Login as recruiter → Navbar → Post Job
  2) Submit → Job created with `status='pending'`
  3) Admin approves in Admin → Jobs → select → Approve selected jobs
  4) Job becomes visible in list/search/detail

- Apply to a Job (Jobseeker)
  1) Login as jobseeker → open a job detail
  2) Upload resume and optional cover letter → Submit
  3) Recruiter can update status in Applications manager

- Search & Filters
  - On `/jobs/`, use search fields for title/skills, location, min/max salary

- AI‑lite Recommendations
  - `/jobs/recommendations/`
  - Upload resume (PDF) or type skills → Top 5 jobs ranked by overlap with `Job.skills`

## 8) Where to Change Things

- Auto-approve jobs for demos: in `jobs/views.py` `job_create` view, change `status='pending'` → `status='approved'`
- Hide features you don’t want: remove links from `base.html` and corresponding routes/templates
- Add validations/forms for job posting: create Django `forms.Form`/`ModelForm` to replace basic POST parsing

## 9) Security & Production Notes

- Replace `SECRET_KEY`, set `DEBUG=False`, configure `ALLOWED_HOSTS`
- Use cloud storage (S3/Cloudinary) for resumes/videos in production
- Add pagination for job list, rate limiting for forms, and CSRF is already enabled
- Consider email verification and password resets via Django auth views

## 10) Nice Next Improvements

- Real-time chat (Django Channels) between recruiter and candidate
- Email job alerts (Celery + Redis schedules)
- Analytics dashboards (Chart.js) for recruiters/candidates
- Company logos and candidate profile with skill progress bars
- Richer matching (spaCy embeddings / keyword weighting)

---
If you want a lighter version for a quick demo/interview, I can disable approval (auto‑approve on post), hide bookmarks/recommendations, and keep only the baseline in a separate branch.
