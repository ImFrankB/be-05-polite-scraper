from src.parser import parse_catalogue_page, parse_detail_page
from src.models import ValidatedBookRecord
from pydantic import ValidationError
import pytest

def test_parse_catalogue_page():
    html = """
    <html>
        <body>
            <article class="product_pod">
                <h3><a href="catalogue/book1/index.html">Book 1</a></h3>
            </article>
            <li class="next"><a href="page-2.html">next</a></li>
        </body>
    </html>
    """
    urls, next_url = parse_catalogue_page(html, "http://books.toscrape.com/")
    assert len(urls) == 1
    assert urls[0] == "http://books.toscrape.com/catalogue/book1/index.html"
    assert next_url == "http://books.toscrape.com/page-2.html"

def test_validate_price():
    raw_record = {
        "title": "A Book",
        "product_url": "http://books.toscrape.com/book1",
        "price_text": "£51.77",
        "availability_text": "In stock (22 available)",
        "rating_text": "Three",
        "description": "A good book.",
        "source_page": "http://books.toscrape.com/page-1",
        "fetched_at": "2023-10-25T14:00:00Z"
    }
    validated = ValidatedBookRecord(**raw_record)
    assert validated.price_gbp == 51.77
    assert validated.price_text == "£51.77"
    
def test_validate_invalid_url():
    raw_record = {
        "title": "A Book",
        "product_url": "not-a-url",
        "price_text": "£51.77",
        "availability_text": "In stock (22 available)",
        "rating_text": "Three",
        "description": "A good book.",
        "source_page": "http://books.toscrape.com/page-1",
        "fetched_at": "2023-10-25T14:00:00Z"
    }
    with pytest.raises(ValidationError):
        ValidatedBookRecord(**raw_record)
