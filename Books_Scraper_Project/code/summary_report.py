total_books = len(_items)

valid_books = 0
invalid_books = 0
unique_books = 0
duplicate_books = 0

total_price = 0
price_count = 0

for item in _items:
    book = item["json"]

    if book["validation_status"] == "Valid":
        valid_books += 1
    else:
        invalid_books += 1

    if book["duplicate_status"] == "Unique":
        unique_books += 1
    else:
        duplicate_books += 1

    try:
        price = float(book["price"].replace("£", "").strip())
        total_price += price
        price_count += 1
    except (ValueError, AttributeError, KeyError):
        pass

average_price = 0

if price_count > 0:
    average_price = round(total_price / price_count, 2)

report = {
    "total_books": total_books,
    "valid_books": valid_books,
    "invalid_books": invalid_books,
    "unique_books": unique_books,
    "duplicate_books": duplicate_books,
    "average_price_gbp": average_price
}

return [{"json": report}]