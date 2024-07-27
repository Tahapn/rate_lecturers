import requests
data = {
    'username': 'admin1',
    'password': 'fdsa'
}
response = requests.post('http://127.0.0.1:8000/user/api/token', data=data)

print(response.status_code)
print(response.json)
