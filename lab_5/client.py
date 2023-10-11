import base64
import json
import os
import socket
import threading

HOST = '127.0.0.1'
PORT = 12345
CLIENT_DIR_BASE = "CLIENT_MEDIA"
MAX_MESSAGE_SIZE = 2 ** 20
HELP_MSG = """
  /help - see existing commands
  /list - list available files on the server
  /download - download a file from the server
  /upload - upload a file to the server
  /exit - exit the program
"""

client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
client_socket.connect((HOST, PORT))
print(f"Client connected to {HOST}:{PORT}")

def connect():
  username = input("Enter username: ")
  room = input("Enter room: ")

  connect_message = {
    "message_type": "connect",
    "payload": {
      "name": username,
      "room": room
    }
  }

  client_socket.send(json.dumps(connect_message).encode('utf-8'))

  return username, room


def send_msg(text):
  message = {
    "message_type": "message",
    "payload": {
      "text": text
    }
  }
  client_socket.send(json.dumps(message).encode('utf-8'))

def send_file(path, name):
  with open(path, "rb") as file:
    content = base64.b64encode(file.read()).decode('utf-8')

  upload_file_message = {
    "message_type": "upload",
    "payload": {
      "file_name": name,
      "file_content": content,
    }
  }

  client_socket.send(json.dumps(upload_file_message).encode('utf-8'))

def download(payload, username):
  CLIENT_FILES_DIR = CLIENT_DIR_BASE + "_" + username

  name = payload.get("file_name")
  content = payload.get("file_content")

  if not os.path.exists(CLIENT_FILES_DIR):
    os.makedirs(CLIENT_FILES_DIR)

  with open(os.path.join(CLIENT_FILES_DIR, name), "wb") as file:
    file.write(base64.b64decode(content))

  print(f"\nFile {name} was downloaded successfully.")


def list_client_media(folder_path):
  files = []

  for filename in os.listdir(folder_path):
    if os.path.isfile(os.path.join(folder_path, filename)):
      files.append(filename)

  return files


def list_server_media(payload):
  server_media = payload.get("media", [])

  if server_media:
    print("\nAvailable server media:")

    for i, name in enumerate(server_media, start=1):
      print(f"{i}. {name}")
  else:
    print("\nNo files available on the server.")


def get_server_media():
  files_list_request = {
    "message_type": "server_media",
    "payload": {}
  }

  client_socket.send(json.dumps(files_list_request).encode('utf-8'))

def get_server_file(name):
  download_file_request = {
    "message_type": "download",
    "payload": {
      "file_name": name
    }
  }

  client_socket.send(json.dumps(download_file_request).encode('utf-8'))


def get_server_message(payload):
  message = payload.get("message")
  print(f"\n{message}")


def get_room_message(payload):
  message = payload.get("message")
  sender = payload.get("sender")
  print(f"\n{sender}: {message}")


def receive_messages():
  while True:
    message = client_socket.recv(MAX_MESSAGE_SIZE).decode('utf-8')

    if not message:
      break

    try:
      message_dict = json.loads(message)
      message_type = message_dict.get("message_type")
      payload = message_dict.get("payload")

      match message_type:
        case "connect_ack":
          get_server_message(payload)
        case "notification":
          get_server_message(payload)
        case "message":
          get_room_message(payload)
        case "file":
          download(payload, username)
        case "server_media":
          list_server_media(payload)

    except json.JSONDecodeError:
      print(f"\n{message}")

def upload():
  file_path = input("Enter the absolute path to the file to upload: ").replace("\"", "")

  if not os.path.isfile(file_path):
    print(f"No such file at {file_path}.")
    return
  
  try: 
    file_name = os.path.basename(file_path)
    send_file(file_path, file_name)
  except:
    print("An error occured during upload")

receive_thread = threading.Thread(target = receive_messages)
receive_thread.daemon = True
receive_thread.start()

username, room = connect()

print(HELP_MSG)

while True:
  text = input().strip().lower()

  match text:
    case '/help':
      print(HELP_MSG)
    case '/exit':
      break
    case '/upload':
      upload()
    case '/list':
      get_server_media()
    case '/download':
      file_name = input("Enter the name of the file to download: ")
      get_server_file(file_name)
    case default:
      send_msg(text)

client_socket.close()