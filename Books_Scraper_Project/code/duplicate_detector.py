seen_books = set()

for item in _items:
    book = item["json"]

    title = book["title"].strip().lower()
    price = book["price"].strip()

    book_key = title

    if book_key in seen_books:
        book["duplicate_status"] = "Duplicate"
    else:
        seen_books.add(book_key)
        book["duplicate_status"] = "Unique"

return _items
