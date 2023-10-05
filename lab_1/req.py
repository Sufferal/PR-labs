import requests

url = 'http://localhost:5000/hello' 
payload = {'id': '1', 'name': 'John Doe'}
response = requests.post(url, json=payload)
print(response.text)
