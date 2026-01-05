from dataclasses import dataclass

@dataclass
class ScraperConfig:
    base_url:str = "https://quotes.toscrape.com"
    delay: float = 1.0 
    timeout: int = 30
    max_retries: int = 3
    max_pages: int = 20

scraper_config = ScraperConfig()