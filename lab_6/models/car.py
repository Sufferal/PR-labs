from models.database import db

class Car(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  name = db.Column(db.String(100), nullable=False)
  year = db.Column(db.Integer, nullable=False)

  def __init__(self, name, year):
    self.name = name
    self.year = year
    