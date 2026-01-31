#!/usr/bin/env python3
"""
Simple startup script for the Scholarship Eligibility Filter
This script initializes the database and starts the Flask application
"""

from app import app, db, init_sample_data

if __name__ == '__main__':
    print("=" * 60)
    print("🎓 SCHOLARSHIP ELIGIBILITY FILTER")
    print("=" * 60)
    print("Initializing application...")
    
    # Create database tables and initialize sample data
    with app.app_context():
        print("📊 Creating database tables...")
        db.create_all()
        print("✅ Database tables created successfully!")
        
        print("📋 Initializing sample scholarships...")
        init_sample_data()
        print("✅ Sample data initialized!")
    
    print("\n" + "=" * 60)
    print("🚀 STARTING SERVER")
    print("=" * 60)
    print("🌐 Application URL: http://localhost:5000")
    print("👨‍💼 Admin Panel: http://localhost:5000/admin")
    print("👩‍🎓 Student Portal: http://localhost:5000")
    print("\n📝 DEMO CREDENTIALS:")
    print("   • Use any email for simulated authentication")
    print("   • First admin user becomes super admin automatically")
    print("=" * 60)
    print("\n🔄 Starting Flask development server...")
    
    # Run the application
    app.run(debug=True, host='0.0.0.0', port=5000)