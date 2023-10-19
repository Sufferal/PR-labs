from app import create_app, db, Car

def init_database():
  app = create_app()

  with app.app_context():
    # Create the database tables
    db.create_all()

    # Insert data into database tables
    car1 = Car('Toyota', 2009)
    car2 = Car('Honda', 2010)
    car3 = Car('BMW', 2011)
  
    db.session.add(car1)
    db.session.add(car2)
    db.session.add(car3)

    db.session.commit()

if __name__ == '__main__':
  init_database()