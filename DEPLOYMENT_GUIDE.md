# 🚀 Django Job Portal - PythonAnywhere Deployment Guide

## Quick Deployment Steps

### 1. Prepare Your Repository
```bash
# Add all files to git
git add .

# Commit changes
git commit -m "Initial commit: Django Job Portal with dark theme"

# Push to GitHub
git push origin main
```

### 2. PythonAnywhere Setup

#### Create Account
- Go to [pythonanywhere.com](https://www.pythonanywhere.com)
- Sign up for free account
- Verify email

#### Create Web App
1. Go to "Web" tab
2. Click "Add a new web app"
3. Choose "Manual configuration"
4. Select Python 3.10
5. Choose "Django" framework

#### Clone Repository
```bash
# In PythonAnywhere Bash console
cd /home/yourusername/
git clone https://github.com/yourusername/your-repo-name.git jobportal
cd jobportal
```

### 3. Install Dependencies
```bash
pip3.10 install --user Django==5.2.6 PyPDF2==3.0.1
```

### 4. Configure Settings
Update `jobportal/settings.py` with your PythonAnywhere details:

```python
# Replace 'yourusername' with your actual PythonAnywhere username
ALLOWED_HOSTS = ['yourusername.pythonanywhere.com']

CSRF_TRUSTED_ORIGINS = ['https://yourusername.pythonanywhere.com']

STATIC_ROOT = '/home/yourusername/jobportal/static'
MEDIA_ROOT = '/home/yourusername/jobportal/media'
```

### 5. Database Setup
```bash
python3.10 manage.py migrate
python3.10 manage.py createsuperuser
python3.10 manage.py collectstatic --noinput
```

### 6. Configure Web App
In PythonAnywhere Web tab:

**Source code**: `/home/yourusername/jobportal/`
**Working directory**: `/home/yourusername/jobportal/`

**WSGI Configuration**:
```python
import os
import sys

path = '/home/yourusername/jobportal'
if path not in sys.path:
    sys.path.append(path)

os.environ['DJANGO_SETTINGS_MODULE'] = 'jobportal.settings'

from django.core.wsgi import get_wsgi_application
application = get_wsgi_application()
```

**Static Files**:
- URL: `/static/`
- Directory: `/home/yourusername/jobportal/static/`

**Media Files**:
- URL: `/media/`
- Directory: `/home/yourusername/jobportal/media/`

### 7. Reload and Test
1. Click "Reload" in Web tab
2. Visit `https://yourusername.pythonanywhere.com`
3. Test all functionality

## 🎯 Features Included

✅ **Dark Theme UI** - Modern, professional design  
✅ **User Authentication** - Signup/Login for recruiters and job seekers  
✅ **Job Management** - Post, edit, and manage jobs  
✅ **Job Applications** - Apply with resume and cover letter  
✅ **AI-Lite Matching** - Skill-based job recommendations  
✅ **Bookmarking** - Save favorite jobs  
✅ **Admin Panel** - Manage jobs and applications  
✅ **Responsive Design** - Works on all devices  

## 🔧 Troubleshooting

### Common Issues:
1. **500 Error**: Check error log in Web tab
2. **Static files not loading**: Run `collectstatic` and check mappings
3. **Database errors**: Run `migrate` command
4. **CSRF errors**: Update `CSRF_TRUSTED_ORIGINS`

### Support:
- Check PythonAnywhere error logs
- Verify all file paths use correct username
- Ensure all dependencies are installed

## 📱 Your Live Site
Once deployed, your job portal will be available at:
`https://yourusername.pythonanywhere.com`

**Admin Access**: `/admin/` (use superuser credentials)

---

**Happy Deploying! 🎉**
