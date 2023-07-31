import json
import re
import requests
from bs4 import BeautifulSoup

cities = ['tienda-medellin', 'nuestra-pasteleria-en-barranquilla-santa-elena', 'tiendas-pastelerias-pereira', 'tienda-bogota', 'tienda-monteria']
shops = []
for city in cities:
    print(city)
    html = requests.get(f"https://www.santaelena.com.co/tiendas-pasteleria/{city}/").text
    soup = BeautifulSoup(html, 'html.parser')
    widgets = soup.find_all("div", re.compile("elementor-element elementor-element-....... elementor-widget "
                                              "elementor-widget-text-editor"))

    shops_info = [widget.text.strip() for widget in widgets if 'Dirección' in str(widget)]
    for info in shops_info:
        shop = {
            "name": "Sante Elena",
            "address": info.split("Dirección:")[1].split("Teléfono:")[0].replace("\n", " "),
            "latlon": "",
            "phones": info.split("Teléfono:")[1].split("Horario de atención:")[0].replace("\n", " "),
            "working_hours": info.split("Horario de atención:")[1].replace("\n", " ")
        }
        shops.append(shop)

shops_json = json.dumps(shops)
with open(f"shops.json", 'w', encoding="utf-8") as f:
    f.write(shops_json)
