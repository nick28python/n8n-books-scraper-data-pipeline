urls = []

base_url = "https://books.toscrape.com/"

for page in range(1, 51):

    if page == 1:
        url = base_url
    else:
        url = base_url + f"catalogue/page-{page}.html"

    urls.append({
        "json": {
            "page": page,
            "url": url
        }
    })

return urls
