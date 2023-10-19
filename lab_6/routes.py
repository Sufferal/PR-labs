from flask import request, jsonify
from models.database import db
from models.car import Car
from __main__ import app

@app.route('/api/cars', methods=['GET'])  
def get_all_cars():
  cars = Car.query.all()
  car_list = []

  for car in cars:
    car_list.append({
      'id': car.id,
      'name': car.name,
      'year': car.year
    })

  return jsonify(car_list), 200

@app.route('/api/car/<int:car_id>', methods=['GET'])
def get_car_by_id(car_id):
  car = Car.query.get(car_id)

  if car is not None:
    return jsonify({
      'id': car.id,
      'name': car.name,
      'year': car.year
    }), 200
  else:
    return jsonify({
      'message': 'Car not found.'
    }), 404

@app.route('/api/cars', methods=['POST'])
def create_car():
  try: 
    data = request.get_json()
    name = data['name']
    year = data['year']
    car = Car(name, year)

    db.session.add(car)
    db.session.commit()

    return jsonify({
      'message': 'Successfully created car.'
    }), 201
  except KeyError:
    return jsonify({
      'message': 'Invalid request parameters.'
    }), 400
  
@app.route('/api/car/<int:car_id>', methods=['PUT'])
def update_car(car_id):
  try:
    car = Car.query.get(car_id)

    if car is not None:
      data = request.get_json()

      car.name = data.get('name', car.name)
      car.year = data.get('year', car.year)

      db.session.commit()
      return jsonify({
        'message': 'Successfully updated car.'
      }), 200
    else:
      return jsonify({
        'message': 'Car not found.'
      }), 404
  except Exception as e:
    return jsonify({
      'message': 'Something went wrong. Error: ' + str(e)
    }), 500
  
@app.route('/api/car/<int:car_id>', methods=['DELETE'])
def delete_car(car_id):
  try:
    car = Car.query.get(car_id)

    if car is not None:
      password = request.headers.get('X-Delete-Password')

      if password == 'admin':
        db.session.delete(car)
        db.session.commit()

        return jsonify({ 'message': 'Successfully deleted car.'}), 200
      else:
        return jsonify({'message': 'Incorrect password.'}), 401
    else:
      return jsonify({ 'message': 'Car not found.'}), 404

  except Exception as e:
    return jsonify({
      'message': 'Something went wrong. Error: ' + str(e)
    }), 500