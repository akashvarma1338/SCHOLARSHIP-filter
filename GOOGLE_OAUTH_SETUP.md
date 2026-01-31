# Google OAuth Setup Guide

## Step-by-Step Instructions to Enable Google Sign-In

### 1. Create Google Cloud Project

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Click "Select a project" → "New Project"
3. Enter project name: "Scholarship Eligibility Filter"
4. Click "Create"

### 2. Enable Required APIs

1. In the Google Cloud Console, go to "APIs & Services" → "Library"
2. Search and enable these APIs:
   - **Google+ API** (for user profile info)
   - **Google Identity Services API** (for authentication)

### 3. Configure OAuth Consent Screen

1. Go to "APIs & Services" → "OAuth consent screen"
2. Choose **"External"** user type
3. Fill in the Application Information:
   - **App name**: Scholarship Eligibility Filter
   - **User support email**: your-email@gmail.com
   - **App logo**: (optional)
   - **App domain**: (leave blank for localhost)
   - **Developer contact information**: your-email@gmail.com
4. Click "Save and Continue"
5. **Scopes**: Click "Add or Remove Scopes"
   - Add: `../auth/userinfo.email`
   - Add: `../auth/userinfo.profile`
   - Add: `openid`
6. Click "Save and Continue"
7. **Test users**: Add your Gmail address
8. Click "Save and Continue"

### 4. Create OAuth Credentials

1. Go to "APIs & Services" → "Credentials"
2. Click "Create Credentials" → "OAuth client ID"
3. Choose **"Web application"**
4. Enter name: "Scholarship App Web Client"
5. **Authorized JavaScript origins**:
   ```
   http://localhost:5000
   ```
6. **Authorized redirect URIs**:
   ```
   http://localhost:5000/admin/google/callback
   http://localhost:5000/student/google/callback
   ```
7. Click "Create"
8. **Copy the Client ID and Client Secret** - you'll need these!

### 5. Update Application Configuration

1. Open `config.py` in your project
2. Replace the placeholder values:
   ```python
   GOOGLE_CLIENT_ID = 'your-actual-client-id-here'
   GOOGLE_CLIENT_SECRET = 'your-actual-client-secret-here'
   ```
3. Set authentication mode:
   ```python
   USE_SIMULATED_AUTH = False
   USE_SIMULATED_AUTH_STUDENT = False
   ```

### 6. Test the Setup

1. Start your application: `python start.py`
2. Go to http://localhost:5000
3. Click "Student Login" → "Sign in with Google"
4. You should be redirected to Google's sign-in page
5. After signing in, you should be redirected back to your app

## Troubleshooting

### Error: "redirect_uri_mismatch"
- Check that your redirect URIs in Google Cloud Console exactly match:
  - `http://localhost:5000/admin/google/callback`
  - `http://localhost:5000/student/google/callback`
- Make sure there are no trailing slashes or extra characters

### Error: "access_blocked"
- Make sure you've added your email to the "Test users" list in OAuth consent screen
- Ensure the required APIs are enabled

### Error: "invalid_client"
- Double-check your Client ID and Client Secret in `config.py`
- Make sure there are no extra spaces or characters

## Quick Test Mode

If you want to test the app without setting up Google OAuth:

1. In `config.py`, set:
   ```python
   USE_SIMULATED_AUTH = True
   USE_SIMULATED_AUTH_STUDENT = True
   ```
2. When you click "Sign in with Google", you'll get a simple form to enter any email
3. This is perfect for testing the application functionality

## Production Setup

For production deployment:

1. Update OAuth consent screen to "Production" status
2. Add your actual domain to authorized origins and redirect URIs
3. Set `DEMO_MODE = False` in config.py
4. Use environment variables for sensitive credentials:
   ```python
   GOOGLE_CLIENT_ID = os.environ.get('GOOGLE_CLIENT_ID')
   GOOGLE_CLIENT_SECRET = os.environ.get('GOOGLE_CLIENT_SECRET')
   ```

## Need Help?

If you're still having issues:
1. Check the browser console for error messages
2. Look at the Flask application logs
3. Verify all steps above are completed correctly
4. Try using simulated auth first to test the app functionality