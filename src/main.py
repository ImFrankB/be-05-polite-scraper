import json
from src.crawler import crawl
from src.config import OUTPUT_DIR

def main():
    print("Starting The Polite Scraper...")
    valid_records, invalid_records, report = crawl()
    
    books_file = OUTPUT_DIR / "books.json"
    errors_file = OUTPUT_DIR / "errors.json"
    report_file = OUTPUT_DIR / "run-report.json"
    
    books_file.write_text(json.dumps(valid_records, indent=2), encoding="utf-8")
    
    if invalid_records:
        errors_file.write_text(json.dumps(invalid_records, indent=2), encoding="utf-8")
    elif errors_file.exists():
        errors_file.write_text("[]", encoding="utf-8")
        
    # Pydantic v2 .model_dump_json() serialization
    report_file.write_text(report.model_dump_json(indent=2), encoding="utf-8")
    
    print(f"Scrape completed in {report.duration_seconds:.2f} seconds.")
    print(f"Total discovered: {report.total_urls_discovered}")
    print(f"Valid records: {report.valid_records}")
    print(f"Failed pages: {report.failed_pages}")

if __name__ == "__main__":
    main()
