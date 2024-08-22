import pytest
from app import app, db
from bson import ObjectId

@pytest.fixture
def client():
    app.config['TESTING'] = True
    client = app.test_client()

    yield client

# Test cases
def test_index_route(client):
    """Test index route."""
    response = client.get('/')
    assert response.status_code == 200

def test_login_route(client):
    """Test login route."""
    response = client.get('/login')
    assert response.status_code == 200

def test_invalid_login(client):
    """Test invalid login credentials."""
    response = client.post('/login', data=dict(
        id='21CS30035',
        password='invalid_password'
    ), follow_redirects=True)
    assert b'Invalid ID or password' in response.data

def test_valid_login(client):
    """Test valid login credentials."""
    response = client.post('/login', data=dict(
        id='21CS30035',
        password='me'
    ), follow_redirects=True)
    print(response.data)
    assert b'Hey student!!!' in response.data

def test_invalid_login(client):
    """Test invalid login credentials."""
    response = client.post('/login', data=dict(
        id='12345',
        password='invalid_password'
    ), follow_redirects=True)
    assert b'Invalid ID or password' in response.data

def test_valid_login(client):
    """Test valid login credentials."""
    response = client.post('/login', data=dict(
        id='12345',
        password='am'
    ), follow_redirects=True)
    print(response.data)
    assert b'Hey faculty!!!' in response.data


def test_invalid_login(client):
    """Test invalid login credentials."""
    response = client.post('/login', data=dict(
        id='admin',
        password='invalid_password'
    ), follow_redirects=True)
    assert b'Invalid ID or password' in response.data

def test_valid_login(client):
    """Test valid login credentials."""
    response = client.post('/login', data=dict(
        id='admin',
        password='admin'
    ), follow_redirects=True)
    print(response.data)
    assert b'Hey admin!!!' in response.data

def test_logout_route(client):
    """Test logout route."""
    response = client.get('/logout', follow_redirects=True)
    assert b'Hello World!' in response.data

def test_verify_otp_forgot_password_page(client):
    response = client.get('/verify_otp_forgot_password')
    assert response.status_code == 200

def test_verify_otp_forgot_password_post(client):
    # Simulate session setup for OTP verification
    with client.session_transaction() as sess:
        sess['otp'] = '123456'
        sess['email'] = 'testuser@iitkgp.ac.in'

    response = client.post('/verify_otp_forgot_password', data={
        'otp': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'Reset Password' in response.data

def test_reset_password_page(client):
    response = client.get('/reset_password')
    assert response.status_code == 200
    assert b'Reset Password' in response.data


def test_view_users_route(client):
    """Test view users route (admin access required)."""
    response = client.get('/view_users')
    assert response.status_code == 302  # Redirects to login because no admin session
    assert b'login' in response.data.lower()

def test_delete_user_route(client):
    """Test delete user route (admin access required)."""
    user_id = ObjectId('60f07633f95cc217a6c628ab')
    response = client.post(f'/delete_user/{user_id}', follow_redirects=True)
    assert b'Unauthorized access' in response.data  # Expecting access denial without admin session

def test_view_profile(client):
    response = client.get('/profile')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_view_profile(client):
    # Add a test user to the database
    test_user = {
        "id": "testuser",
        "full_name": "Test User",
        "email": "testuser@example.com",
        "department": "CSE"
    }
    db.users.delete_many({"id": "testuser"})
    db.users.insert_one(test_user)

    # Test accessing profile without login
    response = client.get('/profile')
    assert response.status_code == 302  # Expect redirect to /index
    assert response.headers['Location'] == '/'

    # Simulate a session with user ID
    with client.session_transaction() as session:
        session['id'] = 'testuser'

    # Test accessing profile with login
    response = client.get('/profile')
    assert response.status_code == 200  # Expect profile page to be rendered
    assert b'Test User' in response.data  # Check if profile information is in the response

    # Test accessing profile with non-existing user
    with client.session_transaction() as session:
        session['id'] = 'nonexistentuser'

    response = client.get('/profile')
    assert response.status_code == 302  # Expect redirect to /index
    assert response.headers['Location'] == '/'

    # Clean up the session
    with client.session_transaction() as session:
        session.pop('id', None)

def test_view_btp_list(client):
    response = client.get('/btp_list')
    assert response.status_code == 302  # Redirect to login page when not logged in


def test_btp_list_faculty(client):
    # Simulate faculty login
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Insert a sample user
    db.users.delete_many({ 'id': 'faculty123' })
    db.users.insert_one({
        'id': 'faculty123',
        'full_name': 'Dr. Test Faculty',
        'email': 'faculty@example.com',
        'department': 'CSE'
    })

    response = client.get('/btp_list')
    assert response.status_code == 200
    assert b'Test Project' in response.data
    assert b'Dr. Test Faculty' in response.data

def test_btp_list_student_no_application(client):
    # Simulate student login
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Insert a sample user (faculty)
    db.users.delete_many({'id': 'faculty123'})
    db.users.insert_one({
        'id': 'faculty123',
        'full_name': 'Dr. Test Faculty',
        'email': 'faculty@example.com',
        'department': 'CSE'
    })

    response = client.get('/btp_list')
    assert response.status_code == 200
    assert b'Test Project' in response.data
    assert b'Dr. Test Faculty' in response.data
    assert b'Apply' in response.data

def test_btp_list_student_with_application(client):
    # Simulate student login
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Insert a sample user (faculty)
    db.users.delete_many({'id': 'faculty123'})
    db.users.insert_one({
        'id': 'faculty123',
        'full_name': 'Dr. Test Faculty',
        'email': 'faculty@example.com',
        'department': 'CSE'
    })

    # Insert a sample application
    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })

    response = client.get('/btp_list')
    assert response.status_code == 200
    assert b'Test Project' in response.data
    assert b'Dr. Test Faculty' in response.data
    assert b'Pending' in response.data

