import requests

def get_user_directory(url):
    try:
        # Fetch data with an explicit timeout of 5 seconds
        response = requests.get(url, timeout=5)
        response.raise_for_status()  # Check for 4xx/5xx errors
        
        # Parse JSON and extract users safely
        return response.json().get("users", [])
        
    except requests.exceptions.RequestException as e:
        print(f"❌ API Request Failed: {e}")
        return []

# Test endpoint
api_url = "https://dummyjson.com/users?limit=10"
users = get_user_directory(api_url)

# Format and print the table
if users:
    print(f"{'ID':<4} | {'Name':<20} | {'Email':<30} | {'Age':<3}")
    print("-" * 65)
    for u in users:
        # Combine names and fetch keys safely using .get()
        fullname = f"{u.get('firstName', '')} {u.get('lastName', '')}"
        print(f"{u.get('id', ''):<4} | {fullname:<20} | {u.get('email', ''):<30} | {u.get('age', ''):<3}")
else:
    print("No users found.")
