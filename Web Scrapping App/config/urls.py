# config/urls.py
"""
Website URLs and scraping configurations
"""

# Supported websites for scraping
SUPPORTED_WEBSITES = {
    "books.toscrape.com": {
        "name": "Books to Scrape",
        "type": "books",
        "base_url": "http://books.toscrape.com",
        "pages": 50  # Number of pages to scrape
    },
    "quotes.toscrape.com": {
        "name": "Quotes to Scrape", 
        "type": "quotes",
        "base_url": "http://quotes.toscrape.com",
        "pages": 10
    }
}

def is_supported_website(url):
    """Check if the website is supported for scraping"""
    for domain, config in SUPPORTED_WEBSITES.items():
        if domain in url:
            return True, config
    return False, None