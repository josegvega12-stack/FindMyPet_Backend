import requests

# 👉 Aquí vas a pegar tu token SIN comillas
TOKEN = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VyX2lkIjoiNjkxNGM2NWQ1NTk1MDYyZWEzZmZjMWRjIiwiZW1haWwiOiJqb3NldmVnYTNAdGVzdC5jb20iLCJleHAiOjE3NjMwODIyNzl9.lKhE3y-IdCeCe9jki8e8tTNQJ0YOmryhTeKE1pXbedE"


url = "http://127.0.0.1:8000/api/users/me"

headers = {
    "accept": "application/json",
    "Authorization": f"Bearer {TOKEN}",
}

response = requests.get(url, headers=headers)

print("Status:", response.status_code)
print("Body:", response.text)
