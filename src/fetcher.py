import hashlib
import time
import requests
from requests.exceptions import RequestException, Timeout
from src import config

class FetchError(Exception):
    pass

def _get_cache_path(url: str, cache_filename: str = None) -> str:
    if cache_filename:
        filename = cache_filename
    else:
        url_hash = hashlib.md5(url.encode('utf-8')).hexdigest()
        filename = f"detail-{url_hash}.html"
    return config.CACHE_DIR / filename

def fetch_page(url: str, cache_filename: str = None) -> str:
    """
    Fetches a page, either from cache or via HTTP.
    Handles politeness, retries, and caching.
    """
    cache_path = _get_cache_path(url, cache_filename)

    if cache_path.exists():
        html_content = cache_path.read_text(encoding='utf-8')
        print(f"CACHE HIT: {url}")
        return html_content

    # Network fetch
    time.sleep(config.POLITENESS_DELAY)
    
    headers = {"User-Agent": config.USER_AGENT}
    
    def attempt_fetch() -> requests.Response:
        response = requests.get(url, headers=headers, timeout=config.REQUEST_TIMEOUT)
        response.raise_for_status()
        return response

    try:
        response = attempt_fetch()
    except (Timeout, requests.exceptions.HTTPError) as e:
        # Retry logic for timeout or 5xx
        is_5xx = isinstance(e, requests.exceptions.HTTPError) and 500 <= e.response.status_code < 600
        is_timeout = isinstance(e, Timeout)
        
        # Do not retry 404 or 403
        if isinstance(e, requests.exceptions.HTTPError) and e.response.status_code in (403, 404):
            raise FetchError(f"HTTP {e.response.status_code} Error: {url}") from e
            
        if is_5xx or is_timeout:
            print(f"RETRYING: {url} after failure ({e})")
            time.sleep(1.5)
            try:
                response = attempt_fetch()
            except Exception as retry_e:
                raise FetchError(f"Failed to fetch {url} after retry: {retry_e}") from retry_e
        else:
            raise FetchError(f"Request failed for {url}: {e}") from e
    except RequestException as e:
        raise FetchError(f"Request exception for {url}: {e}") from e

    html_content = response.text
    cache_path.write_text(html_content, encoding='utf-8')
    print(f"FETCH: {url} (size: {len(html_content.encode('utf-8'))})")
    
    return html_content
