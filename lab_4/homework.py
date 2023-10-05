import requests
import json
import re
from bs4 import BeautifulSoup

WEB_SERVER_URL = 'http://127.0.0.1:8080'

def parse_simple_pages():
  simple_pages = ['/', '/about', '/contact', '/products']
  page_contents = {}

  for page in simple_pages:
    response = requests.get(WEB_SERVER_URL + page)
    if response.status_code == 200:
      page_contents[page] = response.text

  return page_contents

def parse_product_pages():
  product_pages = []
  product_arr = []

  response = requests.get(WEB_SERVER_URL + '/products')
  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')

    product_links = soup.find_all('a')
    for link in product_links:
      product_pages.append("/" + link['href'])

    for product_page in product_pages:
      response = requests.get(WEB_SERVER_URL + product_page)

      if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')

        product_id = int(product_page.split('/')[-1])
        product_name = soup.find('p', string = re.compile(r'^Name:')).text.split(': ')[-1]
        product_author = soup.find('p', string = re.compile(r'^Author:')).text.split(': ')[-1]
        product_price = soup.find('p', string = re.compile(r'^Price:')).text.split(': ')[-1]
        product_description = soup.find('p', string = re.compile(r'^Description:')).text.split(': ')[-1]

        product_arr.append({
          'id': product_id,
          'name': product_name,
          'author': product_author,
          'price': float(product_price),
          'description': product_description
        })

  return product_arr

def main():
  simple_page_contents = parse_simple_pages()

  print("\nContent of simple pages: ")
  for page in simple_page_contents:
    print(page, ": ", simple_page_contents[page])

  product_arr = parse_product_pages()
  print("\nProducts: ")
  for product in product_arr:
    print(product)
 
  with open('product_output.json', 'w') as file:
    json.dump(product_arr, file, indent = 2)

if __name__ == "__main__":
  main()
