from dataclasses import dataclass

@dataclass
class QuoteScraperConfig:
    base_url:str = "https://quotes.toscrape.com"
    delay: float = 1.0 
    timeout: int = 30
    max_retries: int = 3
    max_pages: int = 2

@dataclass
class BookScraperConfig:
    base_url:str = "https://books.toscrape.com/catalogue/page-1.html"
    delay: float = 1.0 
    timeout: int = 30
    max_retries: int = 3
    max_pages: int = 2

quote_scraper_config = QuoteScraperConfig()
book_scraper_config = BookScraperConfig()