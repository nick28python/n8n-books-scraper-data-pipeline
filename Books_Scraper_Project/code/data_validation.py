for item in _items:
    book = item["json"]

    issues = []

    if not book.get("title"):
        issues.append("Missing title")

    if not isinstance(book.get("price_gbp"), (int, float)):
        issues.append("Invalid price")

    if book.get("rating") not in [1, 2, 3, 4, 5]:
        issues.append("Invalid rating")

    if book.get("availability") not in ["In stock"]:
        issues.append("Check availability")

    book["validation_status"] = "Valid" if not issues else "Check"
    book["validation_issues"] = issues

return _items