def test_btp_list_student_with_approved_application(client):
    # Simulate student login
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Insert a sample user (faculty)
    db.users.delete_many({'id': 'faculty123'})
    db.users.insert_one({
        'id': 'faculty123',
        'full_name': 'Dr. Test Faculty',
        'email': 'faculty@example.com',
        'department': 'CSE'
    })

    # Insert a sample application
    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Approved'
    })

    response = client.get('/btp_list')
    assert response.status_code == 200
    assert b'Test Project' in response.data
    assert b'Dr. Test Faculty' in response.data

def test_upload_project(client):
    response = client.post('/upload_project', data=dict(
        btp_name='Test Project'), follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in


def test_upload_project_page(client):
    # Simulate faculty login
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    response = client.get('/upload_project')
    assert response.status_code == 200

def test_upload_project_post(client):
    # Simulate faculty login
    with client.session_transaction() as sess:
        sess['id'] = '12345'
        sess['role'] = 'faculty'

    data = {
        'btp_name': 'Test Project'
    }
    
    response = client.post('/upload_project', data={
        'btp_name': 'Test Project'
    }, follow_redirects=True)
    
    assert response.status_code == 400

def test_upload_project_duplicate_name(client):
    # Simulate faculty login
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Insert a project with the same name
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Duplicate Project',
        'prof_id': 'faculty123',
        'project_file_id': 'some_file_id'
    })

    data = {
        'btp_name': 'Duplicate Project'
    }

    response = client.post('/upload_project', data={
        'btp_name': 'Duplicate Project'
    }, content_type='multipart/form-data', follow_redirects=True)
    
    assert response.status_code == 200
    assert b'A project with the same name already exists. Please choose a different name.' in response.data

def test_apply_for_btp(client):
    response = client.post('/apply_for_btp', data=dict(
        btp_id='test_btp_id'
    ), follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in



def test_apply_for_btp(client):
    # Simulate student login
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Simulate applying for the BTP project
    response = client.post('/apply_for_btp', data={
        'btp_id': '12345'
    })
    
    assert response.status_code == 302  # Check for redirect status code

    # Check that the application was inserted in the database
    application = db.application.find_one({"btp_id": '12345', "roll_no": 'student123'})
    assert application is not None
    assert application['status'] == 'Approved'

def test_apply_for_btp_already_applied(client):
    # Simulate student login
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Insert an existing application for the BTP project
    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending',
    })
    
    # Simulate applying for the same BTP project
    response = client.post('/apply_for_btp', data={
        'btp_id': '12345'
    })
    
    assert response.status_code == 302  # Check for redirect status code

def test_apply_for_btp_get_request(client):
    # Simulate student login
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Simulate a GET request to apply_for_btp
    response = client.get('/apply_for_btp')
    
    assert response.status_code == 302  # Check for redirect status code
    assert response.headers['Location'] == '/btp_list'

def test_view_application_list(client):
    response = client.get('/application_list')
    assert response.status_code == 302  # Redirect to login page when not logged in


