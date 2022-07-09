import steammarket as sm


def get_lowest_price(name):
    print(f"Try to get {name}")
    item = sm.get_item(570, name, currency='RUB')
    if item["success"]:
        return float(item.get("lowest_price").replace(",", ".").split()[0])


