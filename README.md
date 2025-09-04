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
