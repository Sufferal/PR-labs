import socket
import json
from crud import CRUDCar

class Raft:
  def __init__(self, service_info, udp_host="127.0.0.1", udp_port=5000, udp_buffer_size=1024, 
               num_followers=2):
    self.udp_host = udp_host
    self.udp_port = udp_port
    self.udp_buffer_size = udp_buffer_size
    self.service_info = service_info
    self.min_num_msgs = num_followers * 2
    self.udp_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

    try:
      self.udp_socket.bind((self.udp_host, self.udp_port))
      print("Leader")
      self.role = "leader"
      self.followers = []

      msg_count = 0
      while msg_count < self.min_num_msgs:
        message, address = self.udp_socket.recvfrom(self.udp_buffer_size)
        
        if message.decode() == "Accept":
          data = json.dumps(self.service_info)
          msg_count += 1
          self.udp_socket.sendto(str.encode(data), address)
        else:
          message = message.decode()
          msg_count += 1
          follower_data = json.loads(message)
          print(f"Follower {int(msg_count/2)} data : ", follower_data)
          self.followers.append(follower_data)

    except Exception as e:
      print("Follower")
      self.role = "follower"
      self.leader_data = self.send_accept("Accept")
      print("Leader data: ", self.leader_data)
      self.send_accept(self.service_info)
      print("Follower data: ", self.service_info)
    finally:
      self.udp_socket.close()

  def send_accept(self, msg):
    if type(msg) is str:
      send_socket = socket.socket(family=socket.AF_INET, type=socket.SOCK_DGRAM)

      try:
        bytes_to_send = str.encode(msg)
        send_socket.sendto(bytes_to_send, (self.udp_host, self.udp_port))
        msg_from_server = send_socket.recvfrom(self.udp_buffer_size)[0]
        return json.loads(msg_from_server.decode())
      finally:
        send_socket.close()

    else:
      str_dict = json.dumps(msg)
      bytes_to_send = str.encode(str_dict)
      self.udp_socket.sendto(bytes_to_send, (self.udp_host, self.udp_port))

  def create_server(self):
    if self.role == "leader":
      return CRUDCar(True, self.followers)
    else:
      return CRUDCar(False)