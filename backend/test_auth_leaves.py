import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000/api"

def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def test_auth_leaves():
    print("Testing HRMS Auth & Leaves...")

    # 1. Register
    username = f"user_{random_string()}"
    password = "testpassword123"
    email = f"{username}@example.com"
    first_name = f"Test User {random_string()}"
    
    reg_data = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "department": "IT",
        "employee_id": f"EMP-{random_string()}" # Actually RegisterSerializer generates this? No, serializer expects it or generates? 
        # Checking serializer: RegisterSerializer in employees/serializers.py expects 'username', 'password', 'email', 'first_name', 'department'. 
        # And inside create(), it generates employee_id from username.upper().
        # Wait, the RegisterSerializer I wrote in step 621 line 30 uses `validated_data.get('username').upper()`.
        # So I don't need to send employee_id.
    }
    
    # Adjust reg_data to match serializer
    reg_data_payload = {
        "username": username,
        "password": password,
        "email": email,
        "first_name": first_name,
        "department": "IT"
    }

    print(f"Registering user: {username}")
    response = requests.post(f"{BASE_URL}/auth/register/", json=reg_data_payload)
    if response.status_code == 201:
        print("Registration Successful")
    else:
        print(f"Registration Failed: {response.text}")
        exit(1)

    # 2. Login
    print("Logging in...")
    login_data = {
        "username": username,
        "password": password
    }
    response = requests.post(f"{BASE_URL}/token/", json=login_data)
    if response.status_code == 200:
        tokens = response.json()
        access_token = tokens['access']
        print("Login Successful. Token received.")
    else:
        print(f"Login Failed: {response.text}")
        exit(1)

    headers = {
        "Authorization": f"Bearer {access_token}"
    }

    # 3. Apply for Leave
    print("Applying for Leave...")
    leave_data = {
        "start_date": "2023-11-01",
        "end_date": "2023-11-02",
        "reason": "Sick Leave"
    }
    response = requests.post(f"{BASE_URL}/leaves/", json=leave_data, headers=headers)
    if response.status_code == 201:
        print(f"Leave Applied: {response.json()['status']}")
        leave_id = response.json()['id']
    else:
        print(f"Leave Application Failed: {response.text}")
        exit(1)

    # 4. List Leaves
    print("Listing Leaves...")
    response = requests.get(f"{BASE_URL}/leaves/", headers=headers)
    leaves = response.json()
    print(f"Total Leaves: {len(leaves)}")
    if any(l['id'] == leave_id for l in leaves):
        print("Leave verification: PASS")
    else:
        print("Leave verification: FAIL")

    # 5. Mark Attendance (Self)
    print("Marking Attendance...")
    att_data = {
        "date": "2023-11-01",
        "status": "Present"
        # Employee field should be auto-filled by backend
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=att_data, headers=headers)
    if response.status_code == 201:
        print("Attendance Marked Successfully")
    else:
        print(f"Attendance Failed: {response.text}")
        # It might fail if I didn't fix the view correctly or migrations didn't run.

if __name__ == "__main__":
    test_auth_leaves()
