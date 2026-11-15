"""
Course: ISM 2411
Lab: Lab 12 — Read a Sales CSV, Write a Cleaned Report
Student Name: Joshua Eisenberg

Reflection Questions:
1. You've now completed a full ETL pipeline: read a CSV, transform the data, write a new CSV. How does this compare to doing the same task in Excel? What can Python do that Excel can't do easily, and vice versa?
Answer: Building an ETL pipeline in Python automates the entire process so it can be repeated identically on new data files with a single command, without clicking through menus or risking accidental formula overwrites. Python handles massive datasets easily without crashing and integrates directly with logs and APIs, whereas Excel is much better for quick, visual ad-hoc exploration and sharing formatted spreadsheets with non-technical teammates.

2. Exercise 8 showed you append mode. Think of a real business process that would benefit from an append-mode log file — describe it and explain why append mode is the right tool.
Answer: An automated nightly inventory sync or payment processing script for an e-commerce store would greatly benefit from an append-mode log file. Append mode is the right tool because it preserves a permanent, chronological audit trail of every run—including timestamps, processed record counts, and errors—without overwriting previous history.
"""

import csv
from datetime import datetime

print("--- Exercise 1 ---")
with open("data/sales.csv", "r", newline="") as file:
    reader = csv.reader(file)
    rows = list(reader)
    print(f"Header: {rows[0]}")
    print(f"Data rows: {len(rows) - 1}")

print("--- Exercise 2 ---")
with open("data/sales.csv", "r", newline="") as file:
    reader = csv.reader(file)
    for row in reader:
        print(row)

print("--- Exercise 3 ---")
with open("data/sales.csv", "r", newline="") as file:
    reader = csv.reader(file)
    header = next(reader)
    print(f"Header: {header}")
    for row in reader:
        print(row)

print("--- Exercise 4 ---")
overall_revenue = 0

with open("data/sales.csv", "r", newline="") as file:
    reader = csv.reader(file)
    next(reader)
    for row in reader:
        product = row[0]
        price = float(row[1])
        quantity = int(row[2])
        total = price * quantity
        overall_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")

print(f"Total Revenue: ${overall_revenue:.2f}")

print("--- Exercise 5 ---")
original_count = 0
written_count = 0

with open("data/sales.csv", "r", newline="") as infile, open("data/cleaned.csv", "w", newline="") as outfile:
    reader = csv.reader(infile)
    writer = csv.writer(outfile)
    next(reader)
    writer.writerow(["Product", "Price", "Qty", "Total"])

    for row in reader:
        original_count += 1
        product = row[0]
        price = float(row[1])
        qty = int(row[2])
        total = price * qty

        if total > 100:
            written_count += 1
            writer.writerow([product, f"{price:.2f}", qty, f"{total:.2f}"])

print(f"Rows written: {written_count} out of {original_count}")

print("--- Exercise 6 ---")
# csv.reader is simpler when you just want to grab columns by index position without headers.
# csv.DictReader is better when a file has clear column names, making code easier to read.

dict_revenue = 0

with open("data/sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row["product"]
        price = float(row["price"])
        quantity = int(row["quantity"])
        total = price * quantity
        dict_revenue += total
        print(f"{product}: {quantity} units × ${price:.2f} = ${total:.2f}")

print(f"Total Revenue: ${dict_revenue:.2f}")

print("--- Exercise 7 ---")
sales_by_product = {}

with open("data/sales.csv", "r", newline="") as file:
    reader = csv.DictReader(file)
    for row in reader:
        product = row["product"]
        total = float(row["price"]) * int(row["quantity"])
        sales_by_product[product] = sales_by_product.get(product, 0) + total

for product in sorted(sales_by_product):
    print(f"{product}: ${sales_by_product[product]:.2f}")

print("--- Exercise 8 ---")
timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

with open("data/run_log.txt", "a") as log_file:
    log_file.write(f"{timestamp} - Total Revenue: ${overall_revenue:.2f}\n")

print(f"Logged run at {timestamp}")