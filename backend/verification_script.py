import requests
import json

BASE_URL = "http://127.0.0.1:8000/api"

def test_api():
    print("Testing HRMS API...")

    # 1. Create Employee
    emp_data = {
        "employee_id": "EMP001",
        "name": "John Doe",
        "email": "john@example.com",
        "department": "IT"
    }
    response = requests.post(f"{BASE_URL}/employees/", json=emp_data)
    print(f"Create Employee: {response.status_code}")
    if response.status_code == 201:
        print(response.json())
    else:
        print(response.text)

    # 2. List Employees
    response = requests.get(f"{BASE_URL}/employees/")
    print(f"List Employees: {response.status_code}")
    print(response.json())

    # 3. Mark Attendance
    att_data = {
        "employee": "EMP001",
        "date": "2023-10-27",
        "status": "Present"
    }
    response = requests.post(f"{BASE_URL}/attendance/", json=att_data)
    print(f"Mark Attendance: {response.status_code}")
    if response.status_code == 201:
        print(response.json())
    else:
        print(response.text)

    # 4. Filter Attendance
    response = requests.get(f"{BASE_URL}/attendance/?employee_id=EMP001")
    print(f"Filter Attendance: {response.status_code}")
    print(response.json())

    # 5. Duplicate Attendance Check
    response = requests.post(f"{BASE_URL}/attendance/", json=att_data)
    print(f"Duplicate Attendance: {response.status_code}") # Should be 400
    print(response.text)

if __name__ == "__main__":
    try:
        test_api()
    except Exception as e:
        print(f"Error: {e}")
