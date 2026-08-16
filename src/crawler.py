from datetime import datetime, timezone
from src import fetcher, parser, config
from src.models import ValidatedBookRecord, RunReport
from pydantic import ValidationError
import json
import time

def crawl():
    start_time = datetime.now(timezone.utc)
    
    current_url = config.BASE_URL + "index.html"
    pages_crawled = 0
    max_pages = 3
    
    book_links_to_fetch = []
    pages_fetched = 0
    cache_hits = 0
    
    # Discovery Phase
    while current_url and pages_crawled < max_pages:
        cache_filename = f"catalogue-page-{pages_crawled + 1}.html"
        cache_path = fetcher._get_cache_path(current_url, cache_filename)
        
        if cache_path.exists():
            cache_hits += 1
            
        try:
            html = fetcher.fetch_page(current_url, cache_filename=cache_filename)
            pages_fetched += 1
        except fetcher.FetchError as e:
            print(f"Error fetching catalogue page: {e}")
            break
            
        book_urls, next_url = parser.parse_catalogue_page(html, current_url)
        for b_url in book_urls:
            book_links_to_fetch.append({"url": b_url, "source": current_url})
            
        pages_crawled += 1
        current_url = next_url

    total_urls_discovered = len(book_links_to_fetch)
    
    # Extraction Phase
    valid_records = []
    invalid_records = []
    failed_pages = 0
    failed_urls = []
    
    for item in book_links_to_fetch:
        detail_url = item["url"]
        source_page = item["source"]
        
        cache_path = fetcher._get_cache_path(detail_url)
        if cache_path.exists():
            cache_hits += 1
            
        try:
            fetched_at = datetime.now(timezone.utc).isoformat()
            html = fetcher.fetch_page(detail_url)
            pages_fetched += 1
            raw_record = parser.parse_detail_page(html, detail_url, source_page, fetched_at)
            
            try:
                validated = ValidatedBookRecord(**raw_record.model_dump())
                valid_records.append(validated.model_dump(mode='json'))
            except ValidationError as e:
                invalid_records.append({
                    "raw_record": raw_record.model_dump(),
                    "error": str(e)
                })
                
        except Exception as e:
            failed_pages += 1
            failed_urls.append(detail_url)
            print(f"Failed to process {detail_url}: {e}")

    end_time = datetime.now(timezone.utc)
    duration_seconds = (end_time - start_time).total_seconds()
    
    report = RunReport(
        start_time=start_time,
        end_time=end_time,
        duration_seconds=duration_seconds,
        catalogue_pages_discovered=pages_crawled,
        total_urls_discovered=total_urls_discovered,
        pages_fetched=pages_fetched,
        cache_hits=cache_hits,
        valid_records=len(valid_records),
        invalid_records=len(invalid_records),
        failed_pages=failed_pages,
        failed_urls=failed_urls
    )
    
    return valid_records, invalid_records, report
