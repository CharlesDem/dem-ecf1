import json

import structlog
from src.db.queries import save_quote
from src.minio_client import DataType, MinIOStorage
from src.scrapers.quote_scraper import QuotesScraper


logger = structlog.get_logger()

class QuotePipeline:

    def __init__(self):
        pass

    def __scrap_quotes(self):
        try :
            quote_scraper = QuotesScraper()
            minio_client = MinIOStorage()
            authors_quotes = quote_scraper.scrape_complete(1)

            authors = [a.to_dict() for a in authors_quotes.get("authors")]
            authors_json = json.dumps(authors, ensure_ascii=False, indent=2).encode("utf-8")
            minio_client.upload(DataType.QUOTE, "authors/authors.json", authors_json)

            quotes = [q.to_dict() for q in authors_quotes.get("quotes")]
            quotes_json = json.dumps(quotes, ensure_ascii=False, indent=2).encode("utf-8")
            quotes_result = minio_client.upload(DataType.QUOTE, "quotes/quotes.json", quotes_json)

            return {
                "authors": {
                    "data" : authors_quotes.get("authors")
                },
                "quotes": { 
                    "data" : authors_quotes.get("quotes"),
                    "version" : quotes_result.get("version")
                }
            }
        finally:
            quote_scraper.close()

    def __save_quotes(self, quotes_and_authors: dict):
        authors = quotes_and_authors.get("authors")["data"]
        version = quotes_and_authors.get("quotes")["version"]
        data = quotes_and_authors.get("quotes")["data"]
        for quote in data:
            save_quote(quote, authors, version)

    def quotes(self):
        scrap_result = self.__scrap_quotes()
        self.__save_quotes(scrap_result)