import json
import re
import requests
from bs4 import BeautifulSoup

html = requests.get(f"https://www.santaelena.com.co/tiendas-pasteleria/tienda-medellin/").text
soup = BeautifulSoup(html, 'html.parser')
widgets = soup.find_all("div", re.compile("elementor-element elementor-element-....... elementor-widget "
                                          "elementor-widget-text-editor"))

shops_info = [widget.text.strip() for widget in widgets if 'Dirección' in str(widget)]
shops = []
for info in shops_info:
    info = info.split('\n')
    shop = {
        "name": "Sante Elena",
        "address": info[0].split("Dirección: ")[1] if "Teléfono" in info[
            1] else f"{info[0].split('Dirección: ')[1]} {info[1]}",
        "latlon": "",
        "phones": info[1].split("Teléfono: ")[1] if "Teléfono" in info[1] else info[2].split("Teléfono: ")[1],
        "working_hours": info[4:] if 'Horario' in info[3] else info[3:]
    }
    shops.append(shop)
    print(shop)

shops_json = json.dumps(shops)
with open(f"shops.json", 'w', encoding="utf-8") as f:
    f.write(shops_json)
