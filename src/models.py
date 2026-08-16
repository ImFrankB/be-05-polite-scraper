from typing import Optional, List
from pydantic import BaseModel, HttpUrl, Field, field_validator
from datetime import datetime

class RawBookRecord(BaseModel):
    title: str
    product_url: str
    price_text: str
    availability_text: str
    rating_text: str
    description: Optional[str]
    source_page: str
    fetched_at: str

class ValidatedBookRecord(BaseModel):
    title: str
    product_url: HttpUrl
    price_text: str
    price_gbp: float
    availability_text: str
    rating_text: str
    description: Optional[str]
    source_page: HttpUrl
    fetched_at: datetime

    @field_validator("price_gbp", mode="before")
    @classmethod
    def parse_price(cls, v, info):
        if isinstance(v, (int, float)):
            return float(v)
        # If it's a string, we expect something like "£51.77"
        if isinstance(v, str):
            cleaned = "".join(c for c in v if c.isdigit() or c == ".")
            if cleaned:
                return float(cleaned)
        raise ValueError("Could not parse price_gbp from price_text")

class RunReport(BaseModel):
    start_time: datetime
    end_time: datetime
    duration_seconds: float
    catalogue_pages_discovered: int
    total_urls_discovered: int
    pages_fetched: int
    cache_hits: int
    valid_records: int
    invalid_records: int
    failed_pages: int
    failed_urls: List[str]
