# 🏪 Kinmel E-Commerce Platform

A comprehensive, full-featured e-commerce platform built with Django, featuring multi-role user management, shop creation, product management, and secure payment processing.

## 🚀 Features

### 👥 **Multi-Role User System**
- **Admin**: Complete platform management and oversight
- **Trader**: Shop creation and product management (max 4 shops per trader)
- **Customer**: Shopping, ordering, and account management

### 🏪 **Shop Management**
- **Shop Creation**: Traders can create and manage multiple shops
- **Admin Approval**: All shops require admin approval before going live
- **Product Management**: Full CRUD operations for products
- **Category System**: Organized product categorization

### 🔐 **Advanced Authentication**
- **Role-based Access Control**: Secure role-based permissions
- **Email Notifications**: Automated approval notifications for traders
- **OTP Password Reset**: Secure 6-digit OTP system for password recovery
- **Session Management**: Secure user session handling

### 📧 **Email Notification System**
- **Trader Approval**: Professional email notifications when traders are approved
- **Shop Approval**: Automated notifications for shop approvals
- **Password Reset**: Secure OTP delivery via email
- **Professional Templates**: Branded, responsive email designs

### 🛡️ **Security Features**
- **OTP Expiration**: 15-minute time limits for security codes
- **Attempt Limiting**: Maximum 3 attempts per OTP
- **Password Strength**: Minimum 8-character requirements
- **CSRF Protection**: Built-in Django security features

### 🎨 **Modern UI/UX**
- **Responsive Design**: Works on all devices
- **Bootstrap 5**: Modern, professional styling
- **Interactive Elements**: Real-time feedback and validation
- **Professional Dashboard**: Comprehensive admin and trader dashboards

## 🛠️ Technology Stack

- **Backend**: Django 4.2+
- **Database**: SQLite (development) / PostgreSQL (production)
- **Frontend**: HTML5, CSS3, JavaScript, Bootstrap 5
- **Email**: Django Email Framework with SMTP support
- **Authentication**: Django's built-in auth system with custom extensions
- **Security**: CSRF protection, secure password hashing, OTP validation

## 📦 Installation

### Prerequisites
- Python 3.8+
- pip (Python package manager)
- Git

### Setup Instructions

1. **Clone the repository**
   ```bash
   git clone https://github.com/user-bhabuk/Kinmel-Ecommerce-App.git
   cd Kinmel-Ecommerce-App
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment setup**
   ```bash
   # Create .env file with your settings
   cp .env.example .env
   # Edit .env with your configuration
   ```

5. **Database setup**
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Create superuser**
   ```bash
   python manage.py createsuperuser
   ```

7. **Run the server**
   ```bash
   python manage.py runserver
   ```

8. **Access the application**
   - Main site: http://localhost:8000/
   - Admin panel: http://localhost:8000/adminpanel/
   - Django admin: http://localhost:8000/admin/

## 🎯 Usage Guide

### **For Admins**
1. Login at `/adminpanel/` with admin credentials
2. Review and approve trader applications
3. Manage shops and product categories
4. Monitor platform activity and analytics

### **For Traders**
1. Register as a trader at `/users/register/trader/`
2. Wait for admin approval (email notification sent)
3. Create shops (max 4 per trader)
4. Add products and manage inventory
5. Process customer orders

### **For Customers**
1. Register at `/users/register/customer/`
2. Browse shops and products
3. Add items to cart and place orders
4. Use OTP system for password recovery if needed

## 📧 Email Configuration

### Development (Console Backend)
```python
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
```

### Production (SMTP)
```python
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
EMAIL_HOST = 'smtp.gmail.com'
EMAIL_PORT = 587
EMAIL_USE_TLS = True
EMAIL_HOST_USER = 'your-email@gmail.com'
EMAIL_HOST_PASSWORD = 'your-app-password'
```

## 🧪 Testing

Run the comprehensive test suite:
```bash
# Test email notifications
python test_email_notifications.py

# Test OTP system
python test_otp_system.py

# Test admin functionality
python test_admin_functionality.py
```

## 📁 Project Structure

```
Kinmel_Eccomerce_APP/
├── adminpanel/          # Admin dashboard and management
├── ecommerce/           # Main Django project settings
├── orders/              # Order management system
├── payments/            # Payment processing
├── shops/               # Shop and product management
├── users/               # User authentication and management
├── utils/               # Utility functions and services
├── templates/           # HTML templates
├── static/              # CSS, JS, and static assets
├── media/               # User uploaded files
└── requirements.txt     # Python dependencies
```

## 🔧 Key Features Implementation

### **OTP Password Reset**
- 6-digit random OTP generation
- 15-minute expiration window
- Maximum 3 attempts per OTP
- Professional email templates
- Secure validation and cleanup

### **Email Notification System**
- Trader approval notifications
- Shop approval confirmations
- Password reset OTP delivery
- Professional HTML templates
- Automatic email sending on admin actions

### **Admin Panel**
- Comprehensive trader management
- Shop approval workflow
- User analytics and reporting
- Real-time statistics dashboard

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 👨‍💻 Author

**Bhabuk Ghimire**
- GitHub: [@user-bhabuk](https://github.com/user-bhabuk)
- Email: bhabuk@example.com

## 🙏 Acknowledgments

- Django community for the excellent framework
- Bootstrap team for the responsive UI components
- All contributors who helped improve this project

---

**Built with ❤️ using Django and modern web technologies**
