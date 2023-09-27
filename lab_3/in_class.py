import requests
from bs4 import BeautifulSoup

def get_max_num_pages(url):
  response = requests.get(url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    last_page_li = soup.find("li", class_="is-last-page")

    if last_page_li:
      last_page_link = last_page_li.find("a")
      if last_page_link:
        last_page_url = last_page_link.get("href")
        last_page_number = int(last_page_url.split("=")[-1])
        return last_page_number

  return None

def scrape_page_recursive(url, max_num_pages = None, current_page = 1):
  base_url = "https://999.md"
  absolute_urls = set()

  # Scrape all pages
  if max_num_pages is None:
    max_num_pages = get_max_num_pages(url)

  # Base case
  if current_page > max_num_pages:
    return list(absolute_urls)

  full_url = f"{url}?page={current_page}"
  response = requests.get(full_url)

  if response.status_code == 200:
    soup = BeautifulSoup(response.text, 'html.parser')
    links = soup.find_all("a", class_="js-item-ad")

    for i, link in enumerate(links):
      href = link.get('href')

      if href and '/booster/' not in href:
        absolute_url = base_url + href
        print(f"Page {current_page}, index {i}:", absolute_url)
        absolute_urls.add(absolute_url)

    next_page_urls = scrape_page_recursive(url, max_num_pages, current_page + 1)
    absolute_urls.update(next_page_urls)
  else:
    print(f"An error occurred during the request for page {current_page}. Status code: {response.status_code}")

  return list(absolute_urls)

def urls_to_txt(urls):
  with open("apartments.txt", "w") as file:
    for url in urls:
      file.write(url + "\n")

if __name__ == "__main__":
  url = "https://999.md/ro/list/real-estate/apartments-and-rooms"
  max_num_pages = 1
  absolute_urls = scrape_page_recursive(url, max_num_pages)
  urls_to_txt(absolute_urls)

