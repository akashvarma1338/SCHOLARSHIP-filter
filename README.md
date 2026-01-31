# 🎓 Scholarship Eligibility Filter

A comprehensive web application that helps students check their eligibility for various scholarships based on dynamic rules and criteria.

## ✨ Features

- **Student Portal**: Students can register, complete profiles, and check scholarship eligibility
- **Admin Panel**: Admins can manage scholarships, rules, and review applications
- **Dynamic Rules Engine**: Flexible rule system for different scholarship criteria
- **Application Management**: Students can apply for eligible scholarships
- **Document Upload**: Support for document submission and review
- **Dashboard Analytics**: Statistics and insights for administrators
- **Responsive Design**: Works on desktop and mobile devices

## 🚀 Quick Start

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. **Clone or download the project**
   ```bash
   cd eduhack-main
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python run.py
   ```

4. **Access the application**
   - Main Application: http://localhost:5000
   - Admin Panel: http://localhost:5000/admin
   - Dashboard: http://localhost:5000/dashboard

## 🔐 Authentication

The application is configured to use **simulated authentication** for easy testing:

### For Students:
1. Go to http://localhost:5000
2. Click "Student Login"
3. Enter any email address and name
4. You'll be logged in automatically

### For Admins:
1. Go to http://localhost:5000/admin
2. Click "Login with Google" (will redirect to simulated auth)
3. Enter any email address and name
4. First admin becomes super admin automatically

## 📋 Default Scholarships

The application comes with 4 pre-configured scholarships:

1. **Merit Excellence Scholarship** (₹50,000)
   - Minimum 85% marks
   - No backlogs
   - Full-time student

2. **Financial Assistance Scholarship** (₹75,000)
   - Minimum 75% marks
   - Family income ≤ ₹2,50,000
   - No backlogs
   - Full-time student

3. **SC/ST Welfare Scholarship** (₹60,000)
   - Minimum 60% marks
   - SC/ST category
   - Family income ≤ ₹3,00,000
   - Full-time student

4. **General Academic Scholarship** (₹25,000)
   - Minimum 75% marks
   - Family income ≤ ₹2,50,000
   - No backlogs
   - Full-time student

## 🎯 How to Use

### For Students:
1. **Register/Login**: Use the student login with any email
2. **Complete Profile**: Fill in academic and personal details
3. **Check Eligibility**: System automatically checks all scholarships
4. **View Results**: See eligible scholarships with priority scores
5. **Apply**: Submit applications for eligible scholarships
6. **Track Applications**: Monitor application status in "My Applications"

### For Admins:
1. **Login**: Access admin panel with any email (first user becomes super admin)
2. **Manage Scholarships**: Create, edit, or delete scholarship programs
3. **Configure Rules**: Set up dynamic eligibility criteria
4. **Review Applications**: Approve/reject student applications
5. **Request Documents**: Ask students for additional documentation
6. **View Analytics**: Monitor application statistics and trends

## 🛠️ Configuration

### Database
- Uses SQLite database (`scholarship.db`)
- Automatically created on first run
- All tables and sample data initialized automatically

### File Uploads
- Documents stored in `uploads/` folder
- Supported formats: PDF, PNG, JPG, JPEG, DOC, DOCX
- Maximum file size: 5MB

### Google OAuth (Optional)
To enable real Google OAuth instead of simulated auth:

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project or select existing
3. Enable Google+ API
4. Create OAuth 2.0 credentials
5. Set authorized redirect URIs:
   - `http://localhost:5000/admin/google/callback`
   - `http://localhost:5000/student/google/callback`
6. Update `config.py`:
   ```python
   GOOGLE_CLIENT_ID = 'your-client-id'
   GOOGLE_CLIENT_SECRET = 'your-client-secret'
   USE_SIMULATED_AUTH = False
   USE_SIMULATED_AUTH_STUDENT = False
   ```

## 📁 Project Structure

```
eduhack-main/
├── app.py                 # Main Flask application
├── models.py             # Database models
├── rules_engine.py       # Eligibility rules logic
├── config.py             # Configuration settings
├── requirements.txt      # Python dependencies
├── run.py               # Startup script
├── scholarship.db       # SQLite database (created automatically)
├── static/
│   ├── css/
│   │   └── style.css    # Main stylesheet
│   └── js/
│       ├── main.js      # Main JavaScript
│       └── admin.js     # Admin panel JavaScript
├── templates/           # HTML templates
│   ├── index.html       # Home page
│   ├── admin.html       # Admin panel
│   ├── dashboard.html   # Analytics dashboard
│   ├── results.html     # Eligibility results
│   └── ...             # Other templates
└── uploads/            # Document storage (created automatically)
```

## 🔧 API Endpoints

### Student APIs
- `POST /api/students` - Create/update student profile
- `GET /api/check-eligibility/{student_id}` - Check scholarship eligibility
- `POST /api/applications` - Apply for scholarship
- `GET /api/applications/my` - Get student's applications

### Admin APIs
- `GET /api/scholarships` - Get all scholarships
- `POST /api/scholarships` - Create new scholarship
- `PUT /api/scholarships/{id}` - Update scholarship
- `DELETE /api/scholarships/{id}` - Delete scholarship
- `GET /api/admin/applications` - Get all applications
- `PUT /api/admin/applications/{id}/status` - Update application status

### Dashboard APIs
- `GET /api/dashboard/stats` - Get dashboard statistics

## 🎨 Customization

### Adding New Scholarship Rules
1. Go to Admin Panel → Scholarships
2. Select a scholarship
3. Add new rules with:
   - Field (marks_percentage, family_income, category, etc.)
   - Operator (>=, <=, ==, !=, in)
   - Value (threshold or list)
   - Weight (for priority scoring)

### Styling
- Main CSS: `static/css/style.css`
- Uses CSS variables for easy color customization
- Responsive design with mobile support

## 🐛 Troubleshooting

### Common Issues

1. **Module not found errors**
   ```bash
   pip install -r requirements.txt
   ```

2. **Database errors**
   - Delete `scholarship.db` and restart the application
   - Database will be recreated automatically

3. **Google OAuth errors**
   - Set `USE_SIMULATED_AUTH = True` in `config.py`
   - Use simulated authentication for testing

4. **Port already in use**
   - Change port in `run.py`: `app.run(port=5001)`

### Getting Help
- Check the console output for error messages
- Ensure all dependencies are installed
- Verify Python version (3.7+)

## 📄 License

This project is open source and available under the MIT License.

## 🤝 Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Test thoroughly
5. Submit a pull request

## 📞 Support

For issues or questions:
- Check the troubleshooting section
- Review the console output for errors
- Ensure all setup steps are completed

---

**Happy Coding! 🎓✨**