from psycopg import Cursor

from src.db.postgres_lib import db
from src.models.models import Author, Partner, Quote

def fetch_as_scalar(cursor: Cursor):
    value = cursor.fetchone()
    return value


def fetch_as_dicts(cursor: Cursor):
    columns = [desc.name for desc in cursor.description] if cursor.description else []
    rows = cursor.fetchall()
    return [dict(zip(columns, row)) for row in rows]


def __save_author(cursor: Cursor, author: Author, version: int):
    query = """
                INSERT INTO authors(name, bio, birth_date, birth_location, last_scrap_version)
                VALUES (%s, %s, %s, %s, %s)
                ON CONFLICT (name) DO
                UPDATE SET last_scrap_version = EXCLUDED.last_scrap_version 
                RETURNING author_id;
            """
    id = cursor.execute(query, (author.name, author.bio, author.born_date, author.born_location, version))
    return cursor.fetchone()[0]


def __save_tag(cursor: Cursor, tags: list):
    query = """
            INSERT INTO tags (libelle)
                VALUES (%s)
                ON CONFLICT (libelle) DO NOTHING
                RETURNING tag_id;
            """
    ids = []
    for tag in tags:
        cursor.execute(query, (tag,))
        row = cursor.fetchone()
        if row is not None:
            ids.append(row[0])
    
    return ids

def __link_tags(cursor: Cursor, tags: list, quote_id: int):
    query = """
                INSERT INTO quote_tags (quote_id, tag_id)
                VALUES (%s, %s);
            """
    
    rows = [(quote_id, tag_id) for tag_id in tags]
    cursor.executemany(query, rows)


@db
def save_quote(cursor: Cursor, quote: Quote, authors: list[Author], version: int): # la transaction est implicite ? TODO
    tags_ids = __save_tag(cursor, quote.tags)

    author = next(filter(lambda author: author.name == quote.author, authors), None)
    author_id = __save_author(cursor, author, version)

    query = """
                INSERT INTO quotes(text_content, last_scrap_version, author_id)
                VALUES (%s, %s, %s)
                ON CONFLICT (text_content)DO 
                UPDATE SET last_scrap_version = EXCLUDED.last_scrap_version
                RETURNING quote_id;
            """
    cursor.execute(query, (quote.text, version, author_id))
    row = cursor.fetchone()

    if row is not None:
        quote_id = row[0]
        __link_tags(cursor, tags_ids, quote_id)


@db
def save_partners(cursor: Cursor, partners: list[Partner]): #TODO update

    query = """
                INSERT INTO book_stores(
                    name, 
                    address, 
                    zip_code, 
                    city,
                    latitude, 
                    longitude,
                    contact_name_hash, 
                    contact_email_hash, 
                    contact_phone,
                    revenues_crypt, 
                    partner_date, 
                    speciality
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s) 
            """
    
    stores = [
        (
            p.book_store_name,
            p.address,
            p.zipcode,
            p.city,
            p.latitude if hasattr(p, "latitude") else None,
            p.longitude if hasattr(p, "longitude") else None,
            p.name,
            p.email,
            p.phone,
            p.revenue,
            p.partner_date,
            p.speciality,
        )
        for p in partners
    ]

    cursor.executemany(query, stores)


@db
def save_books(cursor: Cursor, books: list, version: int):
    query = """
                INSERT INTO books(
                    title,
                    price,
                    mark,
                    availability,
                    img_url,
                    last_scrap_version
                )
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (title) DO NOTHING
            """

    books = [
        (
            b.title,
            b.price,
            b.mark,
            b.availability,
            b.img_url,
            version
        )
        for b in books
    ]

    cursor.executemany(query, books)