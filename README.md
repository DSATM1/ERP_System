# College ERP System

A comprehensive Enterprise Resource Planning (ERP) system for college management built with Django.

## Features

### Core Modules
- **User Management** - Role-based authentication (Admin, Faculty, Student, Staff)
- **Academic Structure** - Departments, Courses, Subjects management
- **Student Management** - Admission, profiles, academic records
- **Faculty Management** - Faculty profiles and assignments

### Academic Modules
- **Attendance System** - Daily attendance tracking and reports
- **Examination** - Exam schedules, grades, and results
- **Timetable** - Class schedules and room allocation

### Administrative Modules
- **Fee Management** - Fee structures and payment tracking
- **Library** - Book catalog, issues, and returns
- **Hostel** - Room management and allotments
- **Transport** - Bus routes and vehicle management

### Communication
- **Announcements** - College notices and announcements

## Tech Stack

- **Backend**: Django 5.x (Python)
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: Django Templates with Bootstrap 5
- **Authentication**: Django's built-in auth with role-based access

## Installation

### Prerequisites
- Python 3.10+
- pip (Python package manager)

### Setup Steps

1. **Clone/Download the project**
   ```bash
   cd college_erp
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv

   # Windows
   venv\Scripts\activate

   # Linux/Mac
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Run migrations**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

5. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

6. **Run development server**
   ```bash
   python manage.py runserver
   ```

7. **Access the application**
   - Main site: http://127.0.0.1:8000/
   - Admin panel: http://127.0.0.1:8000/admin/

## Project Structure

```
college_erp/
├── config/                 # Django settings
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── apps/
│   ├── core/              # Base models, utilities
│   ├── accounts/          # User management
│   ├── academics/         # Departments, courses, subjects
│   ├── students/          # Student management
│   ├── faculty/           # Faculty management
│   ├── attendance/        # Attendance tracking
│   ├── examination/       # Exams & results
│   ├── timetable/         # Class schedules
│   ├── fees/              # Fee management
│   ├── library/           # Library system
│   ├── hostel/            # Hostel management
│   ├── transport/         # Transport system
│   └── announcements/     # Notices
├── templates/              # HTML templates
├── static/                # CSS, JS, images
└── media/                  # User uploaded files
```

## User Roles

1. **Admin** - Full access to all modules
2. **Faculty** - Manage classes, mark attendance, enter grades
3. **Student** - View academic info, attendance, results
4. **Staff** - Administrative tasks, student management

## Configuration

### Environment Variables

Copy `.env.example` to `.env` and configure:

```
DJANGO_SECRET_KEY=your-secret-key-here
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Database

Default: SQLite (development)

For PostgreSQL:
```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'college_erp',
        'USER': 'your_username',
        'PASSWORD': 'your_password',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

## License

This project is open source and available for educational purposes.

## Contributing

1. Fork the repository
2. Create a feature branch
3. Commit your changes
4. Push to the branch
5. Create a Pull Request
