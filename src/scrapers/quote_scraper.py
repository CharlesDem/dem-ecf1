import re
import time
from typing import Optional, Generator
from urllib.parse import urljoin

import requests
from bs4 import BeautifulSoup
import structlog

from src.config.scraper_config import quote_scraper_config
from src.models.models import Author, Quote

logger = structlog.get_logger()

## Class de Scrapping

class QuotesScraper:

    
    def __init__(self):
        self.base_url = quote_scraper_config.base_url
        self.delay = quote_scraper_config.delay
        self.session = requests.Session()
        self._setup_session()
        
        # Cache pour éviter de re-scraper les auteurs
        self.authors_cache: dict[str, Author] = {}
    
    def _setup_session(self) -> None:
        """Configure la session HTTP."""
        self.session.headers.update({
            "User-Agent": "scraper-2026-chd",
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
            response = self.session.get(url, timeout=quote_scraper_config.timeout)
            response.raise_for_status()
            
            # Politesse
            time.sleep(self.delay)
            
            return BeautifulSoup(response.content, "lxml")
            
        except requests.RequestException as e:
            logger.error("fetch_failed", url=url, error=str(e))
            raise
    
    def _clean_text(self, text: str) -> str:
        """Nettoie le texte d'une citation."""
        # Supprimer les guillemets décoratifs
        text = text.strip()
        text = re.sub(r'^[""\u201c\u201d]+|[""\u201c\u201d]+$', '', text)
        return text.strip()
    
    def scrape_quotes_page(self, url: str) -> list[Quote]:
        """
        Scrape une page de citations.
        
        Args:
            url: URL de la page
            
        Returns:
            Liste de citations
        """
        soup = self._fetch(url)
        if not soup:
            return []
        
        quotes = []
        quote_divs = soup.find_all("div", class_="quote")
        
        for div in quote_divs:
            quote = self._parse_quote(div)
            if quote:
                quotes.append(quote)
        
        return quotes
    
    def _parse_quote(self, element) -> Optional[Quote]:
        """
        Parse un élément de citation.
        
        Args:
            element: Élément BeautifulSoup
            
        Returns:
            Objet Quote ou None
        """
        try:
            # Texte de la citation
            text_elem = element.find("span", class_="text")
            text = self._clean_text(text_elem.text) if text_elem else ""
            
            # Auteur
            author_elem = element.find("small", class_="author")
            author = author_elem.text.strip() if author_elem else "Unknown"
            
            # URL de l'auteur
            author_link = element.find("a", href=True)
            author_url = ""
            if author_link and "/author/" in author_link["href"]:
                author_url = urljoin(self.base_url, author_link["href"])
            
            # Tags
            tags = []
            tags_div = element.find("div", class_="tags")
            if tags_div:
                tag_links = tags_div.find_all("a", class_="tag")
                tags = [tag.text.strip() for tag in tag_links]
            
            return Quote(
                text=text,
                author=author,
                author_url=author_url,
                tags=tags
            )
            
        except Exception as e:
            logger.error("quote_parse_failed", error=str(e))
            return None
    
    def scrape_all_quotes(
        self,
        max_pages: int = 100
    ) -> Generator[Quote, None, None]:
        """
        Scrape toutes les citations avec pagination.
        
        Args:
            max_pages: Limite de pages (None = toutes)
            
        Yields:
            Objets Quote
        """
        max_pages = max_pages or quote_scraper_config.max_pages
        print("max pages ", max_pages)
        page = 1
        url = self.base_url
        
        while url and page <= max_pages:
            logger.info("scraping_page", page=page)
            
            soup = self._fetch(url)
            if not soup:
                break
            
            # Parser les citations de la page
            quote_divs = soup.find_all("div", class_="quote")
            
            for div in quote_divs:
                quote = self._parse_quote(div)
                if quote:
                    yield quote
            
            # Page suivante
            url = self._get_next_page(soup)
            page += 1
    
    def _get_next_page(self, soup: BeautifulSoup) -> Optional[str]:
        """Trouve l'URL de la page suivante."""
        next_li = soup.find("li", class_="next")
        
        if next_li:
            next_link = next_li.find("a", href=True)
            if next_link:
                return urljoin(self.base_url, next_link["href"])
        
        return None
    
    def scrape_author(self, url: str) -> Optional[Author]:
        """
        Scrape les détails d'un auteur.
        
        Args:
            url: URL de la page auteur
            
        Returns:
            Objet Author ou None
        """
        # Vérifier le cache
        if url in self.authors_cache:
            return self.authors_cache[url]
        
        soup = self._fetch(url)
        if not soup:
            return None
        
        try:
            # Nom
            name_elem = soup.find("h3", class_="author-title")
            name = name_elem.text.strip() if name_elem else "Unknown"
            
            # Date de naissance
            born_date_elem = soup.find("span", class_="author-born-date")
            born_date = born_date_elem.text.strip() if born_date_elem else ""
            
            # Lieu de naissance
            born_loc_elem = soup.find("span", class_="author-born-location")
            born_location = born_loc_elem.text.strip() if born_loc_elem else ""
            # Nettoyer "in " au début
            born_location = re.sub(r"^in\s+", "", born_location)
            
            # Biographie
            bio_elem = soup.find("div", class_="author-description")
            bio = bio_elem.text.strip() if bio_elem else ""
            
            author = Author(
                name=name,
                bio=bio,
                born_date=born_date,
                born_location=born_location,
                url=url
            )
            
            # Mettre en cache
            self.authors_cache[url] = author
            logger.info("author_scraped", name=name)
            
            return author
            
        except Exception as e:
            logger.error("author_parse_failed", url=url, error=str(e))
            return None
    
    def scrape_complete(
        self,
        max_pages: int = 3,
    ) -> dict:
        """
        Scrape complet : citations + auteurs.
        
        Args:
            max_pages: Limite de pages
            include_authors: Scraper aussi les auteurs
            
        Returns:
            {quotes: [...], authors: [...]}
        """
        quotes = []
        authors = {}
        
        for quote in self.scrape_all_quotes(max_pages):
            quotes.append(quote)
            
            if quote.author_url:
                if quote.author not in authors:
                    author = self.scrape_author(quote.author_url)
                    if author:
                        authors[quote.author] = author
        
        return {
            "quotes": quotes,
            "authors": list(authors.values())
        }
    
    def close(self) -> None:
        """Ferme la session."""
        self.session.close()