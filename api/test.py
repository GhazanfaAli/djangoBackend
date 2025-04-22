import requests

url = "http://http://10.11.112.123/:8000/api/user/all-users/"
headers = {
    "Authorization": "Bearer eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoiYWNjZXNzIiwiZXhwIjoxNzQ0MDMzNjE0LCJpYXQiOjE3NDQwMzEyMTQsImp0aSI6IjgwY2I2ZWJiODk4NDQ3ZTQ4OTYyM2NiZjE4NzYyYWFiIiwidXNlcl9pZCI6NDZ9.22K_sD7pk3cDprOqnKAzDyJK0UysP0DyvIeHPNJnBm4",
    "Accept": "application/json",
}
response = requests.get(url, headers=headers)
print(response.json())