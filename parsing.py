from bs4 import BeautifulSoup
import requests
import csv

# URL = "https://autoby.by/cars/lexus/nx/"
HEADERS = {'user-agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) '
                         'snap Chromium/80.0.3987.132 Chrome/80.0.3987.132 Safari/537.36', 'accept': '*/*'
}
HOST = 'https://autoby.by'
FILE = '../telegram-bot-parsing_auto/cars.csv'


def get_html(url, params = None):
    r = requests.get(url, headers = HEADERS, params=params)
    return r


def get_pages_count(html):
    soup = BeautifulSoup(html, 'html.parser')
    pagination = soup.find('ul', class_ = 'pagination')
    if pagination:
        pagination = soup.find('ul', class_='pagination').find_all('li')
        return int(pagination[-2].get_text())
    else:
        return 1


def get_content(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_ = 'info-wrapper visible-xs')
    cars = []
    for item in items:
        cars.append({
            'title': item.find('a').get_text().replace('\n', "").replace(",", " Год:"),
            'usd_price': item.find('div', class_ = 'd-price').get_text().replace('\n', ""),
            'byn_price': item.find('div', class_='r-price col-xs-12').get_text().replace('\n', ""),
            'link': HOST +item.find('div', class_ = 'info').find_next('a').get('href')
        })
    return cars


def save_file(items, path):
    with open(path, 'w', newline='') as file:
        writer = csv.writer(file, delimiter = ';')
        writer.writerow(['Марка', 'Ссылка','Цена в $','Цена в BYN'])
        for item in items:
            writer.writerow([item['title'], item['link'], item['usd_price'], item['byn_price']])


def parse(URL):
    html = get_html(URL)
    if html.status_code == 200:
        cars = []
        pages_count = get_pages_count(html.text)
        for page in range(1,pages_count + 1):
            print(f'Parsing page {page} from {pages_count}...')
            html = get_html(URL, params={'page': page})
            cars.extend(get_content(html.text))
        save_file(cars, FILE)
        return f'Getting {len(cars)} cars'
    else:
        return "Errors"


if __name__ == '__main__':
    print(parse())