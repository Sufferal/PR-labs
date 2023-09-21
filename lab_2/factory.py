from datetime import datetime
from player import Player
import xml.etree.ElementTree as ET
import player_pb2

class PlayerFactory:
  def to_json(self, players):
    player_arr = []

    for player in players:
      player_json = {
        "nickname": player.nickname,
        "email": player.email,
        # returns a string representing date and time using date, time or datetime object.
        "date_of_birth": player.date_of_birth.strftime('%Y-%m-%d'),
        "xp": player.xp,
        "class": player.cls
      }
      player_arr.append(player_json)

    return player_arr

  def from_json(self, list_of_dict):
    player_arr = []

    for player_info in list_of_dict:
      player = Player(
        nickname = player_info["nickname"],
        email = player_info["email"],
        date_of_birth = player_info["date_of_birth"],
        xp = player_info["xp"],
        cls = player_info["class"]
      )
      player_arr.append(player)

    return player_arr


  def to_xml(self, list_of_players):
    root = ET.Element('data')

    for player in list_of_players:
      player_el = ET.SubElement(root, 'player')
      ET.SubElement(player_el, 'nickname').text      = player.nickname
      ET.SubElement(player_el, 'email').text         = player.email
      ET.SubElement(player_el, 'date_of_birth').text = player.date_of_birth.strftime('%Y-%m-%d')
      ET.SubElement(player_el, 'xp').text            = str(player.xp)
      ET.SubElement(player_el, 'class').text         = player.cls

    return ET.tostring(root, encoding='utf8').decode('utf8')

  def from_xml(self, xml_string):
    players_arr = []
    root = ET.fromstring(xml_string)
    
    for player_el in root.findall('player'):
      nickname          = player_el.find('nickname').text
      email             = player_el.find('email').text
      date_of_birth_str = player_el.find('date_of_birth').text  
      xp                = int(player_el.find('xp').text)
      player_class      = player_el.find('class').text
      player            = Player(nickname, email, date_of_birth_str, xp, player_class)  
      players_arr.append(player)

    return players_arr

  def to_protobuf(self, list_of_players):
    players_list = player_pb2.PlayersList()  

    for player in list_of_players:
      player_msg               = players_list.player.add()  
      player_msg.nickname      = player.nickname
      player_msg.email         = player.email
      player_msg.date_of_birth = player.date_of_birth.strftime('%Y-%m-%d')
      player_msg.xp            = player.xp
      player_msg.cls           = player.cls

    return players_list.SerializeToString()

  def from_protobuf(self, binary):
    players_list = player_pb2.PlayersList()
    players_list.ParseFromString(binary)

    players_arr = []

    for player_msg in players_list.player:
      nickname      = player_msg.nickname
      email         = player_msg.email
      date_of_birth = player_msg.date_of_birth
      xp            = player_msg.xp
      # Convert enum to string
      cls           = player_pb2.Class.Name(player_msg.cls) 

      player = Player(nickname, email, date_of_birth, xp, cls)
      players_arr.append(player)

    return players_arr




