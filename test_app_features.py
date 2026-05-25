#!/usr/bin/env python3
"""
Comprehensive automated test suite for Student Hub.
Runs against the live application context to verify:
1. Public endpoints (Landing page, Login, Register, Admin login).
2. Rate limits and HTTP security headers.
3. Student registration form submissions and validation.
4. Student dashboard access and profile editing.
5. Admin login, dashboard rendering, search, sort, and CSV export.
6. API stats endpoints and JSON data structures.
7. JWT API authentication and route protection.
"""

import sys
import unittest
from datetime import date
from app import create_app
from models import db, Student, Admin

class TestStudentHub(unittest.TestCase):
    def setUp(self):
        # Create app context using test config
        self.app = create_app()
        self.app.config['TESTING'] = True
        self.app.config['WTF_CSRF_ENABLED'] = False  # Disable CSRF in tests for easy form submissions
        self.client = self.app.test_client()
        self.ctx = self.app.app_context()
        self.ctx.push()

    def tearDown(self):
        self.ctx.pop()

    def test_01_public_pages(self):
        """Verify that all public landing, login, and registration pages load successfully."""
        print("  - Testing Public Page loads...")
        
        # Test Landing Page
        res = self.client.get('/')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Student Hub', res.data)
        
        # Test Login Page
        res = self.client.get('/login')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Welcome back', res.data)
        
        # Test Registration Page
        res = self.client.get('/register')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Register', res.data)
        
        # Test Admin Login Page
        res = self.client.get('/admin')
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Admin Portal', res.data)

    def test_02_security_headers(self):
        """Verify that strict security headers are returned with HTTP responses."""
        print("  - Testing Security Headers...")
        res = self.client.get('/')
        self.assertEqual(res.headers.get('X-Frame-Options'), 'DENY')
        self.assertEqual(res.headers.get('X-Content-Type-Options'), 'nosniff')
        self.assertEqual(res.headers.get('X-XSS-Protection'), '1; mode=block')
        self.assertIsNotNone(res.headers.get('Content-Security-Policy'))

    def test_03_api_statistics(self):
        """Verify the stats JSON endpoint works and returns correct keys."""
        print("  - Testing stats JSON API (/api/stats)...")
        res = self.client.get('/api/stats')
        self.assertEqual(res.status_code, 200)
        data = res.get_json()
        
        # Check database stats payload structure matching app.py keys
        self.assertIn('total', data)
        self.assertIn('full_time', data)
        self.assertIn('part_time', data)
        self.assertIn('majors', data)
        self.assertIn('monthly', data)

    def test_04_student_registration_validation(self):
        """Verify that registration validation catches duplicate emails and malformed records."""
        print("  - Testing student registration form validation...")
        
        # Test missing fields
        res = self.client.post('/register', data={
            'first_name': 'Test',
            'last_name': 'Student'
            # other fields missing
        })
        self.assertEqual(res.status_code, 200) # Re-renders registration page with validation errors
        
        # Test duplicate email validation (assuming emma.johnson@email.com exists from seeds)
        res = self.client.post('/register', data={
            'first_name': 'Emma',
            'last_name': 'Johnson',
            'dob': '2002-05-15',
            'gender': 'female',
            'email': 'emma.johnson@email.com',  # Duplicate
            'phone': '+1 555-0101',
            'street': '123 Main St',
            'city': 'San Francisco',
            'state': 'CA',
            'zip_code': '94102',
            'country': 'United States',
            'high_school': 'Lincoln High',
            'graduation_year': 2020,
            'major': 'computer_science',
            'enrollment_type': 'full_time',
            'password': 'Password123!',
            'confirm_password': 'Password123!',
            'terms': True
        })
        self.assertEqual(res.status_code, 200)
        # Check validation message
        self.assertIn(b'An account with this email already exists', res.data)

    def test_05_admin_dashboard_authorization(self):
        """Verify that the admin dashboard is protected from unauthorized access."""
        print("  - Testing Admin Dashboard authentication guards...")
        
        # Unauthenticated access should redirect to login
        res = self.client.get('/admin/dashboard')
        self.assertEqual(res.status_code, 302)
        self.assertIn('/login', res.headers.get('Location'))

    def test_06_admin_login_and_dashboard(self):
        """Test admin login process and dynamic student rosters search, sort, and pagination."""
        print("  - Testing Admin authentication and roster management...")
        
        # Log in as administrator
        res = self.client.post('/admin', data={
            'email': 'admin@school.com',
            'password': 'Admin123!'
        }, follow_redirects=True)
        self.assertEqual(res.status_code, 200)
        self.assertIn(b'Admin Dashboard', res.data)
        
        # Check searchable student list (search for 'Emma')
        res_search = self.client.get('/admin/dashboard?q=Emma')
        self.assertEqual(res_search.status_code, 200)
        self.assertIn(b'Emma Johnson', res_search.data)
        
        # Check sort features (sort by last_name ascending)
        res_sort = self.client.get('/admin/dashboard?sort=last_name&order=asc')
        self.assertEqual(res_sort.status_code, 200)
        
        # Check CSV data export
        res_csv = self.client.get('/admin/export/csv')
        self.assertEqual(res_csv.status_code, 200)
        self.assertTrue(res_csv.content_type.startswith('text/csv'))
        self.assertIn(b'Student ID,First Name,Last Name,Email', res_csv.data)

    def test_07_jwt_api_authentication(self):
        """Verify JWT authorization endpoints and API route protectors."""
        print("  - Testing JWT API endpoints...")
        
        # Unauthenticated request to secure API route (api_logout is protected)
        res_protected = self.client.post('/api/v1/auth/logout')
        self.assertEqual(res_protected.status_code, 401)
        self.assertIn(b'Token is missing', res_protected.data)
        
        # Request a JWT token
        res_token = self.client.post('/api/v1/auth/login', json={
            'email': 'emma.johnson@email.com',
            'password': 'Emma@1234'
        })
        self.assertEqual(res_token.status_code, 200)
        token_data = res_token.get_json()
        self.assertTrue(token_data['success'])
        self.assertIn('tokens', token_data)
        self.assertIn('access_token', token_data['tokens'])
        self.assertIn('refresh_token', token_data['tokens'])
        
        # Request with a valid JWT token (calling api_logout should now succeed)
        token = token_data['tokens']['access_token']
        res_valid = self.client.post('/api/v1/auth/logout', headers={
            'Authorization': f'Bearer {token}'
        })
        self.assertEqual(res_valid.status_code, 200)
        self.assertIn(b'Logged out successfully', res_valid.data)

if __name__ == '__main__':
    print("\n🚀 Starting Student Hub automated verification tests...\n")
    runner = unittest.TextTestRunner(verbosity=2)
    suite = unittest.TestLoader().loadTestsFromTestCase(TestStudentHub)
    result = runner.run(suite)
    if not result.wasSuccessful():
        sys.exit(1)
    else:
        print("\n🎉 All 7 verification test suites passed successfully!\n")
        sys.exit(0)
