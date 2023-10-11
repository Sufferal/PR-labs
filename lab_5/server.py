import base64
import json
import os
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
MAX_MESSAGE_SIZE = 2 ** 20
SERVER_FILES_DIR = "SERVER_MEDIA"
MEMBERS = {}
ROOMS = {}
CLIENTS = {}

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server_socket.bind((HOST, PORT))
server_socket.listen()
print(f"Server is listening on {HOST}:{PORT}")

def list_server_media(client_socket):
  if not os.path.exists(SERVER_FILES_DIR):
    os.makedirs(SERVER_FILES_DIR)

  room_name = CLIENTS.get(client_socket)
  room_dir = os.path.join(SERVER_FILES_DIR, room_name)

  files = []

  if os.path.exists(room_dir):
    for filename in os.listdir(room_dir):
      if os.path.isfile(os.path.join(room_dir, filename)):
        files.append(filename)

  return files

def upload(payload, client_socket):
  file_name = payload.get("file_name")
  room_name = CLIENTS.get(client_socket)
  file_content = payload.get("file_content")
  sender = MEMBERS[client_socket]

  if not room_name:
    return

  if not os.path.exists(SERVER_FILES_DIR):
    os.makedirs(SERVER_FILES_DIR)

  room_dir = os.path.join(SERVER_FILES_DIR, room_name)

  if not os.path.exists(room_dir):
    os.makedirs(room_dir)

  with open(os.path.join(room_dir, file_name), "wb") as file:
    file.write(base64.b64decode(file_content))

  message_user = f"{sender} uploaded the {file_name} file."
  if room_name in ROOMS:
    for client in ROOMS[room_name]:
      if client != client_socket:
        client.send(message_user.encode('utf-8'))


def send_file(file_name, file_content, client_socket):
  file_message = {
    "message_type": "file",
    "payload": {
      "file_name": file_name,
      "file_content": file_content,
    }
  }
  client_socket.send(json.dumps(file_message).encode('utf-8'))

def download(payload, client_socket):
  if not os.path.exists(SERVER_FILES_DIR):
    os.makedirs(SERVER_FILES_DIR)

  room_name = CLIENTS.get(client_socket)

  if not room_name:
    return

  file_name = payload.get("file_name")
  room_dir = os.path.join(SERVER_FILES_DIR, room_name)

  if os.path.exists(os.path.join(room_dir, file_name)):
    with open(os.path.join(room_dir, file_name), "rb") as file:
      file_content = base64.b64encode(file.read()).decode('utf-8')
      send_file(file_name, file_content, client_socket)
  else:
    client_socket.send("File not found".encode('utf-8'))


def server_media(client_socket):
  server_media = list_server_media(client_socket)

  if not server_media or len(server_media) == 0:
    client_socket.send("There are no files on the server media.".encode('utf-8'))
    return

  files_list_message = {
    "message_type": "server_media",
    "payload": {
      "media": server_media
    }
  }

  client_socket.send(json.dumps(files_list_message).encode('utf-8'))

def send_message(payload, client_socket):
  text = payload.get("text")
  room = CLIENTS.get(client_socket)
  sender = MEMBERS[client_socket]

  message = {
    "message_type": "message",
    "payload": {
      "sender": sender,
      "room": room,
      "message": text
    }
  }

  if room in ROOMS:
    for client in ROOMS[room]:
      if client != client_socket:
        client.send(json.dumps(message).encode('utf-8'))


def member_join(payload, client_socket):
  client_name = payload.get("name")
  room_name = payload.get("room")

  if room_name not in ROOMS:
    ROOMS[room_name] = []

  ROOMS[room_name].append(client_socket)
  CLIENTS[client_socket] = room_name
  MEMBERS[client_socket] = client_name

  notification_message = f"{client_name} has joined the room."
  for client in ROOMS[room_name]:
    if client != client_socket:
      notification(client, notification_message)

def notification(client_socket, notification_message):
  notification = {
    "message_type": "notification",
    "payload": {
      "message": notification_message
    }
  }
  client_socket.send(json.dumps(notification).encode('utf-8'))


def handle_client(client_socket, client_address):
  print(f"Accepted connection from {client_address}")

  try:
    while True:
      message = client_socket.recv(MAX_MESSAGE_SIZE).decode('utf-8')

      if not message:
        break

      print(f"Received from {client_address}: {message}")

      try:
        message_dict = json.loads(message)
        message_type = message_dict.get("message_type")
        payload = message_dict.get("payload")

        match message_type:
          case "connect":
            member_join(payload, client_socket)
          case "message":
            send_message(payload, client_socket)
          case "upload":
            upload(payload, client_socket)
          case "download":
            download(payload, client_socket)
          case "server_media":
            server_media(client_socket)

      except json.JSONDecodeError:
        print(f"Error decoding message from {client_address}")

  except Exception as e:
    print(f"Error handling client {client_address}: {e}")

  finally:
    room_name = CLIENTS.get(client_socket)

    if room_name:
      ROOMS[room_name].remove(client_socket)

      username = MEMBERS[client_socket]
      notification_message = f"{username} has left the room."

      del CLIENTS[client_socket]
      del MEMBERS[client_socket]

      for client in ROOMS[room_name]:
        notification(client, notification_message)

    client_socket.close()


while True:
  client_socket, client_address = server_socket.accept()
  CLIENTS[client_socket] = None
  client_thread = threading.Thread(target = handle_client, args = (client_socket, client_address))
  client_thread.start()