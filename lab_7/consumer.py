import pika
import requests
from threading import Thread, Lock
from bs4 import BeautifulSoup
from tinydb import TinyDB

db = TinyDB('books.json')  
db_lock = Lock()

def process_queue(thread_num):
  connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
  channel = connection.channel()
  channel.queue_declare(queue='books')

  print(f'Thread {thread_num}: Waiting for messages. To exit, press CTRL+C')

  def callback(ch, method, properties, body):
    print(f'Thread {thread_num}: Received {body}')
    response = requests.get(body)

    if response.status_code != 200:
      print(f"Thread {thread_num}: [Error]: Unable to fetch data from the URL: {body}")
      ch.basic_ack(delivery_tag=method.delivery_tag)
      return

    try:
      soup = BeautifulSoup(response.text, 'html.parser')
      title = soup.find("h1", class_="main-title").text.strip()
      details = soup.find_all("div", class_="book-prop-name")
      values = soup.find_all("div", class_="book-prop-value")

      book = {"title": title}

      # Add the rest of the details
      for i in range(len(details)):
        book[details[i].text.strip()] = values[i].text.strip()

      with db_lock:
        db.insert(book)
    except Exception as e:
      print(f"Thread {thread_num}: [Error]: Unable to parse data from the URL: {body}")
      print(f"Thread {thread_num}: Exception: {e}")

    print(f"Thread {thread_num}: Done processing {body}")
    ch.basic_ack(delivery_tag=method.delivery_tag)

  try:
    while True:
      method_frame, _, body = channel.basic_get(queue='books')

      if body is None:
        print(f"Thread {thread_num}: No more messages in the queue. Exiting...")
        break

      callback(channel, method_frame, None, body)
  finally:
    connection.close()

def main():
  num_threads = 5

  # Create and start threads
  threads = []
  for i in range(num_threads):
    t = Thread(target=process_queue, args=(i,))
    threads.append(t)
    t.start()

  # Wait for the threads to complete
  for t in threads:
    t.join()

  print("All threads have finished")

  # Print the contents of the database
  for i in db.all():
    print(i)

if __name__ == "__main__":
  main()
