# 💰 Finance Tracker - Personal Finance Management System

![Django](https://img.shields.io/badge/Django-5.1-green.svg)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-16-blue.svg)
![Python](https://img.shields.io/badge/Python-3.13-blue.svg)

A comprehensive web application for managing personal finances with advanced analytics, budgets, and multi-account support.

## 🎯 Features

### MVP (v1.0) - In Development
- [ ] Multi-account management (cash, bank, credit cards)
- [ ] Income and expense tracking
- [ ] Customizable categories with hierarchies
- [ ] Financial dashboard with summary
- [ ] Date, category, and account filters
- [ ] Expense distribution charts

### Planned Features (v2.0)
- [ ] Monthly budgets by category
- [ ] Recurring expenses automation
- [ ] Savings goals
- [ ] Tag system
- [ ] Excel/CSV export
- [ ] Multi-currency with automatic conversion

## 🛠️ Tech Stack

- **Backend**: Django 5.1.5
- **Database**: PostgreSQL 16
- **Python**: 3.13.1
- **ORM**: Django ORM
- **Testing**: Pytest + pytest-django
- **Environment**: pyenv + virtualenvwrapper

## 📋 Prerequisites

- Python 3.13+
- PostgreSQL 16
- pyenv (recommended)
- virtualenvwrapper (recommended)

## 🚀 Installation
```bash
# Clone repository
git clone https://github.com/YOUR-USERNAME/finance-tracker-django.git
cd finance-tracker-django

# Create virtual environment
mkvirtualenv finance_tracker

# Install dependencies
pip install -r requirements.txt

# Copy environment variables
cp .env.example .env
# Edit .env with your database credentials

# Run migrations
python manage.py migrate

# Create superuser
python manage.py createsuperuser

# Run development server
python manage.py runserver
```

Access: http://localhost:8000

## 📊 Project Structure
```
finance-tracker-django/
├── apps/
│   ├── accounts/          # User management and profiles
│   ├── transactions/      # Transactions and movements
│   ├── categories/        # Categories and tags
│   ├── budgets/           # Budgets and goals
│   └── analytics/         # Reports and analytics
├── config/
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
├── templates/
├── static/
├── media/
├── tests/
├── docs/
├── requirements.txt
└── manage.py
```

## 🧪 Testing
```bash
pytest
```

## 📄 License

MIT License

## 👤 Author

**Valentin Caceres Harris**
- GitHub: [@your-username](https://github.com/your-username)

---

⭐ Star this repo if you find it helpful!
