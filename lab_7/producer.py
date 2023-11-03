import requests
import re
from bs4 import BeautifulSoup
import pika

connection = pika.BlockingConnection(pika.ConnectionParameters('localhost'))
channel = connection.channel()
channel.queue_declare(queue = 'books')

def get_max_num_pages(url):
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", class_ = "page-link")
    last_page_link = links[-1]

    pattern = r'(\d+)'
    match = re.search(pattern, str(last_page_link))

    if match:
      number = match.group(1)
      number = int(number)
      return number
  
  return None

def scrape_page_recursive(url, max_num_pages, current_page = 1):
  absolute_urls = set()

  # Base case
  if current_page > max_num_pages:
    return list(absolute_urls)
  
  full_url = f"{url}/page/{current_page}"
  response = requests.get(full_url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", class_="book-card-img-link")

    for i, link in enumerate(links):
      href = link.get('href')

      if href:
        absolute_url = href
        print(f"Page {current_page}, index {i}:", absolute_url)
        channel.basic_publish(exchange='', routing_key='books', body=absolute_url)
        absolute_urls.add(absolute_url)
      
    next_page_urls = scrape_page_recursive(url, max_num_pages, current_page + 1)
    absolute_urls.update(next_page_urls)
  else:
    print(f"An error occurred during the request for page {current_page}. Status code: {response.status_code}")

  return list(absolute_urls)

def urls_to_txt(urls):
  with open("books.txt", "w") as file:
    for url in urls:
      file.write(url + "\n")

if __name__ == "__main__":
  url = "https://librarius.md/ro/books"
  max_num_pages = 2
  absolute_urls = scrape_page_recursive(url, max_num_pages)
  urls_to_txt(absolute_urls)
  connection.close()