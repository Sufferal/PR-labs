import requests

class CRUDCar:
  def __init__(self, leader: bool, followers: dict = None):
    self.leader = leader
    if self.leader:
      self.followers = followers

  def create_car(self, car: dict):
    if self.leader:
      for follower in self.followers:
        requests.post(f"http://{follower['host']}:{follower['port']}/api/cars",
                              json = car,
                              headers = {"Token" : "Leader"})
    else:
      return {"message": "Only the leader can perform this operation."}, 403
    
  def update_car(self, car: dict, index: str):
    if self.leader:
      for follower in self.followers:
        requests.put(f"http://{follower['host']}:{follower['port']}/api/car/{index}",
                              json = car,
                              headers = {"Token" : "Leader"})
    else:
      return {"message": "Only the leader can perform this operation."}, 403

  def delete_car(self, index: str):
    if self.leader:
      for follower in self.followers:
        requests.delete(f"http://{follower['host']}:{follower['port']}/api/car/{index}",
                          headers={"Token": "Leader", "X-Delete-Password": "admin"})
    else:
      return {"message": "Only the leader can perform this operation."}, 403
