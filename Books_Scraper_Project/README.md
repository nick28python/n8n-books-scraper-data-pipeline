# Books Scraper & Data Quality Workflow (n8n)

An n8n workflow that scrapes the 50-page **Books to Scrape** demo catalogue, transforms the extracted book data, validates records, detects duplicate titles, and produces CSV reports.

This is a learning project demonstrating workflow automation, HTTP requests, HTML extraction, Python-based data processing, error handling, and reporting in n8n.

## What the workflow does

1. **Manual trigger** — starts when the user clicks *Execute workflow*.
2. **Generate page URLs** — creates URLs for pages 1–50 of `https://books.toscrape.com/`.
3. **HTTP requests** — sends GET requests for the generated URLs. Retry on failure is enabled, with up to 3 tries and a 2,000 ms wait between tries. If a request fails, the workflow continues through the error output.
4. **HTML extraction** — extracts book titles, prices, availability, ratings, and a next-page link field from the returned HTML.
5. **Transform records** — creates individual book records and converts prices to numeric GBP values.
6. **Validate records** — checks for a title, a numeric price, a rating from 1 to 5, and the expected availability value (`In stock`). Each record receives a validation status and a list of issues.
7. **Detect duplicate titles** — trims whitespace and converts titles to lowercase before comparison. Repeated normalized titles are marked `Duplicate`; others are marked `Unique`.
8. **Generate reports** — creates the main books CSV, a duplicate-books CSV, a summary report CSV, and an error CSV on the HTTP error branch.

## Workflow outputs

| Output file | Contents |
|---|---|
| `books_data.csv` | Processed book records, including price in GBP, availability, rating, validation status, validation issues, and duplicate status |
| `duplicate_books.csv` | Duplicate-title records, with title, price, and rating |
| `summary_report.csv` | Total, valid, invalid, unique, and duplicate book counts, plus average price in GBP |
| `scraping_errors.csv` | Failed page number, URL, error name, shortened error message, and failure status |

The error CSV is generated only when the HTTP Request node sends items through its error output. If all requests succeed, that branch has no items to export in that execution.

## Duplicate detection rule

The current exported workflow identifies duplicates using the normalized **book title only**:

```python
title = book["title"].strip().lower()
book_key = title
```

Two records with the same title are therefore treated as duplicates even if their prices differ.

## Error handling

The HTTP Request node retries failed requests up to three times, waiting 2 seconds between attempts. If a request still fails, the workflow continues through the error output to the Error Logger and CSV conversion nodes.

## Technologies and n8n nodes

- n8n
- Manual Trigger
- HTTP Request
- HTML
- Code nodes using Python
- Convert to File (CSV)

## About the Python Code Files

The Python files in the `code/` directory contain the code used inside the n8n Code nodes. They are provided separately for readability, documentation, and reference.

**Important:** These are n8n-specific code snippets, not standalone Python programs. They use n8n's execution context and built-in variables such as `_items`, and their output is returned using n8n's expected item structure.

| File | Purpose |
|---|---|
| `url_generator.py` | Generates URLs for all 50 catalogue pages. |
| `data_validation.py` | Validates book records and identifies missing or invalid fields. |
| `duplicate_detector.py` | Detects duplicate book titles using normalized title comparisons. |
| `duplicate_report.py` | Filters duplicate records to generate the duplicate report. |
| `summary_report.py` | Calculates record counts and average book price for the summary report. |

To run these snippets, import the n8n workflow and execute them within their respective Code nodes. They are not intended to be executed directly as regular `.py` files.

## Suggested repository structure

```text
books-scraper-n8n/
├── workflow/
│   └── books_scraper_workflow.json
├── output/
│   ├── books_data.csv
│   ├── duplicate_books.csv
│   └── summary_report.csv
├── screenshots/
│   ├── complete_workflow.png
│   └── summary_report.png
└── README.md
```

Include `scraping_errors.csv` in `output/` if you want to publish the sample error-branch export too.

## How to use

1. Import `workflow/books_scraper_workflow.json` into your n8n instance.
2. Review the nodes and confirm that the target website is reachable.
3. Run the workflow with **Execute workflow**.
4. Download the generated CSV files from the relevant Convert to File nodes.

The workflow currently uses a manually generated list of 50 page URLs. The extracted `next_page` field is not used to drive pagination.

## Scope and limitations

- This workflow is configured for the static HTML structure of the Books to Scrape demo website. It is not a general-purpose scraper.
- It does not use browser automation to execute JavaScript-rendered pages.
- The page range is fixed at 50 pages in the URL-generation code.
- The error-report branch runs only when HTTP requests fail.
- The workflow is manually triggered; no schedule or external notification integration is configured.
- Adapt selectors, validation rules, and request settings before applying this pattern to another website.

## Learning goals demonstrated

- Passing items between n8n nodes
- Making HTTP GET requests
- Extracting structured data from HTML with CSS selectors
- Transforming extracted values into records
- Validating data and recording issues
- Detecting duplicates with a Python set
- Handling request failures through a separate error branch
- Producing CSV exports and a summary report
