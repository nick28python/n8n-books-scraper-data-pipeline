duplicates = []

for item in _items:
    book = item["json"]

    if book["duplicate_status"] == "Duplicate":
        duplicates.append({
            "json": {
                "title": book["title"],
                "price": book["price"],
                "rating": book["rating"]
            }
        })

return duplicates