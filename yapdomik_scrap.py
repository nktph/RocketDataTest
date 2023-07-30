import json
import requests
from bs4 import BeautifulSoup

cities = ["berdsk", "achinsk", "krsk", "nsk", "omsk", "tomsk"]
sushi_bars = []
for i, city in enumerate(cities):
    html = requests.get(f"https://{city}.yapdomik.ru/about").text
    soup = BeautifulSoup(html, 'html.parser')

    adr_div = soup.find('div', class_='site-footer__address-list')

    city_name = adr_div.find_all('h2')[1].text.split("г. ")[1].replace(":", "")
    addresses = adr_div.find_all('li')
    phone = soup.find('a', class_="link link--black link--underline").text
    for address in addresses:
        address = f"{city_name}, {address.text}"
        org_info = requests.get(f"https://search-maps.yandex.ru/v1/?text=японский домик, {address}&type=biz&"
                      f"lang=ru_RU&apikey=c6293ec4-0ab5-42db-881f-bd282bf3a133").json()

        coords = [org_info['features'][0]['geometry']['coordinates'][1], org_info['features'][0]['geometry']['coordinates'][0]]
        working_hours = org_info['features'][0]['properties']['CompanyMetaData']['Hours']['text'].strip().split(";")
        sushi_bar = {
            "name": "Японский Домик",
            "address": address,
            "latlon": coords,
            "phones": [phone],
            "working_hours": working_hours
        }
        sushi_bars.append(sushi_bar)

sushi_bars_json = json.dumps(sushi_bars)
with open(f"sushi_bars.json", 'w', encoding="utf-8") as f:
    f.write(sushi_bars_json)