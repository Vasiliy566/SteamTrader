import csv
import os
import time

from tqdm import tqdm

import requests

from steam_market import get_lowest_price

key = "F3ViTDXAlx0IgPYNkN2GlB9KsS0OZBF"


def get_db_name():
    return requests.get(f"https://market.dota2.net/itemdb/current_570.json").json()['db']


def get_all_items():
    return requests.get(f"https://market.dota2.net/api/QuickItems/?key={key}")


def update_trade_info():
    db_name = get_db_name()
    response = requests.get(f"https://market.dota2.net/itemdb/{db_name}")
    text = response.text.split("\n")
    with open("db.csv", 'w', encoding='UTF8', newline='') as db_file:
        writer = csv.writer(db_file)
        for l in text[1:]:
            row = l.split(";")
            if len(row) == 14 and row[2].isdigit() and 120 * 100 > int(row[2]) > 100 * 100:
                writer.writerow(row)


def get_historical_normal_price(class_id, instance_id):
    r = requests.get(f"https://market.dota2.net/api/ItemHistory/{class_id}_{instance_id}/?key={key}")
    if r.status_code == 200:
        data = r.json()
        if "number" in data:
            print(f"Warning: {data['number']} sales used for stats")
        return data.get("average")


def search_good_trades(class_id, instance_id, name):
    r = requests.get(f"https://market.dota2.net/api/SellOffers/{class_id}_{instance_id}/?key={key}")
    data = r.json()
    if "offers" in data:
        for offer in data["offers"]:
            price = int(offer["price"]) / 100
            steam_price = get_lowest_price(name.replace("\"", ""))
            if steam_price is not None:
                steam_price *= 0.95
                if price <= steam_price:
                    print(
                        f"Good offer for {name}: profit = {(steam_price - price) / price * 100} for price = {price / 100}, average = {steam_price / 100}")
            else:
                print("skipped")

def search_for_good_trades():
    with open('db.csv', encoding='utf-8') as csv_file:
        lines = [line for line in csv_file]
        for row in csv.reader(lines, delimiter=','):
            if len(row) == 14:
                time.sleep(3)
                class_id, instance_id, price, name = row[0], row[1], row[2], row[8]
                try:
                    search_good_trades(class_id, instance_id, name)
                except Exception as e:
                    pass