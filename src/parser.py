from bs4 import BeautifulSoup
from urllib.parse import urljoin
from typing import Tuple, List, Optional
from src.models import RawBookRecord

def parse_catalogue_page(html: str, base_url: str) -> Tuple[List[str], Optional[str]]:
    soup = BeautifulSoup(html, "lxml")
    book_urls = []
    
    for article in soup.find_all("article", class_="product_pod"):
        a_tag = article.find("h3").find("a")
        if a_tag and a_tag.has_attr("href"):
            book_urls.append(urljoin(base_url, a_tag["href"]))
            
    next_btn = soup.find("li", class_="next")
    next_url = None
    if next_btn:
        a_tag = next_btn.find("a")
        if a_tag and a_tag.has_attr("href"):
            next_url = urljoin(base_url, a_tag["href"])
            
    return book_urls, next_url

def parse_detail_page(html: str, url: str, source_page: str, fetched_at: str) -> RawBookRecord:
    soup = BeautifulSoup(html, "lxml")
    
    main_div = soup.find("div", class_="col-sm-6 product_main")
    title = main_div.find("h1").get_text(strip=True) if main_div else ""
    
    price_p = main_div.find("p", class_="price_color") if main_div else None
    price_text = price_p.get_text(strip=True) if price_p else ""
    
    avail_p = main_div.find("p", class_="instock availability") if main_div else None
    availability_text = avail_p.get_text(strip=True) if avail_p else ""
    
    rating_p = main_div.find("p", class_="star-rating") if main_div else None
    rating_text = ""
    if rating_p:
        classes = rating_p.get("class", [])
        for c in classes:
            if c != "star-rating":
                rating_text = c
                break
                
    desc_div = soup.find("div", id="product_description")
    description = None
    if desc_div:
        desc_p = desc_div.find_next_sibling("p")
        if desc_p:
            description = desc_p.get_text(strip=True)
            
    return RawBookRecord(
        title=title,
        product_url=url,
        price_text=price_text,
        availability_text=availability_text,
        rating_text=rating_text,
        description=description,
        source_page=source_page,
        fetched_at=fetched_at
    )
