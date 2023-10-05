from flask import Flask, request

app = Flask(__name__)

@app.route('/hello', methods=['GET', 'POST'])
def index():  
  if request.method == 'GET':
    return {'message': 'Hello, World!'}
  elif request.method == 'POST':
    payload = request.get_json()
    for key, value in payload.items():
      print(f'{key}: {value}')
    return "congrats!"

app.run()