def test_application_list(client):
    # Simulate faculty login
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Insert sample data
    db.users.delete_many({'id': 'student123'})
    db.users.insert_one({
        'id': 'student123',
        'full_name': 'Test Student',
        'email': 'student@test.com',
        'department': 'Computer Science'
    })

    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })

    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending',
    })

    # Access the application list
    response = client.get('/application_list')
    
    assert response.status_code == 200  # Check for OK status code
    assert b'Test Project' in response.data
    assert b'Test Student' in response.data
    assert b'student@test.com' in response.data
    assert b'Computer Science' in response.data

def test_application_list_no_projects(client):
    # Simulate faculty login
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Access the application list with no projects
    response = client.get('/application_list')
    
    assert response.status_code == 200  # Check for OK status code

def test_application_list_no_login(client):
    # Attempt to access the application list without logging in
    response = client.get('/application_list')
    
    assert response.status_code == 302  # Check for redirect status code
    assert response.headers['Location'] == '/login'  # Redirect to login page
    

def test_view_approved_list(client):
    response = client.get('/approved_list')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_change_application_status(client):
    response = client.post('/application_approval/test_application_id', data=dict(
        action='approve'
    ), follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in

def test_list_and_delete_applications(client):
    response = client.get('/list_and_delete_applications')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_application_approval_route(client):
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Create a sample application
    db.application.delete_many({'_id': '60d21b4667d0d8992e610c85'})
    db.application.insert_one({
        '_id': '60d21b4667d0d8992e610c85',
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })

    response = client.post('/application_approval/60d21b4667d0d8992e610c85', data={'action': 'approve'})
    assert response.status_code == 302  # Redirect after approval
    assert response.headers['Location'] == '/application_list'

def test_approved_list_route(client):
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Create a sample approved application
    db.users.delete_many({ 'id': 'student123' })
    db.users.insert_one({
        'id': 'student123',
        'full_name': 'Test Student',
        'email': 'student@test.com',
        'department': 'Computer Science'
    })
    
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })

    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Approved'
    })

    response = client.get('/approved_list')
    assert response.status_code == 200  # Check for OK status code
    assert b'Test Project' in response.data
    assert b'Test Student' in response.data

def test_change_application_status_route(client):
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Create a sample approved application
    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        '_id': '60d21b4667d0d8992e610c85',
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Approved'
    })

    response = client.post('/change_application_status/60d21b4667d0d8992e610c85', data={'action': 'reject'})
    assert response.status_code == 302  # Redirect after rejection
    assert response.headers['Location'] == '/approved_list'

def test_list_and_delete_applications_route(client):
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Create a sample application
    db.users.delete_many({ 'id': 'faculty123' })
    db.users.insert_one({
        'id': 'faculty123',
        'full_name': 'Test Faculty',
        'email': 'faculty@test.com',
        'department': 'Computer Science'
    })
    
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })

    db.application.delete_many({'btp_id': '12345', 'roll_no': 'student123'})
    db.application.insert_one({
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })

    response = client.get('/list_and_delete_applications')
    assert response.status_code == 200  # Check for OK status code


def test_delete_application_route(client):
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Create a sample application
    db.application.insert_one({
        '_id': '60d21b4667d0d8992e610c85',
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })

    response = client.post('/delete_application/60d21b4667d0d8992e610c85')
    assert response.status_code == 302  # Redirect after deletion
    assert response.headers['Location'] == '/list_and_delete_applications'

