import requests, json
from bs4 import BeautifulSoup

def url_to_json(url):
  response = requests.get(url)
    
  if response.status_code != 200:
    print(f"[Error]: Unable to fetch data from the url: {url}")

  try:
    soup = BeautifulSoup(response.text, 'html.parser')
    
    title = soup.find("h1", itemprop = "name").text.strip()
    price = soup.find("span", class_ = "adPage__content__price-feature__prices__price__value").text.strip()

    currency = ""
    currency_elem = soup.find("span", class_ = "adPage__content__price-feature__prices__price__currency")
    if currency_elem is not None:
      currency = currency_elem.text.strip()

    region = soup.find("span", class_ = "adPage__aside__address-feature__text").text.strip()
    author = soup.find("a", class_ = "adPage__aside__stats__owner__login").text.strip()

    description = ""
    description = soup.find("div", class_ = "adPage__content__description grid_18", itemprop="description")
    if description is not None:
      description = description.text.strip()

    last_updated = soup.find("div", class_ = "adPage__aside__stats__date").text.strip().split(": ")[1]
    ad_type = soup.find("div", class_ = "adPage__aside__stats__type").text.strip().split(": ")[1]
    views = soup.find("div", class_ = "adPage__aside__stats__views").text.strip()
    views = int(views.split(": ")[1].replace(" ", "").split("(", 1)[0])
    
    characteristics = {}
    char_elements = soup.find_all("li", class_ = "m-value", itemprop = "additionalProperty")
    for element in char_elements:
      key = element.find("span", class_ = "adPage__content__features__key").text.strip()
      value = element.find("span", class_ = "adPage__content__features__value").text.strip()
      characteristics[key] = value
    
    additional = []
    additional_elements = soup.find_all("li", class_ = "m-no_value", itemprop = "additionalProperty")
    for element in additional_elements:
      key = element.find("span", class_ = "adPage__content__features__key").text.strip()
      additional.append(key)
    
    apart_data = {
      "url": url,
      "title": title,
      "price": price,
      "currency": currency,
      "region": region,
      "author": author,
      "description": description,
      "last updated": last_updated,
      "type": ad_type,
      "views": views,
      "characteristics": characteristics,
      "additional": additional
    }
    
    return apart_data
  
  except Exception as e:
    print(f"[Error]: An error occurred while processing the URL: {url}. Error: {str(e)}")
    return None

def get_apart_data():
  with open("apartments.txt", "r") as file:
    urls = [line.strip() for line in file]

  json_data_list = []

  for index, url in enumerate(urls, start = 1):
    print(f"Fetching data for URL {index} / {len(urls)}: {url}")
    json_data = url_to_json(url)
    if json_data:
      json_data_list.append(json_data)

  with open("apartments.json", "w", encoding="utf-8") as json_file:
    json.dump(json_data_list, json_file, ensure_ascii = False, indent = 2)

if __name__ == "__main__":
  get_apart_data()