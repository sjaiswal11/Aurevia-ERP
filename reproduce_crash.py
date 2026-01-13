import requests
import sys

# Setup session
s = requests.Session()
base_url = "http://localhost:8000"

# 1. Get login page to get CSRF token
login_url = f"{base_url}/admin/login/"
try:
    r = s.get(login_url)
    print(f"Login Page Status: {r.status_code}")
    csrf_token = s.cookies['csrftoken']
except Exception as e:
    print(f"Failed to fetch login page: {e}")
    sys.exit(1)

# 2. Login
login_data = {
    'username': 'admin',
    'password': 'admin',
    'csrfmiddlewaretoken': csrf_token,
    'next': '/'
}
headers = {'Referer': login_url}

try:
    r = s.post(login_url, data=login_data, headers=headers)
    print(f"Login Post Status: {r.status_code}")
    print(f"Login Post URL: {r.url}") # Where did we end up?
except Exception as e:
    print(f"Failed to login: {e}")
    sys.exit(1)

# 3. Request Root URL
try:
    r = s.get(base_url)
    print(f"Root URL Status: {r.status_code}")
    print(f"Root URL Content Snippet: {r.text[:200]}")
except Exception as e:
    print(f"Failed to fetch root: {e}")
