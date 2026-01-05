import json
from src.minio_client import DataType, MinIOStorage
from src.scrapers.quote_scraper import QuotesScraper

def scrap_quotes():
    quote_scraper = QuotesScraper()
    minio_client = MinIOStorage()
    authors_quotes = quote_scraper.scrape_complete()

    authors = [a.to_dict() for a in authors_quotes.get("authors")]
    authors_json = json.dumps(authors, ensure_ascii=False, indent=2).encode("utf-8")
    authors_result = minio_client.upload(DataType.QUOTE, "authors/authors.json", authors_json)


    quotes = [q.to_dict() for q in authors_quotes.get("quotes")]
    quotes_json = json.dumps(quotes, ensure_ascii=False, indent=2).encode("utf-8")
    quotes_result = minio_client.upload(DataType.QUOTE, "quotes/quotes.json", quotes_json)

    return {
        "authors": {
            "data" : authors_quotes.get("authors"),
            "version" : authors_result.get("version")
        },
        "quotes": { 
            "data" : authors_quotes.get("quotes"),
            "version" : quotes_result.get("version")
        }
    }

def quotes():
    scrap_result = scrap_quotes()
    

def main():
    quotes()
    




if __name__ == "__main__":
    main()