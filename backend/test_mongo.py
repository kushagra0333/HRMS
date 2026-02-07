import requests
import random
import string

BASE_URL = "http://127.0.0.1:8000/api"

def random_string(length=6):
    return ''.join(random.choices(string.ascii_uppercase + string.digits, k=length))

def test_api():
    print("Testing HRMS API with MongoDB...")

    # 1. Create Employee
    emp_id = f"EMP-{random_string()}"
    email = f"user-{random_string()}@example.com"
    emp_data = {
        "employee_id": emp_id,
        "name": f"Test User {random_string()}",
        "email": email,
        "department": "IT"
    }
    
    try:
        response = requests.post(f"{BASE_URL}/employees/", json=emp_data, timeout=5)
        print(f"Create Employee: {response.status_code}")
        if response.status_code == 201:
            created_emp = response.json()
            print("Response:", created_emp)
        else:
            print("Error:", response.text)
            exit(1)
            
        # 2. List Employees
        response = requests.get(f"{BASE_URL}/employees/", timeout=5)
        print(f"List Employees: {response.status_code}")
        employees = response.json()
        print(f"Total Employees: {len(employees)}")
        
        # Verify created employee is in list
        found = any(e['employee_id'] == emp_id for e in employees)
        print(f"Verify Created Employee in List: {'PASS' if found else 'FAIL'}")

        # 3. Mark Attendance
        att_data = {
            "employee": emp_id, # Uses SlugRelatedField? Or PK?
            # Wait, our model uses employee_id (str) as PK if configured?
            # No, default AutoField/BigAutoField is PK.
            # But detailed view might use employee_id lookup?
            # Let's check serializer.
            "date": "2023-10-27",
            "status": "Present"
        }
        
        # If serializer expects PK (id), we need to get ID from response
        # Checking implementation: EmployeeSerializer uses `employee_id` field?
        # Actually standard SlugRelatedField usually needs slug_field.
        # But if we use employee_id string in request, backend needs to resolve it.
        # Assumption: Employee model has `employee_id` field, and Attendance has `employee` FK.
        # DRF default FK serializer expects PK (integer ID).
        # But in MongoDB it might be ObjectId or Int.
        
        # Let's inspect the `response.json()` from create.
        # created_emp already set above
        emp_pk = created_emp['employee_id']
        att_data['employee'] = emp_pk 

        response = requests.post(f"{BASE_URL}/attendance/", json=att_data, timeout=5)
        print(f"Mark Attendance: {response.status_code}")
        print(response.text)

    except Exception as e:
        print(f"Test Failed: {e}")
        exit(1)

if __name__ == "__main__":
    test_api()
