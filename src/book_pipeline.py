import json
from src.minio_client import DataType, MinIOStorage
from src.scrapers.book_scraper import BookScraper
from src.db.queries import save_books

class BookPipeline:

    def __init__(self):
        pass

    def __scrap(self):
        try :
            book_scraper = BookScraper()
            minio_client = MinIOStorage()

            res = book_scraper.scrape_complete()
            books = [b.to_dict() for b in res.get("books")]
            books_json = json.dumps(books, ensure_ascii=False, indent=2).encode("utf-8")
            books_result = minio_client.upload(DataType.BOOK, "books/books.json", books_json) #TODO trop compliqué avec l'enum
        
            return {

                "books": { 
                    "data" : res.get("books"),
                    "version" : books_result.get("version")
                }
            }
        finally:
            book_scraper.close()

    def __save_books(self, books: dict):
        data_books = books.get("books")["data"]
        version = books.get("books")["version"]
        save_books(data_books, version)

    def books(self):
        result = self.__scrap()
        print(result)
        self.__save_books(result)


def main():
    book_pipeline = BookPipeline()
    book_pipeline.books()

if __name__ == "__main__":
    main()