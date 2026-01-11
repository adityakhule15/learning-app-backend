# Learning App Backend API

## Quick Start

### 1. Clone & Setup
```bash
# Clone repository
git clone https://github.com/yourusername/learning-app-backend.git
cd learning-app-backend

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate

# Install dependencies
pip install -r requirements.txt
```

### 2. Database Setup
```bash
# Run migrations
python manage.py migrate

# Create admin user
python manage.py createsuperuser
# Username: admin
# Email: admin@example.com
# Password: admin123

# Seed initial data
python seed_data.py
```

### 3. Run Server
```bash
python manage.py runserver
```
**Server runs at:** http://localhost:8000

## API Endpoints

### Authentication
- `POST /api/auth/request-otp/` - Request OTP
- `POST /api/auth/verify-otp/` - Verify OTP & get tokens
- `POST /api/auth/token/refresh/` - Refresh access token
- `GET /api/auth/profile/` - Get user profile

### Lessons (Public)
- `GET /api/lessons/lessons/` - Get all lessons
- `GET /api/lessons/lessons/{id}/` - Get single lesson
- `GET /api/lessons/lessons/{id}/steps/` - Get lesson steps

### Progress Tracking (Protected)
- `POST /api/progress/progress/update_progress/` - Update progress
- `GET /api/progress/progress/by_lesson/` - Get progress by lesson
- `GET /api/progress/progress/overview/` - Get progress overview
- `GET /api/progress/progress/` - Get all user progress

### Admin APIs
- `POST /api/admin/admin/lessons/` - Create lesson
- `GET /api/admin/admin/stats/` - Get statistics

## Quick API Testing

### 1. Request OTP
```bash
curl -X POST http://localhost:8000/api/auth/request-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone": "+919999999999"}'
```

### 2. Verify OTP (Test OTP: 123456)
```bash
curl -X POST http://localhost:8000/api/auth/verify-otp/ \
  -H "Content-Type: application/json" \
  -d '{"phone": "+919999999999", "otp": "123456"}'
```

### 3. Get Lessons (Public)
```bash
curl http://localhost:8000/api/lessons/lessons/
```

### 4. Get Filtered Lessons
```bash
curl "http://localhost:8000/api/lessons/lessons/?category=whatsapp&language=en"
```

## Features Implemented

✅ **OTP Authentication** with rate limiting (5 attempts/hour)  
✅ **JWT Token-based authentication**  
✅ **Multi-language lessons** (English, Hindi, Marathi)  
✅ **Progress tracking** with resume capability  
✅ **Admin panel** at /admin  
✅ **Public APIs** for lessons browsing  
✅ **SQLite database** (easy setup)  
✅ **CORS enabled** for mobile apps  
✅ **Complete seed data** with 2 lessons, 5 steps each  

## Database Models

### 1. CustomUser
- `phone` (Primary Key) - User's phone number
- `name` - User's name
- `email` - User's email
- `date_joined` - Registration date

### 2. OTP
- `phone` - Phone number
- `otp` - 6-digit OTP code
- `expires_at` - Expiry time (2 minutes)
- `is_used` - Whether OTP is used

### 3. Lesson
- `title` - Lesson title
- `category` - whatsapp/upi/basic
- `language` - en/hi/mr
- `order` - Display order

### 4. LessonStep
- `lesson` - Foreign key to Lesson
- `step_number` - Step order
- `title` - Step title
- `instruction_text` - Step instructions

### 5. UserProgress
- `user` - Foreign key to User
- `lesson` - Foreign key to Lesson
- `last_step_completed` - Last completed step
- `completed` - Whether lesson completed

## Sample Data Created

After running `seed_data.py`:

### 1. WhatsApp Basics (English)
- 5 steps from installation to voice messages

### 2. UPI Payments (Hindi)
- 5 steps from app download to payment history

## Testing with Python

```python
import requests

# 1. Request OTP
response = requests.post(
    'http://localhost:8000/api/auth/request-otp/',
    json={'phone': '+919999999999'}
)
print('OTP:', response.json()['otp'])  # Will be 123456

# 2. Verify OTP
response = requests.post(
    'http://localhost:8000/api/auth/verify-otp/',
    json={'phone': '+919999999999', 'otp': '123456'}
)
tokens = response.json()['token']
access_token = tokens['access']

# 3. Get lessons with token
headers = {'Authorization': f'Bearer {access_token}'}
response = requests.get(
    'http://localhost:8000/api/lessons/lessons/',
    headers=headers
)
print('Lessons:', response.json())

# 4. Update progress
progress_data = {
    'lesson_id': 1,
    'last_step_completed': 3,
    'time_spent': 120
}
response = requests.post(
    'http://localhost:8000/api/progress/progress/update_progress/',
    headers=headers,
    json=progress_data
)
print('Progress:', response.json())
```

## Admin Access

1. Access Django Admin: http://localhost:8000/admin
2. Login with superuser credentials
3. Manage:
   - Users
   - Lessons
   - Steps
   - Progress records
   - OTP records

## Troubleshooting

### 1. Port 8000 already in use
```bash
# Kill existing process
pkill -f runserver
# Or use different port
python manage.py runserver 8001
```

### 2. Database errors
```bash
# Delete and recreate database
rm db.sqlite3
python manage.py migrate
python seed_data.py
```

### 3. Module import errors
```bash
# Ensure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate
pip install -r requirements.txt
```

### 4. OTP not working
- Test OTP is always "123456"
- Check rate limit (5 requests/hour)
- OTP expires in 2 minutes

## Deployment to Production

### 1. Update settings.py
```python
DEBUG = False
ALLOWED_HOSTS = ['your-domain.com']
# Use PostgreSQL in production
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': 'mydb',
        'USER': 'myuser',
        'PASSWORD': 'mypassword',
        'HOST': 'localhost',
        'PORT': '5432',
    }
}
```

### 2. Using Gunicorn
```bash
pip install gunicorn
gunicorn learning_backend.wsgi:application --bind 0.0.0.0:8000
```

### 3. Using Nginx
```nginx
server {
    listen 80;
    server_name api.your-domain.com;

    location / {
        proxy_pass http://localhost:8000;
        proxy_set_header Host $host;
    }
}
```

## Project Structure

```
learning-app-backend/
├── accounts/          # Authentication app
├── lessons/           # Lessons management
├── progress_tracker/  # Progress tracking
├── admin_api/         # Admin APIs
├── learning_backend/  # Project settings
├── requirements.txt   # Python dependencies
├── seed_data.py       # Initial data
├── manage.py          # Django CLI
└── db.sqlite3         # Database
```

## Default Admin Credentials
- **URL**: http://localhost:8000/admin
- **Username**: admin
- **Password**: admin123 (change after first login)

## API Status Check
```bash
# Check if API is running
curl http://localhost:8000/api/lessons/lessons/

# Check admin panel
curl http://localhost:8000/admin/
```

## Ready for Mobile App Integration

Your backend is ready to connect with:
- **Flutter** mobile app
- **React Native** app
- **iOS/Android** applications
- **Web frontend**

## Support

For issues:
1. Check if server is running: `python manage.py runserver`
2. Check database: `python manage.py check`
3. Test endpoints with Postman or curl
4. View logs in terminal

---

**Backend is now ready!** 🎉

Access at: http://localhost:8000  
Admin Panel: http://localhost:8000/admin  
API Base: http://localhost:8000/api/

