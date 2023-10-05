import socket
import sys
import signal
import threading
import json
import re

HOST = '127.0.0.1'
PORT = 8080
IS_RUNNING = True

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind((HOST, PORT))
server_socket.listen(5)
print(f"Server is listening on {HOST}:{PORT}")

def signal_handler(sig, frame):
  global IS_RUNNING
  print("\nShutting down the server...")
  server_socket.close()
  IS_RUNNING = False
  sys.exit(0)

def handle_request(client_socket):
  # Receive and print the client's request data 
  request_data = client_socket.recv(1024).decode('utf-8')
  print(f"Received Request:\n{request_data}")

  # Parse the request to get the HTTP method and path
  request_lines = request_data.split('\n')
  request_line = request_lines[0].strip().split()
  method = request_line[0]
  path = request_line[1]

  response_body = ""
  status_code = 200

  # Prepare and send appropriate HTTP response
  f = open('product_input.json')
  data = json.load(f)

  if path == '/':
    response_body = "<h1>Home Page</h1>"
  elif path == '/about':
    response_body = "<h1>About Page</h1>"
  elif path == '/contact':
    response_body = "<h1>Contact Page</h1>"
  elif path == '/products':
    response_body = "<h1>Products Page</h1>"
    for i in data:
      id = i['id']
      response_body += f'<a href="product/{id}">Product {id}</a> <br>'
  elif path.startswith('/product/'):
    product_url_id = path.split('/')[-1]

    if re.match(r'^[1-9][0-9]*$', product_url_id):
      product_url_id = int(product_url_id)

      for product in data:
        if product and product['id'] == product_url_id:
          response_body = f"<h1>Product Details</h1>"
          response_body += f"<p>ID: { product['id'] }</p>"
          response_body += f"<p>Name: { product['name'] }</p>"
          response_body += f"<p>Author: { product['author'] }</p>"
          response_body += f"<p>Price: { product['price'] }</p>"
          response_body += f"<p>Description: { product['description'] }</p>"

  else:
    response_body = "<h1>Error 404: Page not found</h1>"
    status_code = 404

  # Send HTTP response
  response = f"HTTP/1.1 {status_code} OK\nContent-Type: text/html\n\n{response_body}"
  client_socket.sendall(response.encode('utf-8'))

  client_socket.close()

def main():
  signal.signal(signal.SIGINT, signal_handler)
  
  while IS_RUNNING:
    # Accept incoming connection
    client_socket, client_address = server_socket.accept()
    print(f"Accepted connection from {client_address[0]}:{client_address[1]}")

    # Create a thread to handle the client's request
    client_handler = threading.Thread(target=handle_request, args=(client_socket,))
    client_handler.start()

if __name__ == "__main__":
  main()