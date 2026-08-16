# The Polite Scraper

## Quickstart

Run the following command to set up the environment, install dependencies, and execute the scraper:

```bash
python -m venv venv && .\venv\Scripts\activate && pip install -r requirements.txt && python src/main.py
```

*(On macOS/Linux, use `source venv/bin/activate` instead).*

## Target Classification
- **Target Site:** `books.toscrape.com` (A sandbox site designed for testing web scrapers).
- **Scope:** Crawl exactly 3 catalogue pages.
- **Data Collected:** Book title, product URL, price, availability, rating, description, source page, and fetch timestamp.
- **Robots.txt:** `/robots.txt` returned 404 (Not Found).

> "I will not reuse this code on another site without checking its rules and terms first."

## Politeness Architecture
The scraper implements the following politeness measures:
- **User-Agent:** `FlyRankInternship-A9/1.0 (+https://github.com/<username>/the-polite-scraper)`
- **Request Timeout:** 8 seconds per request.
- **Throttling:** 500ms delay (`time.sleep(0.5)`) between actual outbound HTTP requests.
- **Caching:** Requests are cached locally in the `cache/` directory. Cache hits incur zero politeness delay and zero network overhead.

## Schema Definition
The scraper extracts the following raw string fields from each detail page:
- `title`
- `product_url`
- `price_text`
- `availability_text`
- `rating_text`
- `description`
- `source_page`
- `fetched_at`

During validation, the `price_text` (e.g., `"£51.77"`) is normalized into `price_gbp` (e.g., `51.77` as a float). `product_url` and `source_page` are resolved and validated as absolute URLs. Both the raw text and normalized fields are present in the final output.

## Sample Run Report
```json
{
  "start_time": "2023-10-25T14:00:00.000000Z",
  "end_time": "2023-10-25T14:00:32.000000Z",
  "duration_seconds": 32.5,
  "catalogue_pages_discovered": 3,
  "total_urls_discovered": 60,
  "pages_fetched": 63,
  "cache_hits": 0,
  "valid_records": 60,
  "invalid_records": 0,
  "failed_pages": 0,
  "failed_urls": []
}
```

## Browserless Execution
This project uses `requests` and `BeautifulSoup4` instead of a headless browser like Playwright or Puppeteer. The data on `books.toscrape.com` is completely pre-rendered in the server's HTML response, meaning there is no dynamic JavaScript rendering required to view the catalogue or book details. Bypassing headless browsers significantly reduces execution overhead and resource consumption.

## Ethics Statement
When scraping, always:
- Respect the site's Terms of Service and `robots.txt`.
- Use official APIs when available instead of scraping HTML.
- Throttle traffic to avoid overloading the server.
- Never bypass authentication or paywalls without authorization.
