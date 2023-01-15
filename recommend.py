import httpx
from selectolax.parser import HTMLParser
import csv
import time
from datetime import datetime
from dataclasses import dataclass, asdict

@dataclass
class Seller:
    seller: str
    stock: str
    date: str
    time: str
    change: int

def get_time():
    current_time = time.time()
    day = datetime.fromtimestamp(current_time).strftime("%Y-%m-%d")
    hour = datetime.fromtimestamp(current_time).strftime("%H:%M:%S")
    return [day, hour]

def last_stock_value():
    with open("AbGold.csv", "r") as f:
        reader =  csv.reader(f)
        data = list(reader)
        return int(data[-1][1].replace(",", ""))


    
url = "https://www.g2g.com/offer/Area-52--US----Horde?service_id=lgc_service_1&brand_id=lgc_game_2299&region_id=dfced32f-2f0a-4df5-a218-1e068cfadffa&fa=lgc_2299_platform%3Algc_2299_platform_40012"

resp = httpx.get(url=url, timeout=10)
tree = HTMLParser(resp.text)

stock = tree.css('div.offers-bottom-attributes.offer__content-lower-items span')[1].text().replace("K", "")
name = tree.css('div.seller__name-detail')[2].text()
day_hour = get_time()

last_stock =  last_stock_value()


monitoreo = Seller(
seller=name,
stock=stock,
date=day_hour[0],
time=day_hour[1],
change=last_stock - int(stock.replace(",",""))
)
with open("AbGold.csv", "a", newline="") as f:
    fieldnames = ["seller", "stock", "date", "time", "change"]
    writer= csv.DictWriter(f, fieldnames=fieldnames)
    writer.writerow(asdict(monitoreo))
    print("Search Done")