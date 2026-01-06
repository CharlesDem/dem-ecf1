    
import re
import time
from typing import Generator, Optional
from urllib.parse import urljoin

from bs4 import BeautifulSoup
from fake_useragent import UserAgent
import requests
import structlog
from src.models.models import Book
from src.config.scraper_config import book_scraper_config

logger = structlog.get_logger()

rating_map = {'One':1,'Two':2,'Three':3,'Four':4,'Five':5}

class BookScraper:

    def __init__(self):
        self.base_url = book_scraper_config.base_url
        self.delay = book_scraper_config.delay
        self.session = requests.Session()
        self.ua = UserAgent()
        self._setup_session()
        
    
    def _setup_session(self) -> None:
        """Configure la session HTTP."""
        self.session.headers.update({
            "User-Agent": self.ua.random,
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "en-US,en;q=0.5",
            "Connection": "keep-alive"
        })

    def _fetch(self, url: str) -> Optional[BeautifulSoup]:
        """
        Récupère et parse une page.
        
        Args:
            url: URL à récupérer
            
        Returns:
            BeautifulSoup ou None
        """
        try:
            logger.debug("fetching", url=url)
            response = self.session.get(url, timeout=book_scraper_config.timeout)
            response.raise_for_status()
            
            # Politesse
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, "lxml")
            
        except requests.RequestException as e:
            logger.error("fetch_failed", url=url, error=str(e))
            raise

    def _parse_book(self, element) -> Optional[Book]:

        try:
            title = element.find('h3').find('a')['title']

            price_text = element.find('p', class_='price_color').text
            price = float(re.findall(r'[\d.]+',price_text)[0])

            rating_class = element.find('p',class_='star-rating')['class'][1]
            rating = rating_map.get(rating_class,0)

            availability = element.find('p',class_='instock availability').text.strip()
            in_stock = 'In stock' in availability

            
            return Book(
                title,
                price,
                rating,
                in_stock,
                img_url=None,
            )
            
        except Exception as e:
            logger.error("book_parse_failed", error=str(e))
            return None
        
    def _get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """Trouve l'URL de la page suivante."""
        next_li = soup.find("li", class_="next")
        
        if next_li:
            next_link = next_li.find("a", href=True)
            if next_link:
                return urljoin(self.base_url, next_link["href"])
        
        return None

    def scrape_all_books(
            self,
            max_pages: int = 100
        ) -> Generator[Book, None, None]:

            max_pages = max_pages or book_scraper_config.max_pages
            page = 1
            url = self.base_url     

            while url and page <= max_pages:
                logger.info("scraping_page", page=page)
                
                soup = self._fetch(url)
                if not soup:
                    break
                
                books_divs = soup.find_all('article',class_='product_pod')
                
                for div in books_divs:
                    quote = self._parse_book(div)
                    if quote:
                        yield quote
                
                url = self._get_next_page(soup)
                page += 1


    def scrape_complete(
        self,
        max_pages: int = 3,
    ) -> dict:
        books = []
        
        for book in self.scrape_all_books(max_pages):
            books.append(book)
            
        return {
            "books": books,
        }

    def close(self) -> None:
        """Ferme la session."""
        self.session.close()