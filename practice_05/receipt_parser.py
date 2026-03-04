import re
import json

# read file
with open("raw.txt", "r", encoding="utf-8") as f:
    text = f.read()

# extract prices (numbers like 308,00 or 1 200,00)
price_strings = re.findall(r"\d{1,3}(?:\s\d{3})*,\d{2}", text)

# convert prices to float
prices = [float(p.replace(" ", "").replace(",", ".")) for p in price_strings]

# extract product names
products = re.findall(r"\d+\.\n(.+)", text)

# extract date and time
datetime_match = re.search(r"\d{2}\.\d{2}\.\d{4}\s\d{2}:\d{2}:\d{2}", text)

date = None
time = None
if datetime_match:
    date, time = datetime_match.group().split()

# payment method
payment = "Card" if "Банковская карта" in text else "Cash"

# extract total
total_match = re.search(r"ИТОГО:\n([\d\s,]+)", text)

total = None
if total_match:
    total = float(total_match.group(1).replace(" ", "").replace(",", "."))

# output
data = {
    "products": products,
    "prices": prices,
    "date": date,
    "time": time,
    "payment_method": payment,
    "total": total
}

print(json.dumps(data, indent=4, ensure_ascii=False))