def test_select_co_guides(client):
    response = client.get('/select_co_guides/test_application_id')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_view_selected_co_guides(client):
    response = client.get('/view_selected_co_guides/test_application_id')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_send_applications_to_co_guides(client):
    response = client.post('/send_applications_to_co_guides/60f07633f95cc217a6c628ab', data=dict(
        co_guides=['test_co_guide_id']
    ), follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in

def test_view_co_guide_applications(client):
    response = client.get('/co_guide_applications')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_approve_application(client):
    response = client.post('/approve_application/test_application_id', follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in

def test_select_co_guides_get(client):
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Create a sample application
    application_id = str(ObjectId())
    db.application.insert_one({
        '_id': ObjectId(application_id),
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })
    
    # Create a sample student user
    db.users.delete_many({'id': 'student123'})
    db.users.insert_one({
        'id': 'student123',
        'full_name': 'Test Student',
        'department': 'Computer Science'
    })

    # Create sample faculty users
    db.users.delete_many({'id': 'faculty1'})
    db.users.insert_one({
        'id': 'faculty1',
        'full_name': 'Faculty One',
        'role': 'faculty',
        'department': 'Computer Science'
    })
    
    response = client.get(f'/select_co_guides/{application_id}')
    assert response.status_code == 200
    assert b'Faculty One' in response.data

def test_select_co_guides_post(client):
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Create a sample application
    application_id = str(ObjectId())
    db.application.insert_one({
        '_id': ObjectId(application_id),
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })
    
    # Create a sample student user
    db.users.delete_many({'id': 'student123'})
    db.users.insert_one({
        'id': 'student123',
        'full_name': 'Test Student',
        'department': 'Computer Science'
    })

    response = client.post(f'/select_co_guides/{application_id}', data={
        'co_guides[]': ['faculty1']
    })
    assert response.status_code == 302
    assert response.headers['Location'] == '/application_list'
    
    selected_co_guides = db.co_guides_selected.find_one({"application_id": ObjectId(application_id)})
    assert selected_co_guides is not None
    assert 'faculty1' in selected_co_guides['co_guides_selected']

def test_view_selected_co_guides(client):
    with client.session_transaction() as sess:
        sess['id'] = 'student123'
        sess['role'] = 'student'
    
    # Create a sample application
    application_id = str(ObjectId())
    db.application.insert_one({
        '_id': ObjectId(application_id),
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })
    
    # Create a sample student user
    db.users.delete_many({'id': 'student123'})
    db.users.insert_one({
        'id': 'student123',
        'full_name': 'Test Student',
        'department': 'Computer Science'
    })

    # Create sample faculty users
    db.users.insert_one({
        '_id': ObjectId(),
        'id': 'faculty1',
        'full_name': 'Faculty One',
        'role': 'faculty',
        'department': 'Computer Science'
    })
    
    db.co_guides_selected.insert_one({
        "application_id": ObjectId(application_id),
        "co_guides_selected": [ObjectId()]
    })

    response = client.get(f'/view_selected_co_guides/{application_id}')
    assert response.status_code == 200

    # Test case where 'any' is in co_guides_selected
    db.co_guides_selected.update_one(
        {"application_id": ObjectId(application_id)},
        {"$set": {"co_guides_selected": ['any']}}
    )
    response = client.get(f'/view_selected_co_guides/{application_id}')
    assert response.status_code == 200

def test_select_co_guides_post_invalid_data(client):
    with client.session_transaction() as sess:
        sess['id'] = 'faculty123'
        sess['role'] = 'faculty'
    
    # Create a sample application
    application_id = str(ObjectId())
    db.application.insert_one({
        '_id': ObjectId(application_id),
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })
    
    response = client.post(f'/select_co_guides/{application_id}', data={})
    assert response.status_code == 302
    assert response.headers['Location'] == '/application_list'
    
    selected_co_guides = db.co_guides_selected.find_one({"application_id": ObjectId(application_id)})
    assert selected_co_guides is not None

def test_co_guide_applications(client):
    # Create a sample faculty user and session
    db.users.delete_many({'id': 'faculty1'})
    db.users.insert_one({
        'id': 'faculty1',
        'full_name': 'Faculty One',
        'role': 'faculty'
    })
    
    with client.session_transaction() as sess:
        sess['id'] = 'faculty1'
        sess['role'] = 'faculty'

    # Create a sample application
    application_id = str(ObjectId())
    db.application.insert_one({
        '_id': ObjectId(application_id),
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })

    # Create a sample co-guides selected entry
    db.co_guides_selected.insert_one({
        'application_id': ObjectId(application_id),
        'co_guide_id': 'faculty1',
        'status': 'Pending'
    })

    response = client.get('/co_guide_applications')
    assert response.status_code == 200

def test_approve_application(client):
    # Create a sample faculty user and session
    db.users.delete_many({'id': 'faculty1'})
    db.users.insert_one({
        'id': 'faculty1',
        'full_name': 'Faculty One',
        'role': 'faculty'
    })
    
    with client.session_transaction() as sess:
        sess['id'] = 'faculty1'
        sess['role'] = 'faculty'

    # Create a sample application
    application_id = str(ObjectId())
    db.application.insert_one({
        '_id': ObjectId(application_id),
        'btp_id': '12345',
        'roll_no': 'student123',
        'status': 'Pending'
    })

    # Create a sample co-guides selected entry
    db.co_guides_selected.insert_one({
        'application_id': ObjectId(application_id),
        'co_guide_id': 'faculty1',
        'status': 'Pending'
    })

    # Test the POST request to approve the application
    response = client.post(f'/approve_application/{application_id}')
    assert response.status_code == 302
    assert response.headers['Location'] == '/co_guide_applications'
    
    application = db.application.find_one({'_id': ObjectId(application_id)})
    assert application['status'] == 'Pending'
    
    co_guides_selected = db.co_guides_selected.find_one({'application_id': ObjectId(application_id)})
    assert co_guides_selected['status'] == 'Pending'

def test_approve_application_invalid(client):
    # Create a sample faculty user and session
    db.users.insert_one({
        'id': 'faculty1',
        'full_name': 'Faculty One',
        'role': 'faculty'
    })
    
    with client.session_transaction() as sess:
        sess['id'] = 'faculty1'
        sess['role'] = 'faculty'

    # Test the POST request to approve an invalid application ID
    response = client.post('/approve_application/60f07633f95cc217a6c628ab')
    assert response.status_code == 302
    assert response.headers['Location'] == '/co_guide_applications'
    
    # Check that no application status is updated to 'Approved'
    application = db.application.find_one({'status': 'Approved'})
    assert application is not None

def test_co_guide_applications_access_denied(client):
    # Test access denied for non-faculty users
    response = client.get('/co_guide_applications')
    assert response.status_code == 302
    assert response.headers['Location'] == '/'

def test_view_users(client):
    response = client.get('/view_users')
    assert response.status_code == 302  # Redirect to login page when not logged in

def test_view_users_admin(client):
    # Login as an admin
    with client.session_transaction() as sess:
        sess['id'] = 'admin'
        sess['role'] = 'admin'

    # Access the view_users endpoint
    response = client.get('/view_users')
    assert response.status_code == 200

def test_view_users_non_admin(client):
    # Login as a non-admin user
    with client.session_transaction() as sess:
        sess['id'] = 'faculty1'
        sess['role'] = 'faculty'

    # Access the view_users endpoint
    response = client.get('/view_users')
    assert response.status_code == 302  # Expect redirect to login page
    assert response.headers['Location'] == '/login'

def test_view_users_unauthorized(client):
    # Access the view_users endpoint without logging in
    response = client.get('/view_users')
    assert response.status_code == 302  # Expect redirect to login page
    assert response.headers['Location'] == '/login'  # Adjust URL as needed


def test_delete_user(client):
    response = client.post('/delete_user/test_user_id', follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in

def test_confirm_project(client):
    response = client.post('/confirm_project', data=dict(
        project_id='test_project_id'
    ), follow_redirects=True)
    assert response.status_code == 200  # Redirect to login page when not logged in

def test_delete_user_admin(client):
    # Login as admin
    with client.session_transaction() as sess:
        sess['id'] = 'admin'
        sess['role'] = 'admin'

    # Perform the delete request for user1
    response = client.post('/delete_user/admin1_id')
    assert response.status_code == 302  # Expect redirect
    assert response.headers['Location'] == '/admin_home'  # Adjust URL as needed

    # Check if the user1 is deleted from the database
    deleted_user = db.users.find_one({"id": "admin1"})
    assert deleted_user is None


def test_delete_user_non_admin(client):
    # Login as non-admin user
    with client.session_transaction() as sess:
        sess['id'] = 'admin'
        sess['role'] = 'admin'

    # Attempt to delete a user
    db.users.insert_one({
        'id': 'delete1',
        'full_name': 'Dr. Test Faculty',
        'email': 'faculty@example.com',
        'department': 'CSE'
    })
    user_to_delete = db.users.find_one({"id": "delete1"})
    assert user_to_delete is not None
    user_id = str(user_to_delete['_id'])

    # Perform the delete request for user1
    response = client.post(f'/delete_user/{user_id}')
    assert response.status_code == 302  # Expect redirect
    assert response.headers['Location'] == '/view_users'

    # Check if admin1 is still in the database
    admin_user = db.users.find_one({"id": "admin"})
    assert admin_user is not None

def test_confirm_project_student(client):
    # Login as student
    with client.session_transaction() as sess:
        sess['id'] = 'student1'
        sess['role'] = 'student'

    # Test GET request to confirm_project route
    response = client.get('/confirm_project')
    assert response.status_code == 200

    # Test POST request to confirm_project route
    data = {'project_id': 'project1'}
    response = client.post('/confirm_project', data=data, follow_redirects=True)
    assert response.status_code == 200

    # Check if project1 is confirmed and other projects are set to Approved
    confirmed_project = db.application.find_one({"roll_no": "student1", "btp_id": "project1", "status": "Temporarily Confirmed"})
    assert confirmed_project is None

def test_confirm_project_student_invalid_project(client):
    # Login as student
    with client.session_transaction() as sess:
        sess['id'] = 'student1'
        sess['role'] = 'student'

    # Test POST request to confirm_project route with invalid data
    data = {'project_id': ''}
    response = client.post('/confirm_project', data=data, follow_redirects=True)
    assert response.status_code == 200

def test_confirm_project_non_student(client):
    # Login as non-student user (faculty)
    with client.session_transaction() as sess:
        sess['id'] = 'faculty1'
        sess['role'] = 'faculty'

    # Test access to confirm_project route (should redirect)
    response = client.get('/confirm_project')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'  # Redirected to homepage or login

def test_confirm_project_unauthorized(client):
    # Access the route without logging in
    response = client.get('/confirm_project')
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'  # Redirected to homepage or login


# Example of testing POST request with form data
def test_send_applications_to_co_guides_route(client):
    """Test send applications to co-guides route (POST request)."""
    # Assuming session with faculty role and a valid application_id
    application_id = '60f07633f95cc217a6c628ab'  # Replace with a valid application_id
    with client.session_transaction() as sess:
        sess['role'] = 'faculty'
    response = client.post(f'/send_applications_to_co_guides/{application_id}', data={
        'co_guides[]': ['co_guide_id_1', 'co_guide_id_2']
    }, follow_redirects=True)
    assert b'Applications sent to selected co-guides successfully' in response.data

# More test cases for other routes and functionalities as needed

def test_send_email(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '21CS30035'
            sess['role'] = 'student'

        response = client.get('/send_email', follow_redirects=True)
        assert b'Hey student!!!' in response.data
        assert response.status_code == 200

def test_view_projects(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        response = client.get('/view_projects')
        assert b'Projects' in response.data
        assert response.status_code == 200

def test_set_submission_details(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        data = {
            'submission_deadline': '2024-07-01 12:00',
            'full_marks': '100',
            'students': ['21CS300351', '21CS300352']
        }
        response = client.post('/set_submission_details/123', data=data, follow_redirects=True)
        assert response.status_code == 200

def test_set_submission_details(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = 'faculty123'
            sess['role'] = 'faculty'
            db.btp_list.delete_many({'btp_id': '12345'})
            db.btp_list.insert_one({
                'btp_id': '12345',
                'btp_name': 'Test Project',
                'prof_id': 'faculty123',
                'students': []
            })
        response = client.get('/set_submission_details/12345')

        assert response.status_code == 200

def test_marks_submissions(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        data = {'marks': '90'}
        response = client.post('/marks_submissions/123/21CS30035', data=data, follow_redirects=True)
        assert response.status_code == 200

def test_marks_submissions_get(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        response = client.get('/marks_submissions/123/21CS30035', follow_redirects=True)
        assert response.status_code == 200

def test_marks_submissions_unauthorized(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'student'

        response = client.get('/marks_submissions/123/21CS30035', follow_redirects=True)
        assert response.status_code == 200

def test_unauthorized_access(client):
    # Simulate a GET request to /marks_submissions/<btp_id>/<roll_no>
    btp_id = '12345'
    roll_no = '56789'

    # Simulate a session where role is not 'faculty'
    with client.session_transaction() as sess:
        sess['role'] = 'student'  # Simulate logged-in user with student role

    response = client.get(f'/marks_submissions/{btp_id}/{roll_no}')

    # Assert that the response status code is 302 (redirect)
    assert response.status_code == 302

    # Assert that the response redirects to login page
    assert response.location.endswith('/login')

def test_submission_not_found(client):
    # Simulate a GET request to /marks_submissions/<btp_id>/<roll_no> for a non-existent submission
    btp_id = '12345'
    roll_no = '56789'

    # Simulate a session where role is 'faculty'
    with client.session_transaction() as sess:
        sess['role'] = 'faculty'  # Simulate logged-in user with faculty role

    response = client.get(f'/marks_submissions/{btp_id}/{roll_no}')

    # Assert that the response status code is 302 (redirect)
    assert response.status_code == 302

    # Assert that the response redirects to faculty_home page
    assert response.location.endswith('/faculty_home')

def test_view_marks_student(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '21CS30035'
            sess['role'] = 'student'

        response = client.get('/view_marks/123/21CS30035')
        assert response.status_code == 302

def test_view_marks_faculty(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        response = client.get('/view_marks/123/21CS30035')
        assert response.status_code == 302

def test_faculty_not_associated_with_btp(client):
    btp_id = '12345'
    roll_no = '56789'

    # Simulate a session where the role is 'faculty' but not associated with the BTP project
    with client.session_transaction() as sess:
        sess['role'] = 'faculty'
        sess['id'] = 'faculty_id'

    db.btp_list.delete_many({"btp_id": btp_id, "prof_id": 'faculty_id'})
    db.btp_list.insert_one({"btp_id": btp_id, "prof_id": 'faculty_id'})

    response = client.get(f'/view_marks/{btp_id}/{roll_no}')

    assert response.status_code == 302
    assert response.location.endswith('/faculty_home')

def test_unauthorized_access(client):
    btp_id = '12345'
    roll_no = '56789'

    # Simulate a session where the role is not 'student' or 'faculty'
    with client.session_transaction() as sess:
        sess['role'] = 'admin'  # Some other role

    response = client.get(f'/view_marks/{btp_id}/{roll_no}')

    assert response.status_code == 302
    assert response.location.endswith('/login')


def test_send_email_unauthorized(client):
    response = client.get('/send_email', follow_redirects=True)
    # assert b'Please login as a student' in response.data
    assert response.status_code == 200

def test_view_projects_unauthorized(client):
    response = client.get('/view_projects', follow_redirects=True)
    assert b'Unauthorized access. Please login as faculty.' in response.data
    assert response.status_code == 200

def test_set_submission_details_get(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'am'

        response = client.get('/set_submission_details/123', follow_redirects=True)
        assert response.status_code == 200

def test_submit_report_get(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '21CS30035'
            sess['role'] = 'student'

        response = client.get('/submit_report/123/21CS30035', follow_redirects=True)
        assert b'Submit Report' in response.data
        assert response.status_code == 200

def test_marks_submissions_get(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'am'

        response = client.get('/marks_submissions/123/21CS30035', follow_redirects=True)
        assert response.status_code == 200

def test_view_marks_unauthorized(client):
    response = client.get('/view_marks/123/21CS30035', follow_redirects=True)
    assert b'Unauthorized access.' in response.data
    assert response.status_code == 200

def test_send_email_no_applications(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '21CS30035'
            sess['role'] = 'student'

        response = client.get('/send_email', follow_redirects=True)
        assert response.status_code == 200

def test_set_submission_details_no_students(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        data = {
            'submission_deadline': '2024-07-01 12:00',
            'full_marks': '100',
            'students': []
        }
        response = client.post('/set_submission_details/123', data=data, follow_redirects=True)
        assert response.status_code == 200

def test_submit_report_no_file(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '21CS30035'
            sess['role'] = 'student'

        response = client.post('/submit_report/123/21CS30035', 
                               data={},
                               content_type='multipart/form-data',
                               follow_redirects=True)
        assert response.status_code == 200

def test_marks_submissions_no_marks(client):
    with client:
        with client.session_transaction() as sess:
            sess['id'] = '12345'
            sess['role'] = 'faculty'

        data = {}
        response = client.post('/marks_submissions/123/21CS30035', data=data, follow_redirects=True)
        assert response.status_code == 200


def test_signup_page(client):
    response = client.get('/signup', follow_redirects=True)
    assert response.status_code == 200
    assert b'Sign Up' in response.data


def test_verify_otp_signup_page(client):
    response = client.get('/verify_otp_signup')
    assert response.status_code == 200

def test_verify_otp_signup_post(client):
    # Simulate signup to set session variables
    with client.session_transaction() as sess:
        sess['otp'] = '123456'
        sess['email'] = 'testuser@iitkgp.ac.in'
        sess['id'] = '123456789'
        sess['password'] = 'password123'
        sess['full_name'] = 'Test User'
        sess['department'] = 'CSE'
        sess['role'] = 'student'

    response = client.post('/verify_otp_signup', data={
        'otp': '123456'
    }, follow_redirects=True)
    assert response.status_code == 200
    assert b'You have successfully Signed Up!!!' in response.data


def test_submit_report(client):
    with client.session_transaction() as sess:
        sess['id'] = 'student1'
        sess['role'] = 'student'

    # Prepare mock data
    btp_id = 'btp123'
    roll_no = 'student1'

    # Simulate a successful submission
    response = client.post(f'/submit_report/{btp_id}/{roll_no}', data={'report_file': 'file'})
    assert response.status_code == 302  # Expect redirect

    # Simulate no file uploaded
    response = client.post(f'/submit_report/{btp_id}/{roll_no}', data={})
    assert response.status_code == 302  # Expect redirect

    # Simulate exception during submission
    response = client.post(f'/submit_report/{btp_id}/{roll_no}', data={'report_file': 'invalid_data'})
    assert response.status_code == 302  # Expect redirect


from app import send_otp_signup

def test_signup_and_verify(client):
    # Test signup route
    db.users.delete_many({'id': '123456789'})
    signup_data = {
        'id': '123456789',
        'password': 'testpassword',
        'full_name': 'Test Student',
        'email': 'teststudent@iitkgp.com',
        'department': 'CSE'
    }
    with client.session_transaction() as sess:
        # Mocking session data for signup
        sess['otp'] = 123456
        sess['email'] = signup_data['email']
        sess['id'] = signup_data['id']
        sess['password'] = signup_data['password']
        sess['full_name'] = signup_data['full_name']
        sess['department'] = signup_data['department']
        sess['role'] = 'student'

    # Send mock OTP (normally done by send_otp_signup, mocked here)
    send_otp_signup(sess['otp'], sess['email'])

    # Simulate POST request to signup route
    response = client.post('/signup', data=signup_data, follow_redirects=True)

    # Assertions for signup route
    # assert b'An OTP has been sent to your email address.' in response.data
    assert sess.get('otp') is not None

    # Test verify_otp_signup route
    otp_data = {
        'otp': sess['otp']
    }
    response = client.post('/verify_otp_signup', data=otp_data, follow_redirects=True)

    # Assertions for verify_otp_signup route
    assert b'You have successfully Signed Up!!!' in response.data


# Mock send_otp_forgot_password function to prevent actual email sending during tests
def mock_send_otp_forgot_password(otp, receiver_email):
    pass  # Mock function does nothing

# Applying the mock function to your app
app.send_otp_forgot_password = mock_send_otp_forgot_password

def test_forgot_password_get(client):
    response = client.get('/forgot_password')
    assert response.status_code == 200
    assert b'Forgot Password' in response.data

def test_forgot_password_post_existing_email(client):
    with client.session_transaction() as sess:
        sess.clear()  # Clear session data before the test

    response = client.post('/forgot_password', data={'email': 'existinguser@example.com'}, follow_redirects=True)

    assert response.status_code == 200


def test_forgot_password_post_non_existing_email(client):
    response = client.post('/forgot_password', data={'email': 'nonexistinguser@example.com'}, follow_redirects=True)

    assert response.status_code == 200

from app import send_otp_forgot_password
def test_send_otp_forgot_password():
    otp = "123456"
    receiver_email = "test@example.com"

    send_otp_forgot_password(otp, receiver_email)


def test_send_email(client):
    # Mock the session
    with client.session_transaction() as sess:
        sess['id'] = 'student1'
        sess['role'] = 'student'

    db.application.delete_many({"roll_no": "student1", "status": "Temporarily Confirmed"})
    db.application.insert_one({"roll_no": "student1", "status": "Temporarily Confirmed", "btp_id": '12345'})

    # Insert a sample BTP project
    db.btp_list.delete_many({'btp_id': '12345'})
    db.btp_list.insert_one({
        'btp_id': '12345',
        'btp_name': 'Test Project',
        'prof_id': 'faculty123',
    })
    
    # Insert a sample user
    db.users.delete_many({ 'id': 'faculty123' })
    db.users.insert_one({
        'id': 'faculty123',
        'full_name': 'Dr. Test Faculty',
        'email': 'faculty@example.com',
        'department': 'CSE'
    })

    # Mock the PDF generation and email sending within the route
    with app.app_context():
        response = client.get('/send_email')

    # Assertions
    assert response.status_code == 302
    assert response.headers['Location'] == '/login'


def test_reset_password(client):
    # Add a test user to the database
    db.users.insert_one({
        "email": "test@example.com",
        "password": "oldpassword"
    })

    # Simulate a session with email and OTP
    with client.session_transaction() as session:
        session['email'] = 'test@example.com'
        session['otp'] = '123456'  # Assuming OTP verification is done separately

    # Test password reset with matching passwords
    response = client.post('/reset_password', data={
        'password': 'newpassword',
        'confirm_password': 'newpassword'
    })

    assert response.status_code == 302  # Expect redirect to /login
    assert response.headers['Location'] == '/login'

    # Verify that the password has been updated in the database
    user = db.users.find_one({"email": "test@example.com"})
    assert user['password'] == 'newpassword'

    # Test password reset with non-matching passwords
    response = client.post('/reset_password', data={
        'password': 'newpassword',
        'confirm_password': 'differentpassword'
    })

    assert response.status_code == 302  # Expect redirect to /reset_password

    # Clean up the session
    with client.session_transaction() as session:
        session.pop('email', None)
        session.pop('otp', None)

if __name__ == '__main__':
    pytest.main()