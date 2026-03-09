# Flask Todo App

A production-ready task management web application built with Flask, featuring user authentication, secure credential management with AWS Secrets Manager, and deployment on AWS Elastic Beanstalk.

![Status](https://img.shields.io/badge/Status-Production%20Ready-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Flask](https://img.shields.io/badge/Flask-2.3-green)
![License](https://img.shields.io/badge/License-MIT-yellow)

## 🌟 Features

- **🔐 User Authentication**: Secure registration, login, and logout with password hashing
- **✅ Todo Management**: Create, view, update, and delete tasks
- **📧 Email Notifications**: Flask-Mail integration for user communications
- **🛡️ Security**: CSRF protection, secure sessions, and AWS Secrets Manager for credentials
- **📱 Responsive Design**: Bootstrap 5 for mobile-friendly UI
- **💾 Database**: MySQL on Amazon RDS with Flask-Migrate for schema management
- **☁️ Cloud-Ready**: Deployed on AWS Elastic Beanstalk with auto-scaling

## 🚀 Quick Start

### Prerequisites

- Python 3.11+
- MySQL 8.0+ or Amazon RDS
- AWS Account (for deployment)
- AWS CLI configured

### Local Development

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/flask-todo-app.git
   cd flask-todo-app
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   
   # Windows
   venv\Scripts\activate
   
   # Mac/Linux
   source venv/bin/activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment variables**
   
   Create a `.env` file in the root directory:
   ```env
   FLASK_ENV=development
   FLASK_APP=application.py
   SECRET_KEY=your-secret-key-here
   
   # Database (for local MySQL)
   RDS_USERNAME=username
   RDS_PASSWORD=your-password
   RDS_HOST=localhost
   RDS_PORT=3306
   RDS_DB_NAME=your-db-name
   
   # Email Configuration
   MAIL_SERVER=smtp.gmail.com
   MAIL_PORT=587
   MAIL_USE_TLS=True
   MAIL_USERNAME=your-email@gmail.com
   MAIL_PASSWORD=your-app-password
   MAIL_DEFAULT_SENDER=your-email@gmail.com
   ```

5. **Initialize database**
   ```bash
   flask db upgrade
   ```

6. **Run the application**
   ```bash
   flask run
   ```

7. **Access the app**
   
   Open your browser and navigate to `http://localhost:5000`

## 🏗️ Project Structure

```
flask-todo-app/
├── application.py          # WSGI entry point
├── config.py               # Configuration classes
├── requirements.txt        # Python dependencies
├── .env                    # Environment variables (not in repo)
├── .gitignore              # Git ignore rules
│
├── app/
│   ├── __init__.py         # Application factory
│   ├── models.py           # SQLAlchemy models (User, Todo)
│   ├── extensions.py       # Flask extensions initialization
│   │
│   ├── auth/
│   │   ├── __init__.py
│   │   └── auth_routes.py  # Authentication routes
│   │
│   ├── home/
│   │   ├── __init__.py
│   │   └── home_routes.py  # Todo CRUD routes
│   │
│   ├── static/
│   │   ├── css/
│   │   ├── js/
│   │   └── images/
│   │
│   └── templates/
│       ├── base.html
│       ├── auth/
│       │   ├── login.html
│       │   └── register.html
│       └── home/
│           └── dashboard.html
│
└── migrations/             # Alembic migrations
    ├── versions/
    ├── env.py
    └── script.py.mako
```
## ☁️ AWS Deployment

### Prerequisites

- AWS CLI configured
- Elastic Beanstalk CLI installed (`pip install awsebcli`)
- RDS instance created
- Secrets Manager secret created

## 🔐 Security

### Best Practices Implemented

- ✅ **Passwords**: Hashed using Werkzeug's `generate_password_hash`
- ✅ **Secrets**: Stored in AWS Secrets Manager, not in code
- ✅ **Sessions**: Secure cookies with HTTPOnly flag
- ✅ **CSRF**: Protected with Flask-WTF
- ✅ **SQL Injection**: Prevented with SQLAlchemy ORM
- ✅ **Environment Variables**: Never committed to Git

### Environment Variables

Never commit `.env` or credentials to Git. The `.gitignore` file excludes:
- `.env`
- `venv/`
- `__pycache__/`
- `*.db`
- `.DS_Store`

## 🧪 Testing

```bash
# Install test dependencies
pip install pytest pytest-cov

# Run tests
pytest

# Run with coverage
pytest --cov=app
```

## 📊 Tech Stack

| Category | Technology |
|----------|-----------|
| **Framework** | Flask 2.3 |
| **Database** | MySQL 8.0 (Amazon RDS) |
| **ORM** | SQLAlchemy 3.1 |
| **Migrations** | Flask-Migrate 4.0 (Alembic) |
| **Authentication** | Flask-Login 0.6 |
| **Forms** | Flask-WTF 1.2 |
| **Email** | Flask-Mail 0.9 |
| **Driver** | PyMySQL 1.1 |
| **AWS SDK** | Boto3 1.34 |
| **Server** | Waitress / Gunicorn |
| **Frontend** | Bootstrap 5 |

## 📝 API Endpoints

| Method | Endpoint | Description | Auth Required |
|--------|----------|-------------|---------------|
| GET | `/` | Home page | No |
| GET | `/register` | Registration page | No |
| POST | `/register` | Create account | No |
| GET | `/login` | Login page | No |
| POST | `/login` | Authenticate user | No |
| GET | `/logout` | Logout user | Yes |
| GET | `/dashboard` | User dashboard | Yes |
| POST | `/todo/add` | Create todo | Yes |
| POST | `/todo/delete/<id>` | Delete todo | Yes |
| POST | `/todo/update/<id>` | Update todo | Yes |

##  Contributing

1. Fork the repository
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🙏 Acknowledgments

- Flask documentation
- AWS Elastic Beanstalk team
- Bootstrap community
- All contributors

**Made with ❤️ using Flask and AWS